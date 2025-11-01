# 🔧 Login Error Troubleshooting - 400 Bad Request

## ⚠️ Error: POST /auth/v1/token 400 (Bad Request)

This error occurs when trying to sign in. Here are the most common causes and fixes:

---

## 🔍 Common Causes

### 1. **Email Not Confirmed** ⭐ Most Common
Supabase requires email confirmation by default.

**Fix:**
```
1. Go to Supabase Dashboard
2. Authentication → Users
3. Find your user
4. Check if "Email Confirmed" shows a checkmark ✅
5. If not, click the user and manually confirm
```

**Or disable email confirmation (for development):**
```
1. Go to Authentication → Settings
2. Scroll to "Email Auth"
3. Toggle OFF "Enable email confirmations"
4. Save
5. Try signing in again
```

### 2. **Wrong Email/Password Format**
Check that:
- Email is valid format (e.g., `admin@fito.com`)
- Password meets minimum requirements (6+ characters)
- No extra spaces in email/password

### 3. **User Doesn't Exist**
Verify the user exists in Supabase:
```
1. Go to Authentication → Users
2. Check if your email is listed
3. If not, create the user first
```

### 4. **Email Provider Settings**
Some email providers are blocked by default.

**Fix:**
```
1. Go to Authentication → Settings
2. Check "Email Provider Settings"
3. Make sure your domain isn't blocked
```

---

## ✅ Step-by-Step Fix

### **Step 1: Verify User Exists**

Go to: https://supabase.com/dashboard/project/frzxrohhhpvbgwxnisww/auth/users

Check if your admin user is listed.

### **Step 2: Confirm Email**

**Option A: Auto-Confirm on Creation**
1. When creating user, check **"Auto Confirm User"** ✅
2. This bypasses email verification

**Option B: Manually Confirm Existing User**
1. Click on the user in the list
2. Look for "Email Confirmed" field
3. If it shows ❌, manually confirm it

**Option C: Disable Email Confirmation (Development Only)**
1. Go to: https://supabase.com/dashboard/project/frzxrohhhpvbgwxnisww/auth/settings
2. Scroll to **"Email Auth"** section
3. Find **"Enable email confirmations"**
4. Toggle it **OFF**
5. Click **"Save"**
6. Try logging in again

### **Step 3: Check User Status**

In the user details, verify:
- ✅ Email Confirmed
- ✅ User is not banned
- ✅ Email is correct

### **Step 4: Test with Correct Credentials**

Make sure you're using:
- The exact email you created
- The exact password you set
- No extra spaces

---

## 🧪 Test User Creation

### **Create a Test Admin User (Properly)**

1. Go to: https://supabase.com/dashboard/project/frzxrohhhpvbgwxnisww/auth/users

2. Click **"Add user"**

3. Fill in:
   ```
   Email: admin@fito.com
   Password: Admin123!
   Auto Confirm User: ✅ CHECK THIS BOX
   ```

4. Click **"Create user"**

5. After creation, click on the user

6. Click **"Edit"** on User Metadata

7. Add:
   ```json
   {
     "role": "admin",
     "full_name": "Admin User"
   }
   ```

8. Click **"Save"**

9. Now try logging in:
   ```
   Email: admin@fito.com
   Password: Admin123!
   ```

---

## 🔍 Debugging Steps

### **Check Browser Console**

1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for detailed error message
4. Common errors:
   - `Invalid login credentials` = Wrong email/password
   - `Email not confirmed` = Need to confirm email
   - `User not found` = User doesn't exist

### **Check Network Tab**

1. Open DevTools (F12)
2. Go to Network tab
3. Try logging in
4. Click on the failed request
5. Check the Response:
   ```json
   {
     "error": "Invalid login credentials",
     "error_description": "Email not confirmed"
   }
   ```

---

## 🛠️ Quick Fixes

### **Fix 1: Disable Email Confirmation (Fastest)**

```bash
# For development, disable email confirmation:
# 1. Supabase Dashboard → Authentication → Settings
# 2. Email Auth → Enable email confirmations → OFF
# 3. Save
```

### **Fix 2: Auto-Confirm All New Users**

```bash
# When creating users, always check:
# ✅ Auto Confirm User
```

### **Fix 3: Manually Confirm Existing User**

```sql
-- Run in Supabase SQL Editor:
UPDATE auth.users 
SET email_confirmed_at = NOW()
WHERE email = 'admin@fito.com';
```

### **Fix 4: Reset User Password**

```bash
# In Supabase Dashboard:
# 1. Authentication → Users
# 2. Click user
# 3. Click "Send Password Recovery"
# 4. Or manually set new password
```

---

## 📋 Checklist

Before trying to log in, verify:

- [ ] User exists in Supabase Authentication → Users
- [ ] Email is confirmed (✅ checkmark)
- [ ] User is not banned
- [ ] Password is correct (6+ characters)
- [ ] Email format is valid
- [ ] "Auto Confirm User" was checked when creating
- [ ] OR "Enable email confirmations" is disabled
- [ ] User has admin role in metadata: `{"role": "admin"}`
- [ ] .env.local has correct Supabase credentials
- [ ] Dev server was restarted after creating .env.local

---

## 🎯 Recommended Setup for Development

### **Best Practice:**

1. **Disable email confirmation** for development:
   - Authentication → Settings → Email Auth
   - Toggle OFF "Enable email confirmations"

2. **Create admin user** with auto-confirm:
   - Check "Auto Confirm User" ✅
   - Set strong password
   - Add admin role metadata

3. **Test immediately** after creation

4. **Re-enable email confirmation** for production

---

## 🔐 Production Setup

For production, keep email confirmation enabled:

1. Set up email templates
2. Configure SMTP settings
3. Test email delivery
4. Users verify via email link
5. Then manually add admin role

---

## 💡 Common Mistakes

### ❌ Wrong:
```
Creating user without "Auto Confirm User" ✅
Trying to login before email is confirmed
Using wrong password
Extra spaces in email/password
```

### ✅ Correct:
```
Check "Auto Confirm User" when creating
OR disable email confirmation for dev
Use exact credentials
No spaces
Verify user exists first
```

---

## 🆘 Still Not Working?

### Try This:

1. **Delete the user** and recreate:
   ```
   Authentication → Users → Click user → Delete
   Then create again with Auto Confirm ✅
   ```

2. **Check Supabase logs**:
   ```
   Logs → Auth Logs
   Look for failed login attempts
   Check error messages
   ```

3. **Test with SQL**:
   ```sql
   -- Check if user exists and is confirmed
   SELECT 
     email, 
     email_confirmed_at,
     banned_until,
     raw_user_meta_data
   FROM auth.users 
   WHERE email = 'admin@fito.com';
   ```

4. **Verify environment variables**:
   ```bash
   # In frontend directory:
   cat .env.local  # Mac/Linux
   type .env.local  # Windows
   ```

---

## 📞 Quick Support

**Most likely fix**: Disable email confirmation

1. Go to: https://supabase.com/dashboard/project/frzxrohhhpvbgwxnisww/auth/settings
2. Find "Enable email confirmations"
3. Toggle OFF
4. Save
5. Try login again

**This should fix 90% of 400 Bad Request errors!**

---

**Last Updated**: November 1, 2025

