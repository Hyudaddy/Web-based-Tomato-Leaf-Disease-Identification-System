# 🔐 Fito Authentication System

## Overview

The Fito Tomato Leaf Disease Identification System now includes a complete authentication system with sign-in and sign-up functionality for admin users.

---

## ✨ Features

### User-Facing Features
- ✅ **Minimalist Login Page** - Clean, no-card design matching site aesthetics
- ✅ **Sign-In Form** - Email and password authentication
- ✅ **Sign-Up Form** - New user registration with validation
- ✅ **Form Toggle** - Easy switch between sign-in and sign-up
- ✅ **Email Verification** - Secure account creation
- ✅ **Error Handling** - Clear, user-friendly error messages
- ✅ **Success Feedback** - Confirmation messages for actions
- ✅ **Responsive Design** - Works perfectly on all devices
- ✅ **Glassmorphism UI** - Modern backdrop blur effects
- ✅ **Smooth Animations** - Professional transitions and hover effects

### Admin Features
- ✅ **Role-Based Access Control** - Admin and Super Admin roles
- ✅ **Admin Profiles** - Comprehensive profile management
- ✅ **Last Login Tracking** - Security monitoring
- ✅ **Active Status** - Enable/disable admin accounts
- ✅ **Auto Profile Creation** - Automatic profile setup on signup
- ✅ **Dashboard Access** - Protected admin dashboard
- ✅ **Dataset Management** - Full CRUD operations on predictions

### Security Features
- ✅ **Row Level Security (RLS)** - Database-level access control
- ✅ **Password Validation** - Minimum 6 characters
- ✅ **Email Confirmation** - Verified accounts only
- ✅ **Admin-Only Routes** - Protected admin pages
- ✅ **Session Management** - Secure authentication tokens
- ✅ **Role Verification** - Server-side role checking

---

## 🎨 Design Philosophy

### Minimalist Approach
The login page follows the same minimalist design principles as the rest of the Fito system:

- **No Cards**: Forms float directly on the background
- **Glassmorphism**: Transparent inputs with backdrop blur
- **Consistent Colors**: Green accent (#47f793) matching the brand
- **Clean Typography**: Montserrat font for headings
- **Simple Layout**: Centered, focused design
- **Smooth Interactions**: Subtle animations and transitions

### Visual Consistency
- Same tomato leaf background as home page
- Matching navigation bar style
- Consistent button designs
- Unified color scheme
- Responsive breakpoints

---

## 🚀 Getting Started

### Prerequisites
- Supabase account and project
- Node.js and npm installed
- Fito frontend and backend set up

### Installation

#### 1. Database Setup

**Run Main Schema (if not done):**
```bash
# Copy contents of supabase_schema.sql
# Paste into Supabase SQL Editor
# Click "Run"
```

**Run Admin Profiles Schema:**
```bash
# Copy contents of admin_profiles_schema.sql
# Paste into Supabase SQL Editor
# Click "Run"
```

#### 2. Create First Admin

**Option A: Via Supabase UI (Recommended)**
1. Go to Supabase Dashboard → Authentication → Users
2. Click "Add user"
3. Fill in:
   - Email: `admin@fito.com`
   - Password: Your choice
   - Auto Confirm User: ✅
4. Click "Create user"
5. Click on the user to edit
6. In User Metadata, add:
   ```json
   {
     "role": "admin",
     "full_name": "Admin User"
   }
   ```
7. Save

**Option B: Via Sign-Up Page**
1. Start frontend: `npm run dev`
2. Go to: `http://localhost:3000/login`
3. Click "Don't have an account? Sign Up"
4. Fill in the form and submit
5. Verify email
6. Manually add admin role via Supabase UI (see Option A, steps 5-7)

#### 3. Test Login

```bash
# Start frontend
cd frontend
npm run dev

# Visit login page
http://localhost:3000/login

# Sign in with admin credentials
# Should redirect to /admin dashboard
```

---

## 📍 Routes

| Route | Description | Access Level | Features |
|-------|-------------|--------------|----------|
| `/login` | Main login page | Public | Sign-in, Sign-up, Form toggle |
| `/admin` | Admin dashboard | Admin only | Statistics, Category cards |
| `/admin/login` | Legacy admin login | Public | Simple sign-in only |
| `/admin/dataset` | Dataset manager | Admin only | View, Edit, Delete, Export |

---

## 🔑 User Roles

### Regular Admin
**Permissions:**
- ✅ View admin dashboard
- ✅ View dataset
- ✅ Edit predictions (relabel)
- ✅ Delete predictions
- ✅ Export data (CSV, ZIP)
- ✅ Update own profile
- ❌ Create/delete other admins
- ❌ Change user roles

**Use Case:** Day-to-day dataset management and monitoring

### Super Admin
**Permissions:**
- ✅ All regular admin permissions
- ✅ Create new admin users
- ✅ Update any admin profile
- ✅ Delete admin users
- ✅ Promote/demote admins
- ✅ Deactivate accounts
- ✅ View admin statistics

**Use Case:** System administration and user management

---

## 🔒 Security Architecture

### Authentication Flow

```
┌─────────────────────────────────────────────────────────┐
│                    User Access Flow                     │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
                   Click "Log-in" Button
                           │
                           ▼
                  Redirect to /login
                           │
                           ▼
            ┌──────────────┴──────────────┐
            │                             │
            ▼                             ▼
        Sign-In                       Sign-Up
            │                             │
            ▼                             ▼
    Enter Credentials            Enter User Details
            │                             │
            ▼                             ▼
    Supabase Auth                 Create Account
            │                             │
            ▼                             ▼
    Verify Credentials           Email Verification
            │                             │
            ▼                             ▼
    Check User Metadata          Add Admin Role (Manual)
            │                             │
            ▼                             ▼
    ┌───────────────┐                Sign In Again
    │  Has Admin    │                     │
    │  Role?        │◄────────────────────┘
    └───────────────┘
            │
    ┌───────┴───────┐
    │               │
    ▼               ▼
   YES              NO
    │               │
    ▼               ▼
Redirect to    Access Denied
/admin         + Auto Logout
    │               │
    ▼               ▼
Dashboard      Stay on /login
```

### Database Security

**Row Level Security (RLS) Policies:**

```sql
-- Predictions Table
✅ SELECT: Public (anyone can read)
✅ INSERT: Public (anyone can upload)
✅ UPDATE: Authenticated users only
✅ DELETE: Authenticated users only

-- Admin Profiles Table
✅ SELECT: Admins can read all profiles
✅ SELECT: Users can read own profile
✅ UPDATE: Super admins can update any profile
✅ UPDATE: Admins can update own profile (except role)
✅ INSERT: Super admins only
✅ DELETE: Super admins only
```

**Indexes for Performance:**
- User ID lookups
- Role filtering
- Active status filtering
- Email lookups

**Automatic Triggers:**
- Auto-update `updated_at` timestamp
- Auto-create admin profile on signup
- Auto-track last login

---

## 💾 Database Schema

### `admin_profiles` Table

```sql
CREATE TABLE admin_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID UNIQUE NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT NOT NULL,
  email TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'admin' CHECK (role IN ('admin', 'super_admin')),
  is_active BOOLEAN NOT NULL DEFAULT true,
  last_login TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Helper Functions

```sql
-- Update last login timestamp
SELECT update_admin_last_login('user-uuid');

-- Get all active admins
SELECT * FROM get_active_admins();

-- Check if user is admin
SELECT is_user_admin('user-uuid');
```

### Views

```sql
-- Admin statistics
SELECT * FROM admin_stats;
```

---

## 🛠️ Common Operations

### Create Admin User

**Via Supabase UI:**
```
1. Authentication → Users → Add User
2. Set email and password
3. Auto confirm user
4. Edit user → User Metadata
5. Add: {"role": "admin", "full_name": "Name"}
```

**Via SQL:**
```sql
-- After user signs up
UPDATE auth.users 
SET raw_user_meta_data = raw_user_meta_data || '{"role": "admin"}'::jsonb
WHERE email = 'user@example.com';
```

### Promote to Super Admin

```sql
UPDATE admin_profiles 
SET role = 'super_admin' 
WHERE email = 'admin@fito.com';
```

### Deactivate Admin

```sql
UPDATE admin_profiles 
SET is_active = false 
WHERE email = 'admin@fito.com';
```

### View All Admins

```sql
SELECT 
  full_name,
  email,
  role,
  is_active,
  last_login,
  created_at
FROM admin_profiles
ORDER BY created_at DESC;
```

### Get Admin Statistics

```sql
SELECT * FROM admin_stats;

-- Returns:
-- total_admins: Total number of admins
-- active_admins: Currently active admins
-- super_admins: Number of super admins
-- active_last_week: Admins who logged in last 7 days
-- active_last_month: Admins who logged in last 30 days
```

---

## 🧪 Testing

### Test Sign-In Flow

```bash
# 1. Start frontend
cd frontend && npm run dev

# 2. Navigate to login
http://localhost:3000/login

# 3. Enter credentials
Email: admin@fito.com
Password: your-password

# 4. Click "Sign In"
# Expected: Redirect to /admin dashboard

# 5. Verify dashboard loads
# Expected: See statistics and category cards
```

### Test Sign-Up Flow

```bash
# 1. Navigate to login
http://localhost:3000/login

# 2. Click "Don't have an account? Sign Up"

# 3. Fill form
Full Name: Test Admin
Email: test@example.com
Password: password123
Confirm Password: password123

# 4. Click "Sign Up"
# Expected: Success message

# 5. Check email
# Expected: Verification email from Supabase

# 6. Click verification link
# Expected: Email confirmed

# 7. Add admin role via Supabase UI

# 8. Sign in
# Expected: Redirect to /admin dashboard
```

### Test Access Control

```bash
# 1. Without logging in, try to access:
http://localhost:3000/admin
# Expected: Redirect to /login

# 2. Sign in with non-admin account
# Expected: "Access denied" error

# 3. Sign in with admin account
# Expected: Access granted to dashboard

# 4. Try to access admin routes
http://localhost:3000/admin/dataset
# Expected: Access granted (if admin)
```

---

## 🐛 Troubleshooting

### Issue: 404 Page Not Found

**Symptoms:**
- Clicking "Log-in" shows 404 error
- `/login` route not found

**Solution:**
```bash
# 1. Verify file exists
ls frontend/src/app/login/page.tsx

# 2. Clear Next.js cache
cd frontend
rm -rf .next

# 3. Restart dev server
npm run dev

# 4. Clear browser cache
Ctrl + Shift + R (Windows/Linux)
Cmd + Shift + R (Mac)
```

### Issue: Access Denied

**Symptoms:**
- "Access denied. Admin privileges required."
- Redirected back to login after signing in

**Solution:**
```sql
-- 1. Check user metadata
SELECT email, raw_user_meta_data 
FROM auth.users 
WHERE email = 'your@email.com';

-- 2. Add admin role if missing
UPDATE auth.users 
SET raw_user_meta_data = raw_user_meta_data || '{"role": "admin"}'::jsonb
WHERE email = 'your@email.com';

-- 3. Verify admin profile exists
SELECT * FROM admin_profiles WHERE email = 'your@email.com';

-- 4. Create profile if missing
INSERT INTO admin_profiles (user_id, full_name, email, role)
SELECT id, raw_user_meta_data->>'full_name', email, 'admin'
FROM auth.users WHERE email = 'your@email.com';
```

### Issue: Profile Not Created

**Symptoms:**
- User can sign in but no profile in `admin_profiles`
- Dashboard shows errors

**Solution:**
```sql
-- 1. Check if trigger exists
SELECT tgname FROM pg_trigger WHERE tgname = 'on_auth_user_created_create_admin_profile';

-- 2. Manually create profile
INSERT INTO admin_profiles (user_id, full_name, email, role)
SELECT 
  id, 
  COALESCE(raw_user_meta_data->>'full_name', 'Admin User'),
  email,
  'admin'
FROM auth.users 
WHERE email = 'your@email.com'
ON CONFLICT (user_id) DO NOTHING;
```

### Issue: Can't Access Dashboard

**Symptoms:**
- Login successful but dashboard won't load
- Blank page or errors

**Solution:**
```bash
# 1. Check environment variables
cat frontend/.env.local

# Should have:
# NEXT_PUBLIC_SUPABASE_URL=...
# NEXT_PUBLIC_SUPABASE_ANON_KEY=...

# 2. Check browser console
# Open DevTools (F12) → Console
# Look for authentication errors

# 3. Verify Supabase connection
# Go to Supabase Dashboard → API Settings
# Confirm URL and anon key match .env.local

# 4. Check RLS policies
# Go to Supabase → Database → Tables → predictions
# Verify RLS is enabled and policies exist
```

---

## 📊 Monitoring

### Admin Activity

```sql
-- Recently active admins
SELECT 
  full_name,
  email,
  last_login,
  EXTRACT(EPOCH FROM (NOW() - last_login))/3600 as hours_since_login
FROM admin_profiles
WHERE is_active = true
ORDER BY last_login DESC;

-- Inactive admins (no login in 30 days)
SELECT 
  full_name,
  email,
  last_login,
  created_at
FROM admin_profiles
WHERE 
  is_active = true
  AND (last_login IS NULL OR last_login < NOW() - INTERVAL '30 days')
ORDER BY created_at DESC;
```

### System Statistics

```sql
-- Admin overview
SELECT * FROM admin_stats;

-- User growth
SELECT 
  DATE(created_at) as signup_date,
  COUNT(*) as new_admins
FROM admin_profiles
GROUP BY DATE(created_at)
ORDER BY signup_date DESC
LIMIT 30;
```

---

## 📚 Related Documentation

- **[ADMIN_SETUP_GUIDE.md](ADMIN_SETUP_GUIDE.md)** - Complete setup instructions
- **[LOGIN_QUICK_REFERENCE.md](LOGIN_QUICK_REFERENCE.md)** - Quick reference card
- **[DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)** - Database documentation
- **[SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)** - System overview
- **[ADMIN_DASHBOARD_README.md](ADMIN_DASHBOARD_README.md)** - Dashboard features

---

## 🔄 Updates and Maintenance

### Regular Tasks

**Weekly:**
- Review admin activity logs
- Check for inactive accounts
- Monitor login attempts

**Monthly:**
- Audit admin permissions
- Review super admin list
- Update security policies

**As Needed:**
- Create new admin accounts
- Deactivate old accounts
- Promote/demote users

---

## 🆘 Support

If you need help:

1. **Check Documentation**: Review guides above
2. **Check Logs**: Supabase Dashboard → Logs
3. **Check Console**: Browser DevTools → Console
4. **Verify Setup**: Run verification queries
5. **Check Environment**: Verify .env.local settings

---

## 📝 Changelog

### Version 1.0.0 (November 1, 2025)
- ✅ Initial release
- ✅ Sign-in/Sign-up page created
- ✅ Admin profiles database schema
- ✅ Role-based access control
- ✅ Automatic profile creation
- ✅ Last login tracking
- ✅ Minimalist UI design
- ✅ Complete documentation

---

**Last Updated**: November 1, 2025  
**Version**: 1.0.0  
**Status**: Production Ready ✅

