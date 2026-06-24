# Database Quick Reference Card

## 🚀 One-Command Setup

```bash
# 1. Copy supabase_schema.sql
# 2. Paste into Supabase SQL Editor
# 3. Click Run
# Done! ✅
```

---

## 📋 Table: `predictions`

```
id                UUID         🔑 Primary Key
storage_path      TEXT         📁 "Healthy/abc.jpg"
image_url         TEXT         🌐 "https://..."
predicted_label   TEXT         🤖 "Healthy"
confidence        FLOAT        📊 0.95
final_label       TEXT         ✏️  NULL or "Early Blight"
uploader_id       UUID         👤 FK → auth.users
uploader_name     TEXT         👤 "John Doe"
created_at        TIMESTAMPTZ  📅 Auto
updated_at        TIMESTAMPTZ  📅 Auto (trigger)
```

---

## 🏷️ Disease Categories (10)

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

---

## 🔍 Common Queries

### Get all predictions
```sql
SELECT * FROM predictions ORDER BY created_at DESC;
```

### Get by category
```sql
SELECT * FROM predictions 
WHERE COALESCE(final_label, predicted_label) = 'Healthy';
```

### Get stats
```sql
SELECT * FROM get_category_stats();
```

### Get low confidence (need review)
```sql
SELECT * FROM get_low_confidence_predictions(0.7);
```

### Search
```sql
SELECT * FROM predictions 
WHERE storage_path ILIKE '%search%';
```

### Count by category
```sql
SELECT 
  COALESCE(final_label, predicted_label) as category,
  COUNT(*) as count
FROM predictions
GROUP BY category;
```

---

## 🔐 Security (RLS)

| Operation | Who Can Do It |
|-----------|---------------|
| SELECT (read) | ✅ Everyone |
| INSERT (create) | ✅ Everyone |
| UPDATE (edit) | 🔒 Authenticated only |
| DELETE (remove) | 🔒 Authenticated only |

---

## 📊 Views

```sql
-- Effective label (final or predicted)
SELECT * FROM predictions_with_effective_label;

-- Category statistics
SELECT * FROM category_stats;

-- Recent 100 predictions
SELECT * FROM recent_predictions;
```

---

## ⚙️ Functions

```sql
-- Stats with percentages
SELECT * FROM get_category_stats();

-- Date range
SELECT * FROM get_predictions_by_date_range(
  '2025-10-01'::TIMESTAMPTZ,
  '2025-10-31'::TIMESTAMPTZ
);

-- Low confidence
SELECT * FROM get_low_confidence_predictions(0.7);
```

---

## 🗂️ Storage: `tomato-leaves`

```
tomato-leaves/
├── Healthy/
├── Bacterial Spot/
├── Early Blight/
├── Late Blight/
├── Leaf Mold/
├── Septoria Leaf Spot/
├── Spider Mites/
├── Target Spot/
├── Mosaic Virus/
└── Yellow Curl Virus/
```

**Settings**: Public bucket ✅

---

## 🔧 Maintenance

### Check table size
```sql
SELECT pg_size_pretty(pg_total_relation_size('predictions'));
```

### Optimize
```sql
VACUUM ANALYZE predictions;
```

### Check duplicates
```sql
SELECT storage_path, COUNT(*) 
FROM predictions 
GROUP BY storage_path 
HAVING COUNT(*) > 1;
```

---

## 🎯 Admin User Setup

```
1. Go to Authentication → Users → Add user
2. Email: admin@fito.com
3. Password: (your choice)
4. Click user → User Metadata → Edit
5. Add: {"role": "admin"}
6. Save
```

---

## ✅ Verification

```sql
-- Check table exists
SELECT * FROM predictions LIMIT 1;

-- Check indexes
SELECT indexname FROM pg_indexes WHERE tablename = 'predictions';

-- Check RLS enabled
SELECT tablename, rowsecurity FROM pg_tables WHERE tablename = 'predictions';

-- Check policies
SELECT policyname FROM pg_policies WHERE tablename = 'predictions';

-- Check views
SELECT * FROM category_stats;

-- Check functions
SELECT * FROM get_category_stats();
```

---

## 📚 Full Documentation

- **Complete Schema**: `supabase_schema.sql`
- **Detailed Guide**: `DATABASE_SCHEMA.md`
- **Setup Instructions**: `SUPABASE_SETUP.md`

---

**Quick Tip**: Copy `supabase_schema.sql` into Supabase SQL Editor and run it. Everything will be set up automatically! 🚀

