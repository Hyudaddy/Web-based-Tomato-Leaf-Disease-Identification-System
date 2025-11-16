# Setup Troubleshooting Guide

## 🚨 Common Errors & Solutions

### Error: "relation storage.policies does not exist"

**Cause**: The SQL tried to create storage policies before the bucket exists, or using wrong syntax.

**Solution**:
1. ✅ Run `supabase_schema.sql` first (storage policies are commented out)
2. ✅ Create the `tomato-leaves` bucket via Supabase UI
3. ✅ Then run `storage_policies.sql` separately

**Steps**:
```bash
# Step 1: Run main schema
Copy supabase_schema.sql → Paste in SQL Editor → Run

# Step 2: Create bucket manually
Go to Storage → New bucket → Name: tomato-leaves → Public ✅ → Create

# Step 3: Run storage policies
Copy storage_policies.sql → Paste in SQL Editor → Run
```

---

### Error: "relation predictions does not exist"

**Cause**: The `predictions` table wasn't created.

**Solution**:
1. Go to Supabase SQL Editor
2. Copy ALL of `supabase_schema.sql`
3. Paste and click "Run"
4. Wait for success message

**Verify**:
```sql
SELECT * FROM predictions LIMIT 1;
```
Should return empty result (not an error).

---

### Error: "bucket tomato-leaves not found"

**Cause**: Storage bucket doesn't exist.

**Solution**:
1. Go to **Storage** in Supabase dashboard
2. Click **"New bucket"**
3. Name: `tomato-leaves`
4. Check **"Public bucket"** ✅
5. Click **"Create"**

**Verify**:
- You should see `tomato-leaves` in the buckets list
- Try uploading a test image manually

---

### Error: "permission denied for table predictions"

**Cause**: RLS policies not created or incorrect.

**Solution**:
1. Check if RLS is enabled:
```sql
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE tablename = 'predictions';
```
Should show `rowsecurity = true`

2. Check if policies exist:
```sql
SELECT policyname FROM pg_policies WHERE tablename = 'predictions';
```
Should show 4 policies.

3. If missing, re-run the RLS section from `supabase_schema.sql`

---

### Error: "Access denied" when logging into admin

**Cause**: User doesn't have admin role in metadata.

**Solution**:
1. Go to **Authentication** → **Users**
2. Click on your admin user
3. Scroll to **User Metadata**
4. Click **Edit**
5. Add exactly: `{"role": "admin"}`
6. Click **Save**

**Verify**:
- User metadata should show: `{ "role": "admin" }`
- Try logging in again

---

### Error: Images not showing in admin dashboard

**Cause**: Multiple possible issues.

**Solutions**:

**1. Check if images are in storage:**
```sql
SELECT storage_path, image_url FROM predictions LIMIT 5;
```

**2. Verify storage bucket is PUBLIC:**
- Go to Storage → tomato-leaves
- Check if bucket shows "Public" badge
- If not, click bucket settings → Make public

**3. Check image URLs:**
- Image URLs should start with your Supabase URL
- Example: `https://frzxrohhhpvbgwxnisww.supabase.co/storage/v1/object/public/tomato-leaves/...`

**4. Check browser console:**
- Press F12
- Look for CORS or 404 errors
- If CORS error, check backend CORS settings

---

### Error: "Failed to save to Supabase" in backend logs

**Cause**: Backend can't connect to Supabase or wrong credentials.

**Solution**:

**1. Check backend `.env` file exists:**
```bash
# backend/.env should contain:
SUPABASE_URL=https://frzxrohhhpvbgwxnisww.supabase.co
SUPABASE_ANON_KEY=eyJhbGci...
SUPABASE_SERVICE_KEY=eyJhbGci...
```

**2. Verify credentials are correct:**
- Go to Supabase → Settings → API
- Compare URL and keys

**3. Check if supabase package is installed:**
```bash
cd backend
pip install supabase python-dotenv
```

**4. Test connection:**
```python
from supabase_client import get_supabase_client
supabase = get_supabase_client()
print(supabase.table("predictions").select("*").limit(1).execute())
```

---

### Error: Frontend can't connect to backend

**Cause**: Backend not running or wrong URL.

**Solution**:

**1. Check backend is running:**
```bash
cd backend
python app.py
```
Should see: `Uvicorn running on http://0.0.0.0:8000`

**2. Test backend directly:**
Open browser: http://localhost:8000/health
Should return: `{"status": "healthy"}`

**3. Check frontend is using correct URL:**
- Frontend should call `http://localhost:8000/predict`
- Check browser console for errors

---

### Error: "Module not found" errors

**Cause**: Dependencies not installed.

**Solution**:

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

---

### Error: Views or Functions don't exist

**Cause**: Schema wasn't fully executed.

**Solution**:
1. Re-run entire `supabase_schema.sql`
2. Check for any error messages during execution
3. Verify views exist:
```sql
SELECT viewname FROM pg_views WHERE schemaname = 'public';
```
Should show: `predictions_with_effective_label`, `category_stats`, `recent_predictions`

4. Verify functions exist:
```sql
SELECT proname FROM pg_proc WHERE proname LIKE 'get_%';
```
Should show: `get_category_stats`, `get_predictions_by_date_range`, `get_low_confidence_predictions`

---

## 🔍 Diagnostic Queries

### Check Everything is Set Up

```sql
-- Check table exists
SELECT EXISTS (
  SELECT FROM information_schema.tables 
  WHERE table_name = 'predictions'
);

-- Check RLS is enabled
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE tablename = 'predictions';

-- Check policies exist
SELECT COUNT(*) as policy_count 
FROM pg_policies 
WHERE tablename = 'predictions';

-- Check indexes exist
SELECT COUNT(*) as index_count 
FROM pg_indexes 
WHERE tablename = 'predictions';

-- Check views exist
SELECT COUNT(*) as view_count 
FROM pg_views 
WHERE schemaname = 'public' 
AND viewname LIKE '%prediction%';

-- Check functions exist
SELECT COUNT(*) as function_count 
FROM pg_proc 
WHERE proname LIKE 'get_%';
```

**Expected Results:**
- Table exists: `true`
- RLS enabled: `true`
- Policy count: `4`
- Index count: `5`
- View count: `3`
- Function count: `3`

---

## 🧪 Test Queries

### Test Insert
```sql
INSERT INTO predictions (
  storage_path, 
  image_url, 
  predicted_label, 
  confidence, 
  uploader_name
) VALUES (
  'test/test.jpg',
  'https://example.com/test.jpg',
  'Healthy',
  0.95,
  'test_user'
) RETURNING *;
```

### Test Select
```sql
SELECT * FROM predictions ORDER BY created_at DESC LIMIT 5;
```

### Test Update
```sql
UPDATE predictions 
SET final_label = 'Early Blight' 
WHERE predicted_label = 'Healthy' 
LIMIT 1
RETURNING *;
```

### Test Views
```sql
SELECT * FROM category_stats;
SELECT * FROM recent_predictions LIMIT 5;
```

### Test Functions
```sql
SELECT * FROM get_category_stats();
SELECT * FROM get_low_confidence_predictions(0.7);
```

---

## 📞 Still Having Issues?

### Checklist

- [ ] `supabase_schema.sql` ran without errors
- [ ] `tomato-leaves` bucket exists and is PUBLIC
- [ ] `storage_policies.sql` ran successfully (optional)
- [ ] Admin user created with `{"role": "admin"}` metadata
- [ ] Backend `.env` file has correct credentials
- [ ] Frontend `.env.local` file has correct credentials
- [ ] Backend is running on port 8000
- [ ] Frontend is running on port 3000
- [ ] Can access http://localhost:8000/health
- [ ] Can access http://localhost:3000

### Get More Help

1. **Check Supabase Logs**: Go to Supabase → Logs → API Logs
2. **Check Backend Logs**: Look at terminal where backend is running
3. **Check Browser Console**: Press F12 → Console tab
4. **Review Documentation**:
   - `DATABASE_SCHEMA.md` - Full schema details
   - `SUPABASE_SETUP.md` - Step-by-step setup
   - `QUICK_START.md` - Quick setup guide

---

## 💡 Pro Tips

1. **Always create bucket BEFORE running storage policies**
2. **Make bucket PUBLIC for easier testing**
3. **Check Supabase dashboard for visual confirmation**
4. **Use SQL Editor's "Run" button, not "Execute"**
5. **Wait for success messages before moving to next step**
6. **Test with sample data before using real data**
7. **Keep backup of working schema**

---

## 🎯 Quick Reset (if everything is broken)

```sql
-- WARNING: This deletes all data!

-- Drop everything
DROP TABLE IF EXISTS predictions CASCADE;
DROP VIEW IF EXISTS predictions_with_effective_label CASCADE;
DROP VIEW IF EXISTS category_stats CASCADE;
DROP VIEW IF EXISTS recent_predictions CASCADE;
DROP FUNCTION IF EXISTS get_category_stats() CASCADE;
DROP FUNCTION IF EXISTS get_predictions_by_date_range(TIMESTAMPTZ, TIMESTAMPTZ) CASCADE;
DROP FUNCTION IF EXISTS get_low_confidence_predictions(FLOAT) CASCADE;
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- Then re-run supabase_schema.sql
```

---

**Last Updated**: November 1, 2025  
**For**: Fito Admin Dashboard v1.0.0

