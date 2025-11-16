# Supabase Setup Guide for Fito Admin Dashboard

This guide will help you set up the Supabase database and storage for the Fito admin dashboard.

## Prerequisites

- Supabase account (already created)
- Project URL: `https://frzxrohhhpvbgwxnisww.supabase.co`

## Step 1: Create Database Table

**EASY METHOD**: Use the complete schema file!

1. Open the file: `supabase_schema.sql`
2. Copy ALL the SQL code
3. Go to your Supabase project dashboard → SQL Editor → New Query
4. Paste and click **Run**
5. Done! ✅ (Skip to Step 2)

**OR MANUAL METHOD**: Run the following SQL:

```sql
-- Create predictions table
CREATE TABLE predictions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  storage_path TEXT NOT NULL,
  image_url TEXT,
  predicted_label TEXT NOT NULL,
  confidence FLOAT NOT NULL,
  final_label TEXT,
  uploader_id UUID REFERENCES auth.users(id),
  uploader_name TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX idx_predictions_predicted_label ON predictions(predicted_label);
CREATE INDEX idx_predictions_final_label ON predictions(final_label);
CREATE INDEX idx_predictions_created_at ON predictions(created_at DESC);

-- Enable Row Level Security
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;

-- Policy: Allow public read access (for now)
CREATE POLICY "Allow public read access" ON predictions
  FOR SELECT
  USING (true);

-- Policy: Allow public insert (for predictions from the app)
CREATE POLICY "Allow public insert" ON predictions
  FOR INSERT
  WITH CHECK (true);

-- Policy: Allow authenticated users to update
CREATE POLICY "Allow authenticated update" ON predictions
  FOR UPDATE
  USING (auth.role() = 'authenticated');

-- Policy: Allow authenticated users to delete
CREATE POLICY "Allow authenticated delete" ON predictions
  FOR DELETE
  USING (auth.role() = 'authenticated');
```

## Step 2: Create Storage Bucket

1. Go to **Storage** in the left sidebar
2. Click **New bucket**
3. Bucket name: `tomato-leaves`
4. Make it **Public** (check the public checkbox)
5. Click **Create bucket**

### Configure Storage Policies

After creating the bucket, set up policies:

1. Click on the `tomato-leaves` bucket
2. Go to **Policies** tab
3. Add the following policies:

**Policy 1: Public Read Access**
```sql
CREATE POLICY "Public read access"
ON storage.objects FOR SELECT
USING (bucket_id = 'tomato-leaves');
```

**Policy 2: Public Upload Access**
```sql
CREATE POLICY "Public upload access"
ON storage.objects FOR INSERT
WITH CHECK (bucket_id = 'tomato-leaves');
```

**Policy 3: Authenticated Delete Access**
```sql
CREATE POLICY "Authenticated delete access"
ON storage.objects FOR DELETE
USING (bucket_id = 'tomato-leaves' AND auth.role() = 'authenticated');
```

## Step 3: Create Admin User

1. Go to **Authentication** → **Users**
2. Click **Add user**
3. Email: `admin@fito.com` (or your preferred email)
4. Password: Create a strong password
5. Click **Create user**

### Set Admin Role

After creating the user, you need to set the admin role in user metadata:

1. Click on the user you just created
2. Scroll to **User Metadata**
3. Click **Edit**
4. Add the following JSON:
```json
{
  "role": "admin"
}
```
5. Click **Save**

## Step 4: Verify Setup

### Test Database Connection

Run this query in SQL Editor:

```sql
SELECT * FROM predictions LIMIT 1;
```

Should return empty result (no errors).

### Test Storage

1. Go to Storage → `tomato-leaves`
2. Try uploading a test image manually
3. Verify you can view it

## Step 5: Environment Variables

The environment variables are already configured in:

### Frontend (`frontend/.env.local`)
```
NEXT_PUBLIC_SUPABASE_URL=https://frzxrohhhpvbgwxnisww.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGci...
```

### Backend (`backend/.env`)
```
SUPABASE_URL=https://frzxrohhhpvbgwxnisww.supabase.co
SUPABASE_ANON_KEY=eyJhbGci...
SUPABASE_SERVICE_KEY=eyJhbGci...
```

## Step 6: Test the Integration

### Start Backend
```bash
cd backend
python app.py
```

### Start Frontend
```bash
cd frontend
npm run dev
```

### Test Flow

1. **Upload Image**: Go to `http://localhost:3000/fito` and upload a tomato leaf image
2. **Check Supabase**: 
   - Go to Storage → `tomato-leaves` → should see uploaded image
   - Go to Table Editor → `predictions` → should see new record
3. **Admin Login**: Go to `http://localhost:3000/admin/login`
   - Email: `admin@fito.com`
   - Password: (your password)
4. **View Dashboard**: Should see category counts
5. **View Dataset**: Should see uploaded images with filters and actions

## Troubleshooting

### Issue: "relation predictions does not exist"
- Solution: Run the SQL in Step 1 again

### Issue: "storage bucket not found"
- Solution: Create the `tomato-leaves` bucket in Step 2

### Issue: "Access denied" on admin login
- Solution: Verify user metadata has `"role": "admin"` in Step 3

### Issue: Images not uploading
- Solution: Check storage bucket policies in Step 2

### Issue: CORS errors
- Solution: Backend CORS is set to allow all origins. Check if backend is running.

## Database Schema Reference

### predictions table

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key (auto-generated) |
| storage_path | TEXT | Path in storage bucket |
| image_url | TEXT | Public URL of image |
| predicted_label | TEXT | AI prediction result |
| confidence | FLOAT | Prediction confidence (0-1) |
| final_label | TEXT | Admin-corrected label (nullable) |
| uploader_id | UUID | User ID (nullable) |
| uploader_name | TEXT | User name or "anonymous" |
| created_at | TIMESTAMPTZ | Upload timestamp |
| updated_at | TIMESTAMPTZ | Last update timestamp |

## Disease Categories

The system supports 10 categories:
1. Healthy
2. Bacterial Spot
3. Early Blight
4. Late Blight
5. Leaf Mold
6. Septoria Leaf Spot
7. Spider Mites
8. Target Spot
9. Mosaic Virus
10. Yellow Curl Virus

## Next Steps

After setup is complete:
- Test uploading images from the main app
- Login to admin dashboard
- Test filtering by category
- Test relabeling images
- Test CSV export
- Test image downloads

## Security Notes

- Service role key should NEVER be exposed in frontend
- Consider implementing proper authentication for production
- Review and tighten RLS policies for production use
- Enable email confirmation for user signups
- Set up proper backup strategy for database and storage

