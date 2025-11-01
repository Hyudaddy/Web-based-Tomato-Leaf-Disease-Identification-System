# 🔐 Login System - Quick Reference

## 🚀 5-Minute Setup

### 1. Run Database Schemas

```bash
# In Supabase SQL Editor (https://supabase.com/dashboard/project/YOUR_PROJECT/sql)

# First, run supabase_schema.sql (if not done)
# Then, run admin_profiles_schema.sql
```

### 2. Create First Admin

**Via Supabase UI:**
1. Authentication → Users → Add User
2. Email: `admin@fito.com`
3. Password: Your choice
4. Auto Confirm: ✅
5. After creation → Edit User
6. User Metadata: `{"role": "admin", "full_name": "Admin User"}`
7. Save ✅

### 3. Test Login

```bash
# Start frontend
cd frontend
npm run dev

# Visit http://localhost:3000/login
# Sign in with your admin credentials
# Should redirect to /admin dashboard
```

---

## 📍 Routes

| Route | Description | Access |
|-------|-------------|--------|
| `/login` | Sign-in/Sign-up page | Public |
| `/admin` | Admin dashboard | Admin only |
| `/admin/login` | Old admin login (still works) | Public |
| `/admin/dataset` | Dataset management | Admin only |

---

## 🎨 Login Page Features

### Sign-In Form
- Email input
- Password input
- Error messages
- Loading state
- Auto-redirect to /admin on success

### Sign-Up Form
- Full name input
- Email input
- Password input
- Confirm password input
- Password validation (min 6 chars)
- Email verification required
- Success message
- Auto-switch to sign-in after 3s

### Design
- ✅ Minimalist (no cards)
- ✅ Glassmorphism effects
- ✅ Matches site style
- ✅ Responsive
- ✅ Smooth animations
- ✅ Green accent (#47f793)
- ✅ Tomato leaf background

---

## 🔑 Admin Roles

### Regular Admin
- View dashboard
- Manage dataset
- Update own profile
- Cannot manage other admins

### Super Admin
- All admin permissions
- Create/delete admins
- Update any profile
- Promote/demote admins

**To create super admin:**
```sql
UPDATE admin_profiles 
SET role = 'super_admin' 
WHERE email = 'admin@fito.com';
```

---

## 🛠️ Common Tasks

### Create Admin User
```sql
-- After user signs up, add admin role
UPDATE auth.users 
SET raw_user_meta_data = raw_user_meta_data || '{"role": "admin"}'::jsonb
WHERE email = 'user@example.com';
```

### Check Admin Status
```sql
SELECT * FROM admin_profiles WHERE email = 'admin@fito.com';
```

### View All Admins
```sql
SELECT * FROM get_active_admins();
```

### Deactivate Admin
```sql
UPDATE admin_profiles SET is_active = false WHERE email = 'admin@fito.com';
```

### Update Last Login
```sql
SELECT update_admin_last_login('user-uuid');
```

---

## 🐛 Quick Fixes

### "404 Page Not Found"
- File created at: `frontend/src/app/login/page.tsx`
- Clear cache: Ctrl+Shift+R
- Restart dev server

### "Access Denied"
- Check user metadata has `{"role": "admin"}`
- Verify email is confirmed
- Check admin_profiles table exists

### Profile Not Created
```sql
-- Manually create profile
INSERT INTO admin_profiles (user_id, full_name, email, role)
SELECT id, raw_user_meta_data->>'full_name', email, 'admin'
FROM auth.users WHERE email = 'your@email.com';
```

### Can't Access Dashboard
- Check `.env.local` has Supabase credentials
- Verify RLS policies are created
- Check browser console for errors

---

## 📊 Database Tables

### `admin_profiles`
```
id              UUID        Primary key
user_id         UUID        → auth.users(id)
full_name       TEXT        Admin's name
email           TEXT        Admin's email
role            TEXT        'admin' or 'super_admin'
is_active       BOOLEAN     Account status
last_login      TIMESTAMP   Last login time
created_at      TIMESTAMP   Profile created
updated_at      TIMESTAMP   Last update
```

### Indexes
- `idx_admin_profiles_user_id`
- `idx_admin_profiles_role`
- `idx_admin_profiles_active`
- `idx_admin_profiles_email`

---

## 🔒 Security

### RLS Policies
- ✅ Admins can read all profiles
- ✅ Users can read own profile
- ✅ Super admins can update any profile
- ✅ Admins can update own profile
- ✅ Super admins can create/delete profiles

### Authentication Flow
```
User → /login → Sign In → Check Role → Redirect
                  ↓
              Is Admin? → Yes → /admin
                  ↓
                 No → Access Denied
```

---

## 📝 Environment Setup

**frontend/.env.local**
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

---

## ✅ Checklist

- [ ] Run `supabase_schema.sql`
- [ ] Run `admin_profiles_schema.sql`
- [ ] Create admin user in Supabase
- [ ] Add admin role to user metadata
- [ ] Test sign-in at `/login`
- [ ] Verify redirect to `/admin`
- [ ] Test sign-up flow
- [ ] Create super admin (optional)
- [ ] Test dashboard access
- [ ] Test dataset management

---

## 🎯 Testing

```bash
# 1. Start frontend
cd frontend && npm run dev

# 2. Visit login page
http://localhost:3000/login

# 3. Test sign-in
Email: admin@fito.com
Password: your-password

# 4. Should redirect to
http://localhost:3000/admin

# 5. Test sign-up
Click "Don't have an account? Sign Up"
Fill form → Submit → Check email

# 6. Test access control
Logout → Try accessing /admin directly
Should redirect to /login
```

---

## 📚 Files Created

```
frontend/src/app/login/page.tsx          ← New login page
admin_profiles_schema.sql                 ← Database schema
ADMIN_SETUP_GUIDE.md                      ← Full guide
LOGIN_QUICK_REFERENCE.md                  ← This file
```

---

## 🆘 Need Help?

1. Check **ADMIN_SETUP_GUIDE.md** for detailed instructions
2. Review **Troubleshooting** section in setup guide
3. Check Supabase logs in dashboard
4. Verify all SQL scripts ran successfully
5. Check browser console for errors

---

**Quick Links:**
- [Full Setup Guide](ADMIN_SETUP_GUIDE.md)
- [Database Schema](DATABASE_SCHEMA.md)
- [System Architecture](SYSTEM_ARCHITECTURE.md)
- [Supabase Dashboard](https://supabase.com/dashboard)

---

**Last Updated**: November 1, 2025

