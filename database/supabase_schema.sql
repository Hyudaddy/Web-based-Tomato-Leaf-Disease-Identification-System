-- ============================================================================
-- FITO ADMIN DASHBOARD - SUPABASE DATABASE SCHEMA
-- ============================================================================
-- This script sets up the complete database schema for the Fito admin dashboard
-- Run this in Supabase SQL Editor: https://supabase.com/dashboard/project/frzxrohhhpvbgwxnisww/sql
-- ============================================================================

-- ============================================================================
-- 1. CREATE PREDICTIONS TABLE
-- ============================================================================
-- This table stores all tomato leaf disease predictions and their metadata

CREATE TABLE IF NOT EXISTS predictions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  storage_path TEXT NOT NULL,
  image_url TEXT,
  predicted_label TEXT NOT NULL,
  confidence FLOAT NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
  final_label TEXT,
  uploader_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  uploader_name TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Add comments for documentation
COMMENT ON TABLE predictions IS 'Stores tomato leaf disease predictions from the AI model';
COMMENT ON COLUMN predictions.id IS 'Unique identifier for each prediction';
COMMENT ON COLUMN predictions.storage_path IS 'Path to image in Supabase Storage bucket';
COMMENT ON COLUMN predictions.image_url IS 'Public URL to access the image';
COMMENT ON COLUMN predictions.predicted_label IS 'AI model prediction result';
COMMENT ON COLUMN predictions.confidence IS 'Prediction confidence score (0.0 to 1.0)';
COMMENT ON COLUMN predictions.final_label IS 'Admin-corrected label (overrides predicted_label)';
COMMENT ON COLUMN predictions.uploader_id IS 'User ID who uploaded the image (nullable for anonymous)';
COMMENT ON COLUMN predictions.uploader_name IS 'Display name of uploader';
COMMENT ON COLUMN predictions.created_at IS 'Timestamp when prediction was created';
COMMENT ON COLUMN predictions.updated_at IS 'Timestamp when record was last updated';

-- ============================================================================
-- 2. CREATE INDEXES FOR PERFORMANCE
-- ============================================================================
-- These indexes speed up common queries

-- Index for filtering by predicted label (disease category)
CREATE INDEX IF NOT EXISTS idx_predictions_predicted_label 
ON predictions(predicted_label);

-- Index for filtering by final label (admin-corrected category)
CREATE INDEX IF NOT EXISTS idx_predictions_final_label 
ON predictions(final_label);

-- Index for sorting by creation date (most recent first)
CREATE INDEX IF NOT EXISTS idx_predictions_created_at 
ON predictions(created_at DESC);

-- Index for filtering by uploader
CREATE INDEX IF NOT EXISTS idx_predictions_uploader_id 
ON predictions(uploader_id);

-- Composite index for common query patterns (category + date)
CREATE INDEX IF NOT EXISTS idx_predictions_label_date 
ON predictions(predicted_label, created_at DESC);

-- ============================================================================
-- 3. CREATE UPDATED_AT TRIGGER
-- ============================================================================
-- Automatically update the updated_at timestamp when a record is modified

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_predictions_updated_at
    BEFORE UPDATE ON predictions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 4. ENABLE ROW LEVEL SECURITY (RLS)
-- ============================================================================
-- Protect data with row-level security policies

ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- 5. CREATE RLS POLICIES
-- ============================================================================

-- Policy 1: Allow anyone to read predictions (for public app access)
CREATE POLICY "Allow public read access" 
ON predictions
FOR SELECT
USING (true);

-- Policy 2: Allow anyone to insert predictions (for app uploads)
CREATE POLICY "Allow public insert" 
ON predictions
FOR INSERT
WITH CHECK (true);

-- Policy 3: Allow authenticated users to update predictions
CREATE POLICY "Allow authenticated update" 
ON predictions
FOR UPDATE
USING (auth.role() = 'authenticated')
WITH CHECK (auth.role() = 'authenticated');

-- Policy 4: Allow authenticated users to delete predictions
CREATE POLICY "Allow authenticated delete" 
ON predictions
FOR DELETE
USING (auth.role() = 'authenticated');

-- ============================================================================
-- 6. CREATE STORAGE BUCKET POLICIES
-- ============================================================================
-- IMPORTANT: You must create the storage bucket FIRST via Supabase UI:
-- 1. Go to Storage → New bucket
-- 2. Name: tomato-leaves
-- 3. Check "Public bucket" ✅
-- 4. Click Create
--
-- Then uncomment and run these policies (or set them via UI):

/*
-- Policy 1: Allow public uploads
CREATE POLICY "Allow public uploads"
ON storage.objects FOR INSERT
WITH CHECK (bucket_id = 'tomato-leaves');

-- Policy 2: Allow public reads
CREATE POLICY "Allow public reads"
ON storage.objects FOR SELECT
USING (bucket_id = 'tomato-leaves');

-- Policy 3: Allow authenticated deletes
CREATE POLICY "Allow authenticated deletes"
ON storage.objects FOR DELETE
USING (bucket_id = 'tomato-leaves' AND auth.role() = 'authenticated');
*/

-- Note: If bucket is set to PUBLIC, read access is automatic
-- Upload/delete policies can be set via Supabase UI → Storage → Policies

-- ============================================================================
-- 7. CREATE HELPER VIEWS
-- ============================================================================

-- View: Get effective label (final_label if set, otherwise predicted_label)
CREATE OR REPLACE VIEW predictions_with_effective_label AS
SELECT 
  id,
  storage_path,
  image_url,
  predicted_label,
  confidence,
  final_label,
  COALESCE(final_label, predicted_label) as effective_label,
  uploader_id,
  uploader_name,
  created_at,
  updated_at
FROM predictions;

COMMENT ON VIEW predictions_with_effective_label IS 'Predictions with effective label (final_label if set, otherwise predicted_label)';

-- View: Category statistics
CREATE OR REPLACE VIEW category_stats AS
SELECT 
  COALESCE(final_label, predicted_label) as category,
  COUNT(*) as count,
  AVG(confidence) as avg_confidence,
  MIN(created_at) as first_upload,
  MAX(created_at) as last_upload
FROM predictions
GROUP BY COALESCE(final_label, predicted_label)
ORDER BY count DESC;

COMMENT ON VIEW category_stats IS 'Aggregated statistics by disease category';

-- View: Recent predictions
CREATE OR REPLACE VIEW recent_predictions AS
SELECT 
  id,
  storage_path,
  image_url,
  predicted_label,
  confidence,
  final_label,
  COALESCE(final_label, predicted_label) as effective_label,
  uploader_name,
  created_at
FROM predictions
ORDER BY created_at DESC
LIMIT 100;

COMMENT ON VIEW recent_predictions IS 'Most recent 100 predictions';

-- ============================================================================
-- 8. CREATE HELPER FUNCTIONS
-- ============================================================================

-- Function: Get category statistics
CREATE OR REPLACE FUNCTION get_category_stats()
RETURNS TABLE (
  category TEXT,
  count BIGINT,
  avg_confidence FLOAT,
  percentage FLOAT
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    COALESCE(final_label, predicted_label) as category,
    COUNT(*) as count,
    AVG(confidence)::FLOAT as avg_confidence,
    (COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ())::FLOAT as percentage
  FROM predictions
  GROUP BY COALESCE(final_label, predicted_label)
  ORDER BY count DESC;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_category_stats IS 'Get statistics for each disease category with percentages';

-- Function: Get predictions by date range
CREATE OR REPLACE FUNCTION get_predictions_by_date_range(
  start_date TIMESTAMPTZ,
  end_date TIMESTAMPTZ
)
RETURNS TABLE (
  id UUID,
  predicted_label TEXT,
  confidence FLOAT,
  final_label TEXT,
  created_at TIMESTAMPTZ
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    p.id,
    p.predicted_label,
    p.confidence,
    p.final_label,
    p.created_at
  FROM predictions p
  WHERE p.created_at BETWEEN start_date AND end_date
  ORDER BY p.created_at DESC;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_predictions_by_date_range IS 'Get predictions within a specific date range';

-- Function: Get low confidence predictions (for review)
CREATE OR REPLACE FUNCTION get_low_confidence_predictions(
  confidence_threshold FLOAT DEFAULT 0.7
)
RETURNS TABLE (
  id UUID,
  storage_path TEXT,
  image_url TEXT,
  predicted_label TEXT,
  confidence FLOAT,
  created_at TIMESTAMPTZ
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    p.id,
    p.storage_path,
    p.image_url,
    p.predicted_label,
    p.confidence,
    p.created_at
  FROM predictions p
  WHERE p.confidence < confidence_threshold
    AND p.final_label IS NULL
  ORDER BY p.confidence ASC;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_low_confidence_predictions IS 'Get predictions with low confidence scores that need review';

-- ============================================================================
-- 9. INSERT SAMPLE DATA (OPTIONAL - FOR TESTING)
-- ============================================================================
-- Uncomment the following section if you want to insert sample data for testing

/*
INSERT INTO predictions (
  storage_path,
  image_url,
  predicted_label,
  confidence,
  uploader_name
) VALUES
  ('Healthy/sample-1.jpg', 'https://example.com/sample-1.jpg', 'Healthy', 0.95, 'test_user'),
  ('Bacterial Spot/sample-2.jpg', 'https://example.com/sample-2.jpg', 'Bacterial Spot', 0.87, 'test_user'),
  ('Early Blight/sample-3.jpg', 'https://example.com/sample-3.jpg', 'Early Blight', 0.92, 'test_user'),
  ('Late Blight/sample-4.jpg', 'https://example.com/sample-4.jpg', 'Late Blight', 0.89, 'test_user'),
  ('Leaf Mold/sample-5.jpg', 'https://example.com/sample-5.jpg', 'Leaf Mold', 0.91, 'test_user');
*/

-- ============================================================================
-- 10. VERIFICATION QUERIES
-- ============================================================================
-- Run these queries to verify the setup

-- Check if table exists and has correct structure
SELECT 
  table_name,
  column_name,
  data_type,
  is_nullable
FROM information_schema.columns
WHERE table_name = 'predictions'
ORDER BY ordinal_position;

-- Check if indexes exist
SELECT 
  indexname,
  indexdef
FROM pg_indexes
WHERE tablename = 'predictions';

-- Check if RLS is enabled
SELECT 
  tablename,
  rowsecurity
FROM pg_tables
WHERE tablename = 'predictions';

-- Check if policies exist
SELECT 
  policyname,
  cmd,
  qual
FROM pg_policies
WHERE tablename = 'predictions';

-- Get category statistics (should return empty if no data)
SELECT * FROM get_category_stats();

-- ============================================================================
-- SETUP COMPLETE!
-- ============================================================================
-- Next steps:
-- 1. Create storage bucket 'tomato-leaves' via Supabase UI (Storage section)
-- 2. Make the bucket PUBLIC
-- 3. Create admin user via Authentication section
-- 4. Add user metadata: {"role": "admin"}
-- 5. Start your backend and frontend servers
-- 6. Test by uploading an image
-- ============================================================================

-- Display success message
DO $$
BEGIN
  RAISE NOTICE '✅ Database schema created successfully!';
  RAISE NOTICE '📋 Next steps:';
  RAISE NOTICE '   1. Create storage bucket: tomato-leaves (make it PUBLIC)';
  RAISE NOTICE '   2. Create admin user with metadata: {"role": "admin"}';
  RAISE NOTICE '   3. Start backend: cd backend && python app.py';
  RAISE NOTICE '   4. Start frontend: cd frontend && npm run dev';
  RAISE NOTICE '   5. Test at http://localhost:3000/fito';
END $$;

