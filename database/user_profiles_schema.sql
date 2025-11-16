-- ============================================================================
-- FITO USER PROFILES - DATABASE SCHEMA EXTENSION
-- ============================================================================
-- This script adds user profile management to the existing Fito database
-- Supports the enhanced login/signup components with first name, last name, etc.
-- Run this AFTER running the main supabase_schema.sql
-- Run in Supabase SQL Editor: https://supabase.com/dashboard/project/frzxrohhhpvbgwxnisww/sql
-- ============================================================================

-- ============================================================================
-- 1. CREATE USER PROFILES TABLE
-- ============================================================================
-- This table stores user profile information from the enhanced signup form

CREATE TABLE IF NOT EXISTS user_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID UNIQUE NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  first_name TEXT,
  last_name TEXT,
  full_name TEXT,
  email TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin', 'super_admin')),
  is_active BOOLEAN NOT NULL DEFAULT true,
  email_verified BOOLEAN NOT NULL DEFAULT false,
  last_login TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Add comments for documentation
COMMENT ON TABLE user_profiles IS 'Stores user profile information from signup form';
COMMENT ON COLUMN user_profiles.id IS 'Unique identifier for the user profile';
COMMENT ON COLUMN user_profiles.user_id IS 'Foreign key to auth.users table';
COMMENT ON COLUMN user_profiles.first_name IS 'User first name from signup form';
COMMENT ON COLUMN user_profiles.last_name IS 'User last name from signup form';
COMMENT ON COLUMN user_profiles.full_name IS 'User full name (auto-generated from first + last)';
COMMENT ON COLUMN user_profiles.email IS 'Email address of the user';
COMMENT ON COLUMN user_profiles.role IS 'User role: user, admin, or super_admin';
COMMENT ON COLUMN user_profiles.is_active IS 'Whether the user account is active';
COMMENT ON COLUMN user_profiles.email_verified IS 'Whether the user has verified their email';
COMMENT ON COLUMN user_profiles.last_login IS 'Timestamp of last login';
COMMENT ON COLUMN user_profiles.created_at IS 'When the user profile was created';
COMMENT ON COLUMN user_profiles.updated_at IS 'When the profile was last updated';

-- ============================================================================
-- 2. CREATE INDEXES FOR USER PROFILES
-- ============================================================================

-- Index for quick user_id lookups
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id 
ON user_profiles(user_id);

-- Index for filtering by role
CREATE INDEX IF NOT EXISTS idx_user_profiles_role 
ON user_profiles(role);

-- Index for filtering active users
CREATE INDEX IF NOT EXISTS idx_user_profiles_active 
ON user_profiles(is_active);

-- Index for email lookups
CREATE INDEX IF NOT EXISTS idx_user_profiles_email 
ON user_profiles(email);

-- Index for email verification status
CREATE INDEX IF NOT EXISTS idx_user_profiles_email_verified 
ON user_profiles(email_verified);

-- Composite index for common queries (active + role)
CREATE INDEX IF NOT EXISTS idx_user_profiles_active_role 
ON user_profiles(is_active, role);

-- ============================================================================
-- 3. CREATE UPDATED_AT TRIGGER FOR USER PROFILES
-- ============================================================================

DROP TRIGGER IF EXISTS update_user_profiles_updated_at ON user_profiles;
CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- 4. ENABLE ROW LEVEL SECURITY FOR USER PROFILES
-- ============================================================================

ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- 5. CREATE RLS POLICIES FOR USER PROFILES
-- ============================================================================

-- Policy 1: Users can read their own profile
CREATE POLICY "Users can read own profile" 
ON user_profiles
FOR SELECT
USING (auth.uid() = user_id);

-- Policy 2: Admins can read all user profiles
CREATE POLICY "Admins can read all profiles" 
ON user_profiles
FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM user_profiles 
    WHERE user_id = auth.uid() 
    AND role IN ('admin', 'super_admin')
    AND is_active = true
  )
);

-- Policy 3: Users can update their own profile
CREATE POLICY "Users can update own profile" 
ON user_profiles
FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (
  auth.uid() = user_id 
  AND role = (SELECT role FROM user_profiles WHERE user_id = auth.uid())
);

-- Policy 4: Admins can update user profiles
CREATE POLICY "Admins can update profiles" 
ON user_profiles
FOR UPDATE
USING (
  EXISTS (
    SELECT 1 FROM user_profiles 
    WHERE user_id = auth.uid() 
    AND role IN ('admin', 'super_admin')
    AND is_active = true
  )
);

-- ============================================================================
-- 6. CREATE FUNCTION TO GENERATE FULL NAME
-- ============================================================================

CREATE OR REPLACE FUNCTION generate_full_name()
RETURNS TRIGGER AS $$
BEGIN
  -- Generate full_name from first_name and last_name
  IF NEW.first_name IS NOT NULL AND NEW.last_name IS NOT NULL THEN
    NEW.full_name := NEW.first_name || ' ' || NEW.last_name;
  ELSIF NEW.first_name IS NOT NULL THEN
    NEW.full_name := NEW.first_name;
  ELSIF NEW.last_name IS NOT NULL THEN
    NEW.full_name := NEW.last_name;
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to auto-generate full_name
CREATE TRIGGER generate_user_full_name
    BEFORE INSERT OR UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION generate_full_name();

COMMENT ON FUNCTION generate_full_name IS 'Automatically generates full_name from first_name and last_name';

-- ============================================================================
-- 7. CREATE FUNCTION TO UPDATE LAST LOGIN
-- ============================================================================

CREATE OR REPLACE FUNCTION update_user_last_login(user_id_param UUID)
RETURNS VOID AS $$
BEGIN
  UPDATE user_profiles
  SET last_login = NOW()
  WHERE user_id = user_id_param;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION update_user_last_login IS 'Updates the last login timestamp for a user';

-- ============================================================================
-- 8. CREATE FUNCTION TO GET ACTIVE USERS
-- ============================================================================

CREATE OR REPLACE FUNCTION get_active_users()
RETURNS TABLE (
  id UUID,
  first_name TEXT,
  last_name TEXT,
  full_name TEXT,
  email TEXT,
  role TEXT,
  last_login TIMESTAMPTZ,
  created_at TIMESTAMPTZ
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    up.id,
    up.first_name,
    up.last_name,
    up.full_name,
    up.email,
    up.role,
    up.last_login,
    up.created_at
  FROM user_profiles up
  WHERE up.is_active = true
  ORDER BY up.created_at DESC;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_active_users IS 'Get all active users with their profile information';

-- ============================================================================
-- 9. CREATE FUNCTION TO CHECK IF USER EXISTS
-- ============================================================================

CREATE OR REPLACE FUNCTION is_user_active(check_user_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM user_profiles
    WHERE user_id = check_user_id
    AND is_active = true
  );
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION is_user_active IS 'Check if a user ID belongs to an active user';

-- ============================================================================
-- 10. CREATE VIEW FOR USER STATISTICS
-- ============================================================================

CREATE OR REPLACE VIEW user_stats AS
SELECT 
  COUNT(*) as total_users,
  COUNT(*) FILTER (WHERE is_active = true) as active_users,
  COUNT(*) FILTER (WHERE email_verified = true) as verified_users,
  COUNT(*) FILTER (WHERE role = 'admin') as admin_users,
  COUNT(*) FILTER (WHERE role = 'super_admin') as super_admin_users,
  COUNT(*) FILTER (WHERE last_login > NOW() - INTERVAL '7 days') as active_last_week,
  COUNT(*) FILTER (WHERE last_login > NOW() - INTERVAL '30 days') as active_last_month,
  COUNT(*) FILTER (WHERE created_at > NOW() - INTERVAL '30 days') as new_users_last_month
FROM user_profiles;

COMMENT ON VIEW user_stats IS 'Statistics about user accounts';

-- ============================================================================
-- 11. CREATE TRIGGER TO AUTO-CREATE USER PROFILE ON SIGNUP
-- ============================================================================
-- This trigger automatically creates a user profile when a user signs up

CREATE OR REPLACE FUNCTION create_user_profile_on_signup()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO user_profiles (
    user_id,
    first_name,
    last_name,
    email,
    role
  ) VALUES (
    NEW.id,
    NEW.raw_user_meta_data->>'first_name',
    NEW.raw_user_meta_data->>'last_name',
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'role', 'user')
  )
  ON CONFLICT (user_id) DO NOTHING;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create the trigger
CREATE TRIGGER on_auth_user_created_create_user_profile
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION create_user_profile_on_signup();

COMMENT ON FUNCTION create_user_profile_on_signup IS 'Automatically creates user profile when user signs up';

-- ============================================================================
-- 12. VERIFICATION QUERIES
-- ============================================================================

-- Check if user_profiles table exists
SELECT 
  table_name,
  column_name,
  data_type,
  is_nullable
FROM information_schema.columns
WHERE table_name = 'user_profiles'
ORDER BY ordinal_position;

-- Check if indexes exist
SELECT 
  indexname,
  indexdef
FROM pg_indexes
WHERE tablename = 'user_profiles';

-- Check if RLS is enabled
SELECT 
  tablename,
  rowsecurity
FROM pg_tables
WHERE tablename = 'user_profiles';

-- Check if policies exist
SELECT 
  policyname,
  cmd
FROM pg_policies
WHERE tablename = 'user_profiles';

-- Get user statistics
SELECT * FROM user_stats;

-- ============================================================================
-- SETUP COMPLETE!
-- ============================================================================
-- Next steps:
-- 1. Users can now sign up with first name and last name
-- 2. User profiles are automatically created on signup
-- 3. Full name is automatically generated from first + last name
-- 4. Admin can manage user roles and status
-- 5. User statistics are available via user_stats view
-- ============================================================================

-- Display success message
DO $$
BEGIN
  RAISE NOTICE '✅ User profiles schema created successfully!';
  RAISE NOTICE '📋 Features:';
  RAISE NOTICE '   • User profiles with first/last name support';
  RAISE NOTICE '   • Automatic full name generation';
  RAISE NOTICE '   • Email verification tracking';
  RAISE NOTICE '   • Last login tracking';
  RAISE NOTICE '   • User statistics view';
  RAISE NOTICE '   • Automatic profile creation on signup';
END $$;
