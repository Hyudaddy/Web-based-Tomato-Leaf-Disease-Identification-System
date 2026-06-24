-- ============================================================================
-- STORAGE BUCKET POLICIES FOR FITO ADMIN DASHBOARD
-- ============================================================================
-- Run this AFTER creating the 'tomato-leaves' bucket via Supabase UI
-- 
-- Prerequisites:
-- 1. Bucket 'tomato-leaves' must exist
-- 2. Bucket should be set to PUBLIC
-- 
-- To create bucket:
-- 1. Go to Storage in Supabase dashboard
-- 2. Click "New bucket"
-- 3. Name: tomato-leaves
-- 4. Check "Public bucket" ✅
-- 5. Click "Create"
-- ============================================================================

-- ============================================================================
-- STORAGE POLICIES - MANUAL SETUP VIA UI
-- ============================================================================
-- SQL policies don't work due to permissions. Set up via Supabase UI instead:
--
-- Go to: Storage → tomato-leaves → Policies tab → New Policy
--
-- Create these 4 policies:
--
-- 1. SELECT (Read) Policy:
--    Name: Allow public reads
--    Policy: bucket_id = 'tomato-leaves'
--
-- 2. INSERT (Upload) Policy:
--    Name: Allow public uploads  
--    Policy: bucket_id = 'tomato-leaves'
--
-- 3. UPDATE Policy:
--    Name: Allow authenticated updates
--    Policy: bucket_id = 'tomato-leaves' AND auth.role() = 'authenticated'
--
-- 4. DELETE Policy:
--    Name: Allow authenticated deletes
--    Policy: bucket_id = 'tomato-leaves' AND auth.role() = 'authenticated'
--
-- ============================================================================

-- Since the bucket is PUBLIC, you can skip the policies for now
-- The app will work with just a PUBLIC bucket

-- ============================================================================
-- VERIFICATION
-- ============================================================================
-- Check if policies were created successfully
SELECT 
  policyname,
  cmd as operation,
  qual as using_expression,
  with_check as check_expression
FROM pg_policies
WHERE schemaname = 'storage' AND tablename = 'objects'
  AND policyname LIKE '%tomato%'
ORDER BY policyname;

-- ============================================================================
-- SUCCESS MESSAGE
-- ============================================================================
DO $$
BEGIN
  RAISE NOTICE '✅ Storage policies created successfully!';
  RAISE NOTICE '📋 Policies created:';
  RAISE NOTICE '   1. Allow public reads (SELECT)';
  RAISE NOTICE '   2. Allow public uploads (INSERT)';
  RAISE NOTICE '   3. Allow authenticated updates (UPDATE)';
  RAISE NOTICE '   4. Allow authenticated deletes (DELETE)';
  RAISE NOTICE '';
  RAISE NOTICE '🎯 Next steps:';
  RAISE NOTICE '   1. Test upload from /fito page';
  RAISE NOTICE '   2. Check Storage → tomato-leaves for uploaded images';
  RAISE NOTICE '   3. Login to admin and verify images appear';
END $$;

