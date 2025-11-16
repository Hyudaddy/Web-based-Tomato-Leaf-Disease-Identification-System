# 🔧 Environment Variables Setup

## ⚠️ Error: "supabaseUrl is required"

This error means your `.env.local` file is missing or doesn't have the required Supabase credentials.

---

## 🚀 Quick Fix (2 Minutes)

### Step 1: Get Your Supabase Credentials

1. Go to your Supabase Dashboard: https://supabase.com/dashboard
2. Select your project (or create one if you haven't)
3. Go to **Settings** → **API**
4. You'll see:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **Project API keys** → **anon public** (long string starting with `eyJ...`)

### Step 2: Create `.env.local` File

In your `frontend` directory, create a file named `.env.local`:

```bash
cd frontend
```

**On Windows (PowerShell):**
```powershell
New-Item -Path ".env.local" -ItemType File
```

**On Windows (Command Prompt):**
```cmd
type nul > .env.local
```

**On Mac/Linux:**
```bash
touch .env.local
```

### Step 3: Add Your Credentials

Open `frontend/.env.local` in your text editor and add:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
```

**Replace**:
- `https://your-project.supabase.co` with your actual Project URL
- `your-anon-key-here` with your actual anon public key

### Step 4: Restart Dev Server

```bash
# Stop the server (Ctrl+C)
# Then restart:
npm run dev
```

### Step 5: Test

Visit: http://localhost:3000/login

✅ Should now work without errors!

---

## 📋 Example `.env.local`

```env
# Example (use your actual values)
NEXT_PUBLIC_SUPABASE_URL=https://frzxrohhhpvbgwxnisww.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZyenhyb2hoaHB2Ymd3eG5pc3d3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTg3NTg0MDAsImV4cCI6MjAxNDMzNDQwMH0.example-key-here
```

---

## 🔍 Where to Find Your Credentials

### Visual Guide:

1. **Supabase Dashboard** → https://supabase.com/dashboard
2. Click your project
3. Left sidebar → **Settings** (gear icon)
4. Click **API**
5. Copy:
   - **Project URL** (under "Project URL" section)
   - **anon public** key (under "Project API keys" section)

---

## ⚠️ Important Notes

### Security
- ✅ `.env.local` is already in `.gitignore` (safe)
- ✅ Never commit this file to Git
- ✅ The `anon` key is safe to use in frontend (it's public)
- ❌ Never share your `service_role` key (keep it secret)

### File Location
```
TLDI_system/
└── frontend/
    ├── .env.local          ← Create this file here
    ├── .env.example        ← Template (already created)
    ├── src/
    ├── package.json
    └── ...
```

### Required Variables
```env
NEXT_PUBLIC_SUPABASE_URL       ← Required
NEXT_PUBLIC_SUPABASE_ANON_KEY  ← Required
```

Both must start with `NEXT_PUBLIC_` to be accessible in the browser.

---

## 🐛 Troubleshooting

### Still Getting Error?

**1. Check file name:**
- Must be exactly `.env.local` (with the dot at the start)
- Not `.env.local.txt` or `env.local`

**2. Check file location:**
- Must be in `frontend/` directory
- Not in root or `frontend/src/`

**3. Check variable names:**
- Must be exactly `NEXT_PUBLIC_SUPABASE_URL`
- Must be exactly `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- Case-sensitive!

**4. Check for spaces:**
- No spaces around `=`
- Correct: `NEXT_PUBLIC_SUPABASE_URL=https://...`
- Wrong: `NEXT_PUBLIC_SUPABASE_URL = https://...`

**5. Restart dev server:**
```bash
# Stop with Ctrl+C
npm run dev
```

### Verify It's Working

**Check in browser console (F12):**
```javascript
// Should NOT be undefined
console.log(process.env.NEXT_PUBLIC_SUPABASE_URL)
```

---

## 📝 Complete Setup Checklist

- [ ] Created `.env.local` file in `frontend/` directory
- [ ] Added `NEXT_PUBLIC_SUPABASE_URL` with your project URL
- [ ] Added `NEXT_PUBLIC_SUPABASE_ANON_KEY` with your anon key
- [ ] Saved the file
- [ ] Restarted dev server (`npm run dev`)
- [ ] Tested login page (no errors)
- [ ] Login page loads successfully

---

## 🎯 Quick Copy-Paste Template

Create `frontend/.env.local` with this content (replace with your values):

```env
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-starting-with-eyJ
```

---

## 🆘 Still Need Help?

### Option 1: Check Existing Setup
If you already have a Supabase project set up for this app, check if there's an existing `.env` file or documentation with the credentials.

### Option 2: Create New Supabase Project
1. Go to https://supabase.com
2. Sign up/Login
3. Create new project
4. Wait for setup (2-3 minutes)
5. Go to Settings → API
6. Copy credentials to `.env.local`

### Option 3: Use Existing Project
From your terminal error, it looks like your project ID might be: `frzxrohhhpvbgwxnisww`

Your URL would be:
```
https://frzxrohhhpvbgwxnisww.supabase.co
```

You just need to get the anon key from the Supabase dashboard.

---

## ✅ After Setup

Once `.env.local` is configured:

1. Login page will work: http://localhost:3000/login
2. You can proceed with admin user creation
3. Follow the setup guides in the documentation

---

**Need the credentials?**
- Check your Supabase dashboard
- Check with your team if this is a shared project
- Or create a new Supabase project

**Last Updated**: November 1, 2025

