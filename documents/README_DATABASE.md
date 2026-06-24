# 🗄️ Fito Database Setup - Complete Guide

## 📦 What You Got

I've created a **complete, production-ready database schema** for your Fito admin dashboard with:

✅ **1 Main Table** - `predictions` (stores all image predictions)  
✅ **5 Indexes** - For fast queries  
✅ **4 RLS Policies** - For security  
✅ **3 Views** - For common queries  
✅ **3 Functions** - For statistics  
✅ **1 Trigger** - Auto-update timestamps  
✅ **Full Documentation** - Everything explained

---

## 🚀 Quick Setup (2 Minutes)

### Step 1: Run the Schema (1 minute)

1. Open file: **`supabase_schema.sql`**
2. Copy **ALL** the SQL code
3. Go to: https://supabase.com/dashboard/project/frzxrohhhpvbgwxnisww/sql
4. Paste into SQL Editor
5. Click **"Run"**
6. ✅ Done!

### Step 2: Create Storage Bucket (30 seconds)

1. Go to **Storage** tab in Supabase
2. Click **"New bucket"**
3. Name: `tomato-leaves`
4. Check **"Public bucket"** ✅
5. Click **"Create"**

### Step 3: Create Admin User (30 seconds)

1. Go to **Authentication** → **Users**
2. Click **"Add user"**
3. Email: `admin@fito.com`
4. Password: (your choice, e.g., `admin123`)
5. After creation, click the user
6. **User Metadata** → **Edit**
7. Add: `{"role": "admin"}`
8. **Save**

✅ **Database setup complete!**

---

## 📊 What Was Created

### Main Table: `predictions`

Stores every tomato leaf image prediction:

```
┌─────────────────────────────────────────────────────────┐
│                      predictions                        │
├─────────────────────────────────────────────────────────┤
│ id               UUID          Unique identifier        │
│ storage_path     TEXT          Path in storage          │
│ image_url        TEXT          Public image URL         │
│ predicted_label  TEXT          AI prediction            │
│ confidence       FLOAT         Confidence (0-1)         │
│ final_label      TEXT          Admin correction         │
│ uploader_id      UUID          User ID                  │
│ uploader_name    TEXT          User name                │
│ created_at       TIMESTAMPTZ   Upload time              │
│ updated_at       TIMESTAMPTZ   Last modified            │
└─────────────────────────────────────────────────────────┘
```

### Indexes (Fast Queries)

- `idx_predictions_predicted_label` - Filter by category
- `idx_predictions_final_label` - Filter by corrected label
- `idx_predictions_created_at` - Sort by date
- `idx_predictions_uploader_id` - Filter by user
- `idx_predictions_label_date` - Category + date combo

### Views (Pre-built Queries)

1. **`predictions_with_effective_label`** - Shows final label if set, else predicted
2. **`category_stats`** - Aggregated stats by category
3. **`recent_predictions`** - Last 100 predictions

### Functions (Helper Queries)

1. **`get_category_stats()`** - Stats with percentages
2. **`get_predictions_by_date_range(start, end)`** - Date filtering
3. **`get_low_confidence_predictions(threshold)`** - Find predictions needing review

### Security (RLS Policies)

- ✅ **Public read** - Anyone can view predictions
- ✅ **Public insert** - Anyone can upload (from /fito page)
- 🔒 **Authenticated update** - Only logged-in users can edit
- 🔒 **Authenticated delete** - Only logged-in users can delete

---

## 📁 Files Created

### Schema Files
- **`supabase_schema.sql`** - Complete SQL schema (run this!)
- **`DATABASE_SCHEMA.md`** - Detailed documentation
- **`DATABASE_QUICK_REFERENCE.md`** - Quick reference card
- **`README_DATABASE.md`** - This file

### Updated Files
- **`SUPABASE_SETUP.md`** - Now references schema file

---

## 🎯 Disease Categories

The database supports 10 tomato leaf disease categories:

1. **Healthy** - No disease
2. **Bacterial Spot** - Bacterial infection
3. **Early Blight** - Fungal (Alternaria)
4. **Late Blight** - Severe fungal (Phytophthora)
5. **Leaf Mold** - Mold (Passalora)
6. **Septoria Leaf Spot** - Fungal spots
7. **Spider Mites** - Pest damage
8. **Target Spot** - Circular lesions
9. **Mosaic Virus** - Viral (ToMV)
10. **Yellow Curl Virus** - Viral (TYLCV)

---

## 🔍 Example Queries

### Get all predictions
```sql
SELECT * FROM predictions ORDER BY created_at DESC;
```

### Get predictions for a category
```sql
SELECT * FROM predictions 
WHERE COALESCE(final_label, predicted_label) = 'Healthy';
```

### Get category statistics
```sql
SELECT * FROM get_category_stats();
```

**Returns:**
| category | count | avg_confidence | percentage |
|----------|-------|----------------|------------|
| Healthy | 45 | 0.94 | 30.0 |
| Early Blight | 23 | 0.87 | 15.3 |

### Find predictions needing review
```sql
SELECT * FROM get_low_confidence_predictions(0.7);
```

### Search predictions
```sql
SELECT * FROM predictions 
WHERE storage_path ILIKE '%search_term%'
   OR uploader_name ILIKE '%search_term%';
```

---

## 🔐 Security Features

### Row Level Security (RLS)
- Enabled on `predictions` table
- Protects data at database level
- Policies enforce access rules

### Authentication
- Supabase Auth integration
- Admin role in user metadata
- JWT token validation

### Storage Security
- Public bucket for image serving
- Authenticated-only deletion
- File type validation in backend

---

## 📈 Data Flow

### When User Uploads Image:

```
1. User uploads at /fito
2. Backend predicts disease
3. Image → Supabase Storage (tomato-leaves/Category/uuid.jpg)
4. Record → predictions table
   ├─ storage_path: "Healthy/abc-123.jpg"
   ├─ image_url: "https://..."
   ├─ predicted_label: "Healthy"
   ├─ confidence: 0.95
   └─ created_at: NOW()
5. User sees prediction
```

### When Admin Relabels:

```
1. Admin changes label in /admin/dataset
2. Frontend → PATCH /api/admin/dataset/{id}/label
3. Backend updates final_label
4. Trigger updates updated_at
5. Table refreshes
```

---

## 🧪 Testing Your Setup

### 1. Check Table Exists
```sql
SELECT * FROM predictions LIMIT 1;
```
Should return: Empty result (no error)

### 2. Check Views Work
```sql
SELECT * FROM category_stats;
```
Should return: Empty result (no error)

### 3. Check Functions Work
```sql
SELECT * FROM get_category_stats();
```
Should return: Empty result (no error)

### 4. Insert Test Data
```sql
INSERT INTO predictions (storage_path, image_url, predicted_label, confidence, uploader_name)
VALUES ('Healthy/test.jpg', 'https://test.com/test.jpg', 'Healthy', 0.95, 'test_user');
```

### 5. Query Test Data
```sql
SELECT * FROM predictions;
```
Should return: 1 row

### 6. Check Stats
```sql
SELECT * FROM get_category_stats();
```
Should return: 1 row (Healthy, count: 1)

---

## 🔧 Maintenance

### Check Database Size
```sql
SELECT pg_size_pretty(pg_total_relation_size('predictions')) as size;
```

### Optimize Performance
```sql
VACUUM ANALYZE predictions;
```

### Check for Duplicates
```sql
SELECT storage_path, COUNT(*) 
FROM predictions 
GROUP BY storage_path 
HAVING COUNT(*) > 1;
```

### View Index Usage
```sql
SELECT indexrelname, idx_scan 
FROM pg_stat_user_indexes 
WHERE relname = 'predictions';
```

---

## 🚨 Troubleshooting

### "relation predictions does not exist"
→ Run `supabase_schema.sql` in SQL Editor

### "bucket tomato-leaves not found"
→ Create bucket in Storage tab (make it PUBLIC)

### "permission denied"
→ Check RLS policies are created

### "function does not exist"
→ Re-run `supabase_schema.sql`

### Images not showing
→ Verify bucket is PUBLIC

---

## 📚 Documentation Reference

| File | Purpose |
|------|---------|
| `supabase_schema.sql` | **Run this first!** Complete SQL schema |
| `DATABASE_SCHEMA.md` | Detailed documentation with examples |
| `DATABASE_QUICK_REFERENCE.md` | Quick reference card |
| `SUPABASE_SETUP.md` | Step-by-step setup guide |
| `README_DATABASE.md` | This overview file |

---

## 🎓 Learn More

### Supabase Concepts

**Row Level Security (RLS)**
- Database-level security
- Policies control access per row
- Automatic enforcement

**Storage Buckets**
- S3-compatible object storage
- Public or private buckets
- CDN delivery

**Views**
- Pre-defined queries
- Simplify complex queries
- Can be used like tables

**Functions**
- Reusable SQL logic
- Can accept parameters
- Return tables or values

**Triggers**
- Automatic actions on events
- BEFORE/AFTER INSERT/UPDATE/DELETE
- Execute functions

---

## ✅ Verification Checklist

After setup, verify:

- [ ] `predictions` table exists
- [ ] 5 indexes created
- [ ] 4 RLS policies active
- [ ] 3 views accessible
- [ ] 3 functions work
- [ ] Trigger active
- [ ] Storage bucket `tomato-leaves` exists
- [ ] Bucket is PUBLIC
- [ ] Admin user created
- [ ] Admin has `role: admin` metadata

---

## 🎉 You're Ready!

Your database is now fully configured and ready to use. Next steps:

1. ✅ Database setup complete (you just did this!)
2. 🚀 Start backend: `cd backend && python app.py`
3. 🚀 Start frontend: `cd frontend && npm run dev`
4. 🧪 Test upload at: http://localhost:3000/fito
5. 🔐 Login admin at: http://localhost:3000/admin/login
6. 📊 View dashboard at: http://localhost:3000/admin

---

## 💡 Pro Tips

1. **Backup regularly**: Supabase provides automatic backups, but export important data
2. **Monitor performance**: Check index usage periodically
3. **Review low confidence**: Use `get_low_confidence_predictions()` to find images needing review
4. **Clean duplicates**: Run duplicate check monthly
5. **Optimize queries**: Use views for common queries

---

## 📞 Need Help?

- **Schema Issues**: Check `DATABASE_SCHEMA.md`
- **Setup Issues**: Check `SUPABASE_SETUP.md`
- **Quick Reference**: Check `DATABASE_QUICK_REFERENCE.md`
- **Supabase Docs**: https://supabase.com/docs

---

**Database Version**: 1.0.0  
**Created**: November 1, 2025  
**Status**: ✅ Production Ready  
**Database**: PostgreSQL (Supabase)

---

🎊 **Congratulations!** You now have a professional, scalable database for your Fito admin dashboard!

