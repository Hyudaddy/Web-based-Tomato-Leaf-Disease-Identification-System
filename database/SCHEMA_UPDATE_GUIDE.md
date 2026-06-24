# FITO Database Schema Update Guide

## Overview
This guide explains the updated database schema to support the enhanced login/signup components with first name, last name, and comprehensive user profile management.

## What Changed

### 1. New User Profiles Table
A new `user_profiles` table has been created to store user information from the enhanced signup form.

**Location:** `database/user_profiles_schema.sql`

### 2. Enhanced Signup Form Fields
The signup form now collects:
- **First Name** (required)
- **Last Name** (required)
- **Email** (required)
- **Password** (required)
- **Confirm Password** (required)

These are stored in the user's authentication metadata and synced to the `user_profiles` table.

## Database Schema

### User Profiles Table

```sql
CREATE TABLE user_profiles (
  id UUID PRIMARY KEY,
  user_id UUID UNIQUE REFERENCES auth.users(id),
  first_name TEXT,
  last_name TEXT,
  full_name TEXT,           -- Auto-generated from first + last
  email TEXT NOT NULL,
  role TEXT DEFAULT 'user', -- user, admin, super_admin
  is_active BOOLEAN DEFAULT true,
  email_verified BOOLEAN DEFAULT false,
  last_login TIMESTAMPTZ,
  created_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ
);
```

### Key Features

#### 1. **Automatic Full Name Generation**
- Full name is automatically generated from first_name + last_name
- Trigger: `generate_user_full_name()`
- Updates whenever first or last name changes

#### 2. **Automatic Profile Creation**
- When a user signs up, a profile is automatically created
- Trigger: `on_auth_user_created_create_user_profile()`
- Extracts data from auth user metadata

#### 3. **Last Login Tracking**
- Function: `update_user_last_login(user_id)`
- Call this after successful login to track user activity

#### 4. **Email Verification Tracking**
- `email_verified` column tracks if user has verified their email
- Update when user confirms their email

#### 5. **Role Management**
- Supports three roles: `user`, `admin`, `super_admin`
- Default role is `user`
- Admins can manage user roles

## Setup Instructions

### Step 1: Run the Schema Script
1. Go to Supabase Dashboard → SQL Editor
2. Copy the contents of `database/user_profiles_schema.sql`
3. Paste and execute in the SQL editor
4. Verify the schema was created successfully

### Step 2: Verify the Setup
Run these verification queries in Supabase SQL Editor:

```sql
-- Check user_profiles table
SELECT * FROM information_schema.columns 
WHERE table_name = 'user_profiles';

-- Check user statistics
SELECT * FROM user_stats;

-- Check active users
SELECT * FROM get_active_users();
```

### Step 3: Update Your Application
The login component has been updated to:
- Collect first name and last name during signup
- Store these in user metadata
- Automatically create user profile via trigger

## API Functions

### Get Active Users
```sql
SELECT * FROM get_active_users();
```
Returns all active users with their profile information.

### Check if User is Active
```sql
SELECT is_user_active('user-id-here'::uuid);
```
Returns true if user is active, false otherwise.

### Update Last Login
```sql
SELECT update_user_last_login('user-id-here'::uuid);
```
Updates the last login timestamp for a user.

### Get User Statistics
```sql
SELECT * FROM user_stats;
```
Returns overall user statistics including:
- Total users
- Active users
- Verified users
- Admin counts
- Activity metrics

## Frontend Integration

### Signup Flow
```typescript
// User fills form with:
// - firstName
// - lastName
// - email
// - password

const { data, error } = await supabase.auth.signUp({
  email,
  password,
  options: {
    data: {
      first_name: firstName,
      last_name: lastName,
      full_name: `${firstName} ${lastName}`,
      role: 'user'
    }
  }
})
```

### Login Flow
```typescript
// After successful login, update last login
const { data, error } = await supabase.auth.signInWithPassword({
  email,
  password
})

if (!error && data.user) {
  // Update last login timestamp
  await supabase.rpc('update_user_last_login', {
    user_id_param: data.user.id
  })
}
```

## Row Level Security (RLS)

### Policies Implemented

1. **Users can read their own profile**
   - Users can only see their own profile data

2. **Admins can read all profiles**
   - Admins and super_admins can view all user profiles

3. **Users can update their own profile**
   - Users can update their own profile (except role)
   - Role can only be changed by admins

4. **Admins can update profiles**
   - Admins can update any user profile

## Indexes for Performance

The following indexes are created for optimal query performance:

- `idx_user_profiles_user_id` - Fast user lookups
- `idx_user_profiles_role` - Filter by role
- `idx_user_profiles_active` - Filter active users
- `idx_user_profiles_email` - Email lookups
- `idx_user_profiles_email_verified` - Filter verified users
- `idx_user_profiles_active_role` - Combined active + role queries

## Migration from Old Schema

If you have existing users:

1. **Existing auth users will still work**
   - They won't have user_profiles entries initially
   - Create profiles manually or via admin interface

2. **New signups will auto-create profiles**
   - The trigger handles this automatically

3. **To migrate existing users:**
   ```sql
   INSERT INTO user_profiles (user_id, email, role)
   SELECT id, email, 'user'
   FROM auth.users
   WHERE id NOT IN (SELECT user_id FROM user_profiles)
   ON CONFLICT (user_id) DO NOTHING;
   ```

## Troubleshooting

### Profile not created after signup?
- Check if the trigger is enabled: `SELECT * FROM pg_trigger WHERE tgname = 'on_auth_user_created_create_user_profile';`
- Verify user metadata was stored correctly in auth.users table

### Full name not generating?
- Check if the trigger is enabled: `SELECT * FROM pg_trigger WHERE tgname = 'generate_user_full_name';`
- Verify first_name and last_name are being stored

### RLS blocking access?
- Check if user has correct role in user_profiles table
- Verify RLS policies are correctly configured

## Best Practices

1. **Always use the user_id from auth.users**
   - Don't rely on email as primary identifier

2. **Update last_login on every login**
   - Helps track user activity

3. **Verify email before granting permissions**
   - Set email_verified = true after email confirmation

4. **Use the user_stats view for dashboards**
   - Provides aggregated user metrics

5. **Keep role management centralized**
   - Only admins should change user roles

## Related Files

- **Frontend:** `frontend/src/app/login/page.tsx`
- **Schema:** `database/user_profiles_schema.sql`
- **Admin Profiles:** `database/admin_profiles_schema.sql`
- **Predictions:** `database/supabase_schema.sql`

## Support

For issues or questions:
1. Check the verification queries above
2. Review the RLS policies
3. Check browser console for auth errors
4. Check Supabase logs for database errors
