# 🔐 Fito Admin Authentication Setup Guide

## Overview

This guide will help you set up the complete admin authentication system for the Fito Tomato Leaf Disease Identification System. The system now includes:

- ✅ **Sign-In/Sign-Up Page** at `/login` (minimalist design matching the site style)
- ✅ **Admin Profiles Database** for managing admin users
- ✅ **Role-Based Access Control** (admin and super_admin roles)
- ✅ **Automatic Profile Creation** when users sign up with admin role
- ✅ **Last Login Tracking** for security monitoring

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Run the Main Database Schema (if not done already)

1. Open file: **`supabase_schema.sql`**
2. Copy ALL the SQL code
3. Go to: https://supabase.com/dashboard/project/frzxrohhhpvbgwxnisww/sql
4. Paste into SQL Editor
5. Click **"Run"**

### Step 2: Run the Admin Profiles Schema

1. Open file: **`admin_profiles_schema.sql`**
2. Copy ALL the SQL code
3. Go to: https://supabase.com/dashboard/project/frzxrohhhpvbgwxnisww/sql
4. Paste into SQL Editor
5. Click **"Run"**
6. ✅ Database setup complete!

### Step 3: Create Your First Admin User

#### Option A: Via Supabase UI (Recommended)

1. Go to **Authentication** → **Users** in Supabase Dashboard
2. Click **"Add user"**
3. Fill in:
   - **Email**: `admin@fito.com` (or your preferred email)
   - **Password**: Choose a strong password
   - **Auto Confirm User**: ✅ Check this box
4. Click **"Create user"**
5. After creation, click on the user to edit
6. Scroll to **User Metadata** section
7. Click **"Edit"** and add:
   ```json
   {
     "role": "admin",
     "full_name": "Admin User"
   }
   ```
8. Click **"Save"**
9. ✅ Admin profile will be created automatically via database trigger!

#### Option B: Via Sign-Up Page

1. Go to: `http://localhost:3000/login`
2. Click **"Don't have an account? Sign Up"**
3. Fill in the form:
   - **Full Name**: Your name
   - **Email**: Your email
   - **Password**: Choose a strong password
   - **Confirm Password**: Re-enter password
4. Click **"Sign Up"**
5. Check your email and verify your account
6. **Manually add admin role** via Supabase UI:
   - Go to Authentication → Users
   - Find your user
   - Edit User Metadata and add: `{"role": "admin"}`
7. ✅ Admin profile will be created automatically!

### Step 4: Create Super Admin (Optional)

If you want to create a super admin with elevated privileges:

1. First, create a regular admin user (follow Step 3)
2. Go to Supabase SQL Editor
3. Run this query:
   ```sql
   UPDATE admin_profiles 
   SET role = 'super_admin' 
   WHERE email = 'admin@fito.com';
   ```
4. ✅ Super admin created!

---

## 📋 Database Tables

### `admin_profiles` Table

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Unique identifier |
| `user_id` | UUID | Foreign key to auth.users |
| `full_name` | TEXT | Full name of admin |
| `email` | TEXT | Email address |
| `role` | TEXT | 'admin' or 'super_admin' |
| `is_active` | BOOLEAN | Account active status |
| `last_login` | TIMESTAMPTZ | Last login timestamp |
| `created_at` | TIMESTAMPTZ | Profile creation date |
| `updated_at` | TIMESTAMPTZ | Last update timestamp |

---

## 🔒 Security Features

### Role-Based Access Control

- **Regular Admin**:
  - Can view dashboard
  - Can manage dataset (view, edit, delete predictions)
  - Can update own profile
  - Cannot create/delete other admins

- **Super Admin**:
  - All regular admin permissions
  - Can create new admin users
  - Can update any admin profile
  - Can delete admin users
  - Can promote/demote admins

### Row Level Security (RLS)

All tables have RLS enabled with the following policies:

- **Read**: Admins can read all admin profiles
- **Update**: Admins can update their own profile; Super admins can update any profile
- **Insert**: Only super admins can create new admin profiles
- **Delete**: Only super admins can delete admin profiles

---

## 🎨 Login Page Features

The new `/login` page includes:

- ✅ **Minimalist Design** - No cards, clean transparent forms matching site style
- ✅ **Sign-In Form** - Email and password authentication
- ✅ **Sign-Up Form** - New user registration with email verification
- ✅ **Form Toggle** - Easy switch between sign-in and sign-up
- ✅ **Error Handling** - Clear error messages for validation
- ✅ **Success Messages** - Confirmation when account is created
- ✅ **Back to Home** - Easy navigation back to main site
- ✅ **Responsive Design** - Works on all devices
- ✅ **Glassmorphism** - Backdrop blur effects matching navbar style

### Design Elements

- Background: Same tomato leaf background as home page
- Forms: Transparent with backdrop blur (white/10 opacity)
- Buttons: Green accent color (#47f793) matching site theme
- Typography: Montserrat font for headings
- Animations: Smooth transitions and hover effects

---

## 🔄 Authentication Flow

```
User clicks "Log-in" in navbar
         ↓
Redirected to /login
         ↓
User chooses Sign-In or Sign-Up
         ↓
    ┌─────────────────┬─────────────────┐
    │    SIGN-IN      │     SIGN-UP     │
    └─────────────────┴─────────────────┘
         ↓                    ↓
Enter credentials      Enter details
         ↓                    ↓
Supabase Auth          Create account
         ↓                    ↓
Check admin role       Email verification
         ↓                    ↓
  ┌──────────────┐      Add admin role
  │ Is Admin?    │      (manually)
  └──────────────┘           ↓
    ↓         ↓              ↓
   Yes        No        Sign in again
    ↓         ↓              ↓
Redirect to  Access      Redirect to
/admin       Denied      /admin
```

---

## 🛠️ Useful SQL Queries

### Get All Active Admins

```sql
SELECT * FROM get_active_admins();
```

### Check if User is Admin

```sql
SELECT is_user_admin('user-uuid-here');
```

### Update Last Login

```sql
SELECT update_admin_last_login('user-uuid-here');
```

### View Admin Statistics

```sql
SELECT * FROM admin_stats;
```

### Manually Create Admin Profile

```sql
INSERT INTO admin_profiles (user_id, full_name, email, role)
VALUES (
  'user-uuid-from-auth-users',
  'Admin Name',
  'admin@example.com',
  'admin'
);
```

### Promote Admin to Super Admin

```sql
UPDATE admin_profiles 
SET role = 'super_admin' 
WHERE email = 'admin@fito.com';
```

### Deactivate Admin Account

```sql
UPDATE admin_profiles 
SET is_active = false 
WHERE email = 'admin@fito.com';
```

### Reactivate Admin Account

```sql
UPDATE admin_profiles 
SET is_active = true 
WHERE email = 'admin@fito.com';
```

---

## 🧪 Testing the Setup

### Test Sign-In

1. Start the frontend: `cd frontend && npm run dev`
2. Go to: `http://localhost:3000/login`
3. Enter admin credentials
4. Click **"Sign In"**
5. Should redirect to `/admin` dashboard

### Test Sign-Up

1. Go to: `http://localhost:3000/login`
2. Click **"Don't have an account? Sign Up"**
3. Fill in the form
4. Click **"Sign Up"**
5. Check email for verification link
6. Verify email
7. Add admin role via Supabase UI
8. Sign in again
9. Should redirect to `/admin` dashboard

### Test Access Control

1. Try accessing `/admin` without logging in
   - Should redirect to `/login`
2. Try logging in with non-admin account
   - Should show "Access denied" error
3. Try logging in with admin account
   - Should successfully access dashboard

---

## 🐛 Troubleshooting

### Issue: "404 Page Not Found" when clicking Log-in

**Solution**: The new `/login` page has been created. Make sure:
- Frontend is running: `npm run dev`
- File exists at: `frontend/src/app/login/page.tsx`
- Clear browser cache and refresh

### Issue: "Access denied. Admin privileges required."

**Solution**: User doesn't have admin role. Fix by:
1. Go to Supabase → Authentication → Users
2. Find the user
3. Edit User Metadata
4. Add: `{"role": "admin"}`
5. Save and try logging in again

### Issue: Admin profile not created automatically

**Solution**: Check if trigger is working:
1. Go to Supabase SQL Editor
2. Run: `SELECT * FROM admin_profiles;`
3. If empty, manually create profile:
   ```sql
   INSERT INTO admin_profiles (user_id, full_name, email, role)
   SELECT id, raw_user_meta_data->>'full_name', email, 'admin'
   FROM auth.users
   WHERE email = 'your-admin@email.com';
   ```

### Issue: Can't see admin dashboard after login

**Solution**: Check AdminLayout.tsx authentication:
1. Open browser console (F12)
2. Look for authentication errors
3. Verify Supabase credentials in `.env.local`
4. Make sure user has admin role in metadata

---

## 📝 Environment Variables

Make sure your `frontend/.env.local` has:

```env
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
```

---

## 🎯 Next Steps

After setup is complete:

1. ✅ Test the login flow
2. ✅ Create your admin users
3. ✅ Set up super admin if needed
4. ✅ Customize admin profiles as needed
5. ✅ Monitor admin activity via `admin_stats` view
6. ✅ Implement additional security features (2FA, IP whitelist, etc.)

---

## 📚 Related Documentation

- **QUICK_START.md** - Quick setup guide for the entire system
- **SUPABASE_SETUP.md** - Detailed Supabase configuration
- **DATABASE_SCHEMA.md** - Complete database schema documentation
- **ADMIN_DASHBOARD_README.md** - Admin dashboard features
- **SYSTEM_ARCHITECTURE.md** - Overall system architecture

---

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review the Supabase logs in the dashboard
3. Check browser console for errors
4. Verify all environment variables are set correctly
5. Ensure database schema is properly created

---

**Last Updated**: November 1, 2025
**Version**: 1.0.0

