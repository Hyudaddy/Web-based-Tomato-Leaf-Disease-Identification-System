-- ============================================================================
-- FITO ADMIN PROFILES - DATABASE SCHEMA EXTENSION
-- ============================================================================
-- This script adds admin profile management to the existing Fito database
-- Run this AFTER running the main supabase_schema.sql
-- Run in Supabase SQL Editor: https://supabase.com/dashboard/project/frzxrohhhpvbgwxnisww/sql
-- ============================================================================

-- ============================================================================
-- 1. CREATE ADMIN PROFILES TABLE
-- ============================================================================
-- This table stores additional information about admin users

CREATE TABLE IF NOT EXISTS admin_profiles (
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

-- Add comments for documentation
COMMENT ON TABLE admin_profiles IS 'Stores admin user profiles and permissions';
COMMENT ON COLUMN admin_profiles.id IS 'Unique identifier for the admin profile';
COMMENT ON COLUMN admin_profiles.user_id IS 'Foreign key to auth.users table';
COMMENT ON COLUMN admin_profiles.full_name IS 'Full name of the admin user';
COMMENT ON COLUMN admin_profiles.email IS 'Email address of the admin user';
COMMENT ON COLUMN admin_profiles.role IS 'Admin role: admin or super_admin';
COMMENT ON COLUMN admin_profiles.is_active IS 'Whether the admin account is active';
COMMENT ON COLUMN admin_profiles.last_login IS 'Timestamp of last login';
COMMENT ON COLUMN admin_profiles.created_at IS 'When the admin profile was created';
COMMENT ON COLUMN admin_profiles.updated_at IS 'When the profile was last updated';

-- ============================================================================
-- 2. CREATE INDEXES FOR ADMIN PROFILES
-- ============================================================================

-- Index for quick user_id lookups
CREATE INDEX IF NOT EXISTS idx_admin_profiles_user_id 
ON admin_profiles(user_id);

-- Index for filtering by role
CREATE INDEX IF NOT EXISTS idx_admin_profiles_role 
ON admin_profiles(role);

-- Index for filtering active admins
CREATE INDEX IF NOT EXISTS idx_admin_profiles_active 
ON admin_profiles(is_active);

-- Index for email lookups
CREATE INDEX IF NOT EXISTS idx_admin_profiles_email 
ON admin_profiles(email);

-- ============================================================================
-- 3. CREATE UPDATED_AT TRIGGER FOR ADMIN PROFILES
-- ============================================================================

CREATE TRIGGER update_admin_profiles_updated_at
    BEFORE UPDATE ON admin_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 4. ENABLE ROW LEVEL SECURITY FOR ADMIN PROFILES
-- ============================================================================

ALTER TABLE admin_profiles ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- 5. CREATE RLS POLICIES FOR ADMIN PROFILES
-- ============================================================================

-- Policy 1: Admins can read all admin profiles
CREATE POLICY "Admins can read all profiles" 
ON admin_profiles
FOR SELECT
USING (
  auth.uid() IN (SELECT user_id FROM admin_profiles WHERE is_active = true)
);

-- Policy 2: Admins can read their own profile
CREATE POLICY "Users can read own profile" 
ON admin_profiles
FOR SELECT
USING (auth.uid() = user_id);

-- Policy 3: Super admins can update any profile
CREATE POLICY "Super admins can update profiles" 
ON admin_profiles
FOR UPDATE
USING (
  EXISTS (
    SELECT 1 FROM admin_profiles 
    WHERE user_id = auth.uid() 
    AND role = 'super_admin' 
    AND is_active = true
  )
);

-- Policy 4: Admins can update their own profile (except role)
CREATE POLICY "Admins can update own profile" 
ON admin_profiles
FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (
  auth.uid() = user_id 
  AND role = (SELECT role FROM admin_profiles WHERE user_id = auth.uid())
);

-- Policy 5: Super admins can insert new admin profiles
CREATE POLICY "Super admins can create profiles" 
ON admin_profiles
FOR INSERT
WITH CHECK (
  EXISTS (
    SELECT 1 FROM admin_profiles 
    WHERE user_id = auth.uid() 
    AND role = 'super_admin' 
    AND is_active = true
  )
);

-- Policy 6: Super admins can delete admin profiles
CREATE POLICY "Super admins can delete profiles" 
ON admin_profiles
FOR DELETE
USING (
  EXISTS (
    SELECT 1 FROM admin_profiles 
    WHERE user_id = auth.uid() 
    AND role = 'super_admin' 
    AND is_active = true
  )
);

-- ============================================================================
-- 6. CREATE FUNCTION TO UPDATE LAST LOGIN
-- ============================================================================

CREATE OR REPLACE FUNCTION update_admin_last_login(admin_user_id UUID)
RETURNS VOID AS $$
BEGIN
  UPDATE admin_profiles
  SET last_login = NOW()
  WHERE user_id = admin_user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION update_admin_last_login IS 'Updates the last login timestamp for an admin user';

-- ============================================================================
-- 7. CREATE FUNCTION TO GET ACTIVE ADMINS
-- ============================================================================

CREATE OR REPLACE FUNCTION get_active_admins()
RETURNS TABLE (
  id UUID,
  full_name TEXT,
  email TEXT,
  role TEXT,
  last_login TIMESTAMPTZ,
  created_at TIMESTAMPTZ
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    ap.id,
    ap.full_name,
    ap.email,
    ap.role,
    ap.last_login,
    ap.created_at
  FROM admin_profiles ap
  WHERE ap.is_active = true
  ORDER BY ap.created_at DESC;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_active_admins IS 'Get all active admin users';

-- ============================================================================
-- 8. CREATE FUNCTION TO CHECK IF USER IS ADMIN
-- ============================================================================

CREATE OR REPLACE FUNCTION is_user_admin(check_user_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM admin_profiles
    WHERE user_id = check_user_id
    AND is_active = true
  );
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION is_user_admin IS 'Check if a user ID belongs to an active admin';

-- ============================================================================
-- 9. CREATE VIEW FOR ADMIN STATISTICS
-- ============================================================================

CREATE OR REPLACE VIEW admin_stats AS
SELECT 
  COUNT(*) as total_admins,
  COUNT(*) FILTER (WHERE is_active = true) as active_admins,
  COUNT(*) FILTER (WHERE role = 'super_admin') as super_admins,
  COUNT(*) FILTER (WHERE last_login > NOW() - INTERVAL '7 days') as active_last_week,
  COUNT(*) FILTER (WHERE last_login > NOW() - INTERVAL '30 days') as active_last_month
FROM admin_profiles;

COMMENT ON VIEW admin_stats IS 'Statistics about admin users';

-- ============================================================================
-- 10. CREATE TRIGGER TO AUTO-CREATE ADMIN PROFILE
-- ============================================================================
-- This trigger automatically creates an admin profile when a user signs up
-- with admin role in their metadata

CREATE OR REPLACE FUNCTION create_admin_profile_on_signup()
RETURNS TRIGGER AS $$
BEGIN
  -- Check if user has admin role in metadata
  IF (NEW.raw_user_meta_data->>'role' = 'admin') THEN
    INSERT INTO admin_profiles (
      user_id,
      full_name,
      email,
      role
    ) VALUES (
      NEW.id,
      COALESCE(NEW.raw_user_meta_data->>'full_name', 'Admin User'),
      NEW.email,
      'admin'
    )
    ON CONFLICT (user_id) DO NOTHING;
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create the trigger
CREATE TRIGGER on_auth_user_created_create_admin_profile
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION create_admin_profile_on_signup();

COMMENT ON FUNCTION create_admin_profile_on_signup IS 'Automatically creates admin profile when user signs up with admin role';

-- ============================================================================
-- 11. VERIFICATION QUERIES
-- ============================================================================

-- Check if admin_profiles table exists
SELECT 
  table_name,
  column_name,
  data_type,
  is_nullable
FROM information_schema.columns
WHERE table_name = 'admin_profiles'
ORDER BY ordinal_position;

-- Check if indexes exist
SELECT 
  indexname,
  indexdef
FROM pg_indexes
WHERE tablename = 'admin_profiles';

-- Check if RLS is enabled
SELECT 
  tablename,
  rowsecurity
FROM pg_tables
WHERE tablename = 'admin_profiles';

-- Check if policies exist
SELECT 
  policyname,
  cmd
FROM pg_policies
WHERE tablename = 'admin_profiles';

-- Get admin statistics
SELECT * FROM admin_stats;

-- ============================================================================
-- SETUP COMPLETE!
-- ============================================================================
-- Next steps:
-- 1. Create your first admin user via Supabase Authentication UI
-- 2. Go to Authentication → Users → Add User
-- 3. Set email and password
-- 4. After creation, edit the user and add to User Metadata:
--    {"role": "admin", "full_name": "Your Name"}
-- 5. The admin profile will be created automatically via trigger
-- 6. For super admin, manually update the role in admin_profiles table:
--    UPDATE admin_profiles SET role = 'super_admin' WHERE email = 'your@email.com';
-- ============================================================================

-- Display success message
DO $$
BEGIN
  RAISE NOTICE '✅ Admin profiles schema created successfully!';
  RAISE NOTICE '📋 Next steps:';
  RAISE NOTICE '   1. Create admin user in Authentication section';
  RAISE NOTICE '   2. Add user metadata: {"role": "admin", "full_name": "Your Name"}';
  RAISE NOTICE '   3. Admin profile will be created automatically';
  RAISE NOTICE '   4. For super admin, update role in admin_profiles table';
END $$;

