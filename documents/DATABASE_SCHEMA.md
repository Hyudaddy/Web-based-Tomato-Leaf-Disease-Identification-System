# Fito Admin Dashboard - Database Schema Documentation

## 📊 Database Overview

The Fito admin dashboard uses **Supabase (PostgreSQL)** as its database with the following components:

- **1 Main Table**: `predictions`
- **5 Indexes**: For query optimization
- **4 RLS Policies**: For security
- **3 Views**: For common queries
- **3 Functions**: For statistics and filtering
- **1 Trigger**: For automatic timestamp updates

---

## 🗃️ Main Table: `predictions`

### Table Structure

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique identifier |
| `storage_path` | TEXT | NOT NULL | Path in Supabase Storage (e.g., "Healthy/abc-123.jpg") |
| `image_url` | TEXT | | Public URL to access the image |
| `predicted_label` | TEXT | NOT NULL | AI model's prediction (e.g., "Healthy", "Early Blight") |
| `confidence` | FLOAT | NOT NULL, CHECK (0-1) | Prediction confidence score (0.0 to 1.0) |
| `final_label` | TEXT | NULLABLE | Admin-corrected label (overrides predicted_label) |
| `uploader_id` | UUID | FOREIGN KEY → auth.users(id) | User who uploaded (NULL for anonymous) |
| `uploader_name` | TEXT | | Display name of uploader |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | When prediction was created |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | When record was last modified |

### Visual Schema

```
┌─────────────────────────────────────────────────────────────────┐
│                         predictions                             │
├─────────────────────────────────────────────────────────────────┤
│ 🔑 id                  UUID                                     │
│ 📁 storage_path        TEXT          ← "Healthy/abc-123.jpg"   │
│ 🌐 image_url           TEXT          ← "https://..."           │
│ 🤖 predicted_label     TEXT          ← "Healthy"               │
│ 📊 confidence          FLOAT         ← 0.95                    │
│ ✏️  final_label         TEXT          ← NULL or "Early Blight" │
│ 👤 uploader_id         UUID          ← FK to auth.users        │
│ 👤 uploader_name       TEXT          ← "John Doe"              │
│ 📅 created_at          TIMESTAMPTZ   ← 2025-11-01 10:30:00    │
│ 📅 updated_at          TIMESTAMPTZ   ← 2025-11-01 10:30:00    │
└─────────────────────────────────────────────────────────────────┘
```

### Disease Categories (predicted_label / final_label values)

1. **Healthy** - No disease detected
2. **Bacterial Spot** - Bacterial infection
3. **Early Blight** - Fungal disease (Alternaria solani)
4. **Late Blight** - Severe fungal disease (Phytophthora infestans)
5. **Leaf Mold** - Mold infection (Passalora fulva)
6. **Septoria Leaf Spot** - Fungal spots (Septoria lycopersici)
7. **Spider Mites** - Pest damage (Tetranychus urticae)
8. **Target Spot** - Circular lesions (Corynespora cassiicola)
9. **Mosaic Virus** - Viral infection (ToMV)
10. **Yellow Curl Virus** - Viral disease (TYLCV)

---

## 🚀 Indexes

Indexes improve query performance for common operations:

| Index Name | Columns | Purpose |
|------------|---------|---------|
| `idx_predictions_predicted_label` | predicted_label | Fast filtering by AI prediction |
| `idx_predictions_final_label` | final_label | Fast filtering by admin label |
| `idx_predictions_created_at` | created_at DESC | Fast sorting by date (newest first) |
| `idx_predictions_uploader_id` | uploader_id | Fast filtering by user |
| `idx_predictions_label_date` | predicted_label, created_at DESC | Composite for category + date queries |

### Query Performance Examples

```sql
-- Fast: Uses idx_predictions_predicted_label
SELECT * FROM predictions WHERE predicted_label = 'Healthy';

-- Fast: Uses idx_predictions_created_at
SELECT * FROM predictions ORDER BY created_at DESC LIMIT 20;

-- Fast: Uses idx_predictions_label_date
SELECT * FROM predictions 
WHERE predicted_label = 'Early Blight' 
ORDER BY created_at DESC;
```

---

## 🔐 Row Level Security (RLS) Policies

| Policy Name | Operation | Rule | Purpose |
|-------------|-----------|------|---------|
| `Allow public read access` | SELECT | `true` | Anyone can read predictions |
| `Allow public insert` | INSERT | `true` | Anyone can create predictions |
| `Allow authenticated update` | UPDATE | `auth.role() = 'authenticated'` | Only logged-in users can update |
| `Allow authenticated delete` | DELETE | `auth.role() = 'authenticated'` | Only logged-in users can delete |

### Security Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     RLS Security Layers                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Public Access (No Auth Required):                              │
│  ✅ Read all predictions                                        │
│  ✅ Insert new predictions (from /fito page)                    │
│                                                                 │
│  Authenticated Access (Login Required):                         │
│  ✅ Update predictions (relabel)                                │
│  ✅ Delete predictions                                          │
│                                                                 │
│  Admin Access (Admin Role Required):                            │
│  ✅ All of the above                                            │
│  ✅ Access admin dashboard                                      │
│  ✅ Export data                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Views

### 1. `predictions_with_effective_label`

Returns predictions with an "effective_label" column that shows the final_label if set, otherwise the predicted_label.

```sql
CREATE VIEW predictions_with_effective_label AS
SELECT 
  *,
  COALESCE(final_label, predicted_label) as effective_label
FROM predictions;
```

**Use case**: Display the "true" label for each prediction in the admin dashboard.

### 2. `category_stats`

Aggregated statistics by disease category.

```sql
CREATE VIEW category_stats AS
SELECT 
  COALESCE(final_label, predicted_label) as category,
  COUNT(*) as count,
  AVG(confidence) as avg_confidence,
  MIN(created_at) as first_upload,
  MAX(created_at) as last_upload
FROM predictions
GROUP BY COALESCE(final_label, predicted_label);
```

**Use case**: Dashboard statistics showing counts per category.

### 3. `recent_predictions`

Most recent 100 predictions.

```sql
CREATE VIEW recent_predictions AS
SELECT 
  id, storage_path, image_url, predicted_label, 
  confidence, final_label, uploader_name, created_at
FROM predictions
ORDER BY created_at DESC
LIMIT 100;
```

**Use case**: Quick access to recent uploads.

---

## ⚙️ Functions

### 1. `get_category_stats()`

Returns category statistics with percentages.

```sql
SELECT * FROM get_category_stats();
```

**Returns:**
| category | count | avg_confidence | percentage |
|----------|-------|----------------|------------|
| Healthy | 45 | 0.94 | 30.0 |
| Early Blight | 23 | 0.87 | 15.3 |
| ... | ... | ... | ... |

### 2. `get_predictions_by_date_range(start_date, end_date)`

Get predictions within a date range.

```sql
SELECT * FROM get_predictions_by_date_range(
  '2025-10-01'::TIMESTAMPTZ,
  '2025-10-31'::TIMESTAMPTZ
);
```

**Use case**: Monthly reports, trend analysis.

### 3. `get_low_confidence_predictions(threshold)`

Get predictions with confidence below threshold (default 0.7).

```sql
SELECT * FROM get_low_confidence_predictions(0.7);
```

**Use case**: Find predictions that need manual review.

---

## 🔄 Triggers

### `update_predictions_updated_at`

Automatically updates the `updated_at` timestamp whenever a record is modified.

```sql
-- Trigger function
CREATE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger
CREATE TRIGGER update_predictions_updated_at
    BEFORE UPDATE ON predictions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

**Effect**: Every UPDATE automatically sets `updated_at = NOW()`.

---

## 📦 Storage Bucket: `tomato-leaves`

### Bucket Configuration
- **Name**: `tomato-leaves`
- **Visibility**: Public
- **Purpose**: Store uploaded tomato leaf images

### Folder Structure
```
tomato-leaves/
├── Healthy/
│   ├── abc-123-def.jpg
│   ├── xyz-456-ghi.jpg
│   └── ...
├── Bacterial Spot/
│   ├── aaa-111-bbb.jpg
│   └── ...
├── Early Blight/
│   └── ...
├── Late Blight/
│   └── ...
├── Leaf Mold/
│   └── ...
├── Septoria Leaf Spot/
│   └── ...
├── Spider Mites/
│   └── ...
├── Target Spot/
│   └── ...
├── Mosaic Virus/
│   └── ...
└── Yellow Curl Virus/
    └── ...
```

### Storage Policies

| Policy | Operation | Rule |
|--------|-----------|------|
| Public read | SELECT | Anyone can view images |
| Public upload | INSERT | Anyone can upload images |
| Authenticated delete | DELETE | Only logged-in users can delete |

---

## 🔗 Relationships

### Foreign Key: `uploader_id` → `auth.users(id)`

```
┌──────────────────┐           ┌──────────────────┐
│  predictions     │           │   auth.users     │
├──────────────────┤           ├──────────────────┤
│ id               │           │ id               │
│ uploader_id      │──────────▶│ email            │
│ uploader_name    │           │ user_metadata    │
│ ...              │           │   └─ role: admin │
└──────────────────┘           └──────────────────┘
```

**Cascade behavior**: `ON DELETE SET NULL` - If user is deleted, uploader_id becomes NULL but prediction remains.

---

## 📈 Common Queries

### Get all predictions for a category
```sql
SELECT * FROM predictions
WHERE COALESCE(final_label, predicted_label) = 'Healthy'
ORDER BY created_at DESC;
```

### Get predictions needing review (low confidence)
```sql
SELECT * FROM predictions
WHERE confidence < 0.7 
  AND final_label IS NULL
ORDER BY confidence ASC;
```

### Get category counts
```sql
SELECT 
  COALESCE(final_label, predicted_label) as category,
  COUNT(*) as count
FROM predictions
GROUP BY category
ORDER BY count DESC;
```

### Get predictions by date range
```sql
SELECT * FROM predictions
WHERE created_at BETWEEN '2025-10-01' AND '2025-10-31'
ORDER BY created_at DESC;
```

### Get predictions with corrections
```sql
SELECT * FROM predictions
WHERE final_label IS NOT NULL 
  AND final_label != predicted_label;
```

### Search predictions
```sql
SELECT * FROM predictions
WHERE storage_path ILIKE '%search_term%'
   OR uploader_name ILIKE '%search_term%'
   OR predicted_label ILIKE '%search_term%';
```

---

## 🎯 Data Flow

### Insert Flow (New Prediction)
```
1. User uploads image at /fito
2. Backend receives image
3. AI model makes prediction
4. Backend uploads image to Storage → storage_path
5. Backend gets public URL → image_url
6. Backend inserts record into predictions table
7. Trigger sets created_at and updated_at
8. Response sent to user
```

### Update Flow (Relabel)
```
1. Admin clicks relabel in /admin/dataset
2. Frontend sends PATCH request
3. Backend updates final_label
4. Trigger automatically updates updated_at
5. Response sent to frontend
6. Table refreshes with new label
```

### Delete Flow
```
1. Admin clicks delete
2. Confirmation dialog
3. Frontend sends DELETE request
4. Backend fetches storage_path
5. Backend deletes from Storage
6. Backend deletes from predictions table
7. Response sent to frontend
8. Table refreshes
```

---

## 🔧 Maintenance Queries

### Check table size
```sql
SELECT 
  pg_size_pretty(pg_total_relation_size('predictions')) as total_size,
  pg_size_pretty(pg_relation_size('predictions')) as table_size,
  pg_size_pretty(pg_indexes_size('predictions')) as indexes_size;
```

### Check index usage
```sql
SELECT 
  indexrelname as index_name,
  idx_scan as times_used,
  idx_tup_read as tuples_read,
  idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public' AND relname = 'predictions';
```

### Vacuum and analyze (optimize)
```sql
VACUUM ANALYZE predictions;
```

### Check for duplicate images
```sql
SELECT storage_path, COUNT(*) 
FROM predictions 
GROUP BY storage_path 
HAVING COUNT(*) > 1;
```

---

## 📊 Sample Data

### Insert Sample Predictions
```sql
INSERT INTO predictions (storage_path, image_url, predicted_label, confidence, uploader_name)
VALUES
  ('Healthy/sample-1.jpg', 'https://...', 'Healthy', 0.95, 'test_user'),
  ('Bacterial Spot/sample-2.jpg', 'https://...', 'Bacterial Spot', 0.87, 'test_user'),
  ('Early Blight/sample-3.jpg', 'https://...', 'Early Blight', 0.92, 'test_user');
```

---

## 🚀 Quick Setup

### 1. Run the Schema
```bash
# Copy the SQL from supabase_schema.sql
# Paste into Supabase SQL Editor
# Click "Run"
```

### 2. Create Storage Bucket
```
1. Go to Storage in Supabase dashboard
2. Click "New bucket"
3. Name: tomato-leaves
4. Make it PUBLIC ✅
5. Click "Create"
```

### 3. Verify Setup
```sql
-- Check table
SELECT * FROM predictions LIMIT 1;

-- Check views
SELECT * FROM category_stats;

-- Check functions
SELECT * FROM get_category_stats();
```

---

## 📚 Additional Resources

- **Full Schema**: `supabase_schema.sql`
- **Setup Guide**: `SUPABASE_SETUP.md`
- **Quick Start**: `QUICK_START.md`
- **Supabase Docs**: https://supabase.com/docs

---

**Schema Version**: 1.0.0  
**Last Updated**: November 1, 2025  
**Database**: PostgreSQL (Supabase)

