# Quick Start Guide - Fito Admin Dashboard

## 🚀 5-Minute Setup

### Step 1: Supabase Database Setup (1 minute)

1. **Go to Supabase SQL Editor**: https://supabase.com/dashboard/project/frzxrohhhpvbgwxnisww/sql

2. **Copy and paste ALL of `supabase_schema.sql`** and click Run

   OR manually run this SQL:

```sql
-- Create table
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

-- Create indexes
CREATE INDEX idx_predictions_predicted_label ON predictions(predicted_label);
CREATE INDEX idx_predictions_final_label ON predictions(final_label);
CREATE INDEX idx_predictions_created_at ON predictions(created_at DESC);

-- Enable RLS
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Allow public read" ON predictions FOR SELECT USING (true);
CREATE POLICY "Allow public insert" ON predictions FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow auth update" ON predictions FOR UPDATE USING (auth.role() = 'authenticated');
CREATE POLICY "Allow auth delete" ON predictions FOR DELETE USING (auth.role() = 'authenticated');
```

3. **Create Storage Bucket**:
   - Go to Storage → New bucket
   - Name: `tomato-leaves`
   - Make it **Public** ✅
   - Click Create

4. **Add Storage Policies** (Optional - run `storage_policies.sql`):
   - After creating bucket, copy `storage_policies.sql`
   - Paste into SQL Editor and Run
   - This sets upload/delete permissions
   - (If bucket is PUBLIC, read access works automatically)

5. **Create Admin User**:
   - Go to Authentication → Users → Add user
   - Email: `admin@fito.com`
   - Password: `admin123` (or your choice)
   - After creation, click the user → User Metadata → Edit
   - Add: `{"role": "admin"}`
   - Save

### Step 2: Start Backend (1 minute)

```bash
cd backend
python app.py
```

Should see:
```
🍅 Starting Fito API Server...
API Documentation: http://localhost:8000/docs
```

### Step 3: Start Frontend (1 minute)

Open new terminal:

```bash
cd frontend
npm run dev
```

Should see:
```
✓ Ready on http://localhost:3000
```

### Step 4: Test (1 minute)

1. **Upload Image**: http://localhost:3000/fito
   - Upload any tomato leaf image
   - Should get prediction

2. **Admin Login**: http://localhost:3000/admin/login
   - Email: `admin@fito.com`
   - Password: `admin123`

3. **View Dashboard**: Should see stats

4. **View Dataset**: Click "Dataset" in sidebar

✅ **Done!**

---

## 📋 Admin Features

### Dashboard (`/admin`)
- Total images count
- Category breakdown
- Visual statistics

### Dataset (`/admin/dataset`)
- **Filter** by category
- **Search** images
- **Preview** full-size
- **Relabel** categories
- **Download** images
- **Delete** images
- **Export** CSV/ZIP

---

## 🔑 Default Credentials

**Admin Login:**
- URL: http://localhost:3000/admin/login
- Email: `admin@fito.com`
- Password: `admin123` (or what you set)

---

## 🐛 Quick Fixes

### "Table doesn't exist"
→ Run Step 1 SQL again

### "Bucket not found"
→ Create `tomato-leaves` bucket (Step 1.3)

### "Can't login"
→ Check user metadata has `"role": "admin"`

### "Images not showing"
→ Make sure bucket is **Public**

### Backend error
→ Check `.env` file exists in `backend/`

### Frontend error
→ Check `.env.local` exists in `frontend/`

---

## 📁 File Locations

```
✅ frontend/.env.local          (Supabase credentials)
✅ frontend/src/lib/supabase.ts (Supabase client)
✅ frontend/src/app/admin/      (Admin pages)
✅ backend/.env                 (Supabase credentials)
✅ backend/supabase_client.py   (Supabase client)
✅ backend/admin_routes.py      (Admin API)
```

---

## 🎯 Test Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can upload image at `/fito`
- [ ] Image appears in Supabase Storage
- [ ] Record in predictions table
- [ ] Can login at `/admin/login`
- [ ] Dashboard shows stats
- [ ] Can filter dataset
- [ ] Can preview image
- [ ] Can relabel image
- [ ] Can download image
- [ ] Can export CSV

---

## 📚 Full Documentation

- **Setup Details**: `SUPABASE_SETUP.md`
- **Complete Guide**: `ADMIN_DASHBOARD_README.md`
- **API Docs**: http://localhost:8000/docs

---

## 🆘 Need Help?

1. Check Supabase dashboard for data
2. Check browser console (F12)
3. Check terminal for errors
4. Review `SUPABASE_SETUP.md`

---

**Ready to use!** 🎉

