# 🔐 Fito Authentication Flow Diagram

## Complete Authentication Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER JOURNEY                                │
└─────────────────────────────────────────────────────────────────────┘

                    User visits Fito website
                              │
                              ▼
                    ┌──────────────────┐
                    │   Public Pages   │
                    │  /home, /about   │
                    │  /faq, /contact  │
                    │  /information    │
                    └──────────────────┘
                              │
                              │ User clicks "Log-in" button
                              ▼
                    ┌──────────────────┐
                    │   /login Page    │
                    │  (Minimalist)    │
                    └──────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
        ┌──────────────┐          ┌──────────────┐
        │   SIGN-IN    │          │   SIGN-UP    │
        │    Form      │          │    Form      │
        └──────────────┘          └──────────────┘
                │                           │
                │                           │
                ▼                           ▼
        Enter credentials          Enter user details
        - Email                    - Full Name
        - Password                 - Email
                │                  - Password
                │                  - Confirm Password
                │                           │
                │                           ▼
                │                  Create Supabase Account
                │                           │
                │                           ▼
                │                  Email Verification
                │                           │
                │                           ▼
                │                  Admin adds role metadata
                │                  {"role": "admin"}
                │                           │
                └───────────┬───────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │   Supabase Auth API   │
                │  signInWithPassword() │
                └───────────────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │  Check User Metadata  │
                │   role === 'admin'?   │
                └───────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
            ✅ YES                   ❌ NO
                │                       │
                │                       ▼
                │              ┌──────────────────┐
                │              │  Access Denied   │
                │              │  Error Message   │
                │              │  Auto Sign Out   │
                │              └──────────────────┘
                │                       │
                │                       ▼
                │              Stay on /login page
                │
                ▼
    ┌───────────────────────┐
    │  Admin Profile Check  │
    │  (admin_profiles)     │
    └───────────────────────┘
                │
                ▼
    ┌───────────────────────┐
    │ Update Last Login     │
    │ Timestamp             │
    └───────────────────────┘
                │
                ▼
    ┌───────────────────────┐
    │  Redirect to /admin   │
    │  (Dashboard)          │
    └───────────────────────┘
                │
                ▼
    ┌───────────────────────┐
    │  AdminLayout Wrapper  │
    │  - Check Auth         │
    │  - Verify Admin Role  │
    │  - Show Sidebar       │
    └───────────────────────┘
                │
                ▼
    ┌───────────────────────┐
    │   Admin Dashboard     │
    │   - Statistics        │
    │   - Category Cards    │
    │   - Dataset Link      │
    └───────────────────────┘
```

---

## Database Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                      DATABASE INTERACTIONS                          │
└─────────────────────────────────────────────────────────────────────┘

User Signs Up
      │
      ▼
┌──────────────────┐
│  auth.users      │  ← Supabase Auth creates user
│  - id (UUID)     │
│  - email         │
│  - metadata      │
│    └─ role       │
│    └─ full_name  │
└──────────────────┘
      │
      │ Trigger: on_auth_user_created_create_admin_profile
      ▼
┌──────────────────┐
│ admin_profiles   │  ← Auto-created by trigger
│  - id            │
│  - user_id ──────┼─→ auth.users(id)
│  - full_name     │
│  - email         │
│  - role          │  ('admin' or 'super_admin')
│  - is_active     │  (true/false)
│  - last_login    │  (timestamp)
│  - created_at    │
│  - updated_at    │
└──────────────────┘
      │
      │ When user uploads image
      ▼
┌──────────────────┐
│  predictions     │  ← Stores prediction data
│  - id            │
│  - storage_path  │
│  - image_url     │
│  - predicted_label
│  - confidence    │
│  - final_label   │  (admin can edit)
│  - uploader_id ──┼─→ auth.users(id)
│  - uploader_name │
│  - created_at    │
│  - updated_at    │
└──────────────────┘
```

---

## Security Layers

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SECURITY FLOW                               │
└─────────────────────────────────────────────────────────────────────┘

Request to /admin/*
      │
      ▼
┌──────────────────────────┐
│  Frontend Route Guard    │
│  (AdminLayout.tsx)       │
│  - Check if logged in    │
│  - Get user from session │
└──────────────────────────┘
      │
      ▼
┌──────────────────────────┐
│  Supabase Auth Check     │
│  supabase.auth.getUser() │
└──────────────────────────┘
      │
      ├─→ No user? → Redirect to /login
      │
      ▼
┌──────────────────────────┐
│  Check User Metadata     │
│  user.user_metadata.role │
└──────────────────────────┘
      │
      ├─→ Not admin? → Redirect to /home
      │
      ▼
┌──────────────────────────┐
│  Check Admin Profile     │
│  Query admin_profiles    │
└──────────────────────────┘
      │
      ├─→ Not active? → Access denied
      │
      ▼
┌──────────────────────────┐
│  Row Level Security      │
│  (RLS Policies)          │
│  - Check permissions     │
│  - Verify role           │
└──────────────────────────┘
      │
      ▼
✅ Access Granted
      │
      ▼
Show Admin Dashboard
```

---

## Component Hierarchy

```
┌─────────────────────────────────────────────────────────────────────┐
│                      COMPONENT STRUCTURE                            │
└─────────────────────────────────────────────────────────────────────┘

App (layout.tsx)
│
├── Navigation
│   ├── Logo (FITO)
│   ├── Nav Links (Home, Identify, Info, About, FAQ, Contact)
│   └── Log-in Button → /login
│
├── BackgroundProvider
│   └── Dynamic backgrounds
│
├── Public Pages
│   ├── Home (/)
│   ├── About (/about)
│   ├── FAQ (/faq)
│   ├── Contact (/contact)
│   ├── Information (/information)
│   └── Fito (/fito) - Upload & Predict
│
├── Authentication
│   ├── Login Page (/login) ⭐ NEW
│   │   ├── Sign-In Form
│   │   │   ├── Email Input
│   │   │   ├── Password Input
│   │   │   ├── Error Display
│   │   │   └── Submit Button
│   │   │
│   │   ├── Sign-Up Form
│   │   │   ├── Full Name Input
│   │   │   ├── Email Input
│   │   │   ├── Password Input
│   │   │   ├── Confirm Password Input
│   │   │   ├── Validation
│   │   │   └── Submit Button
│   │   │
│   │   ├── Form Toggle Button
│   │   └── Back to Home Link
│   │
│   └── Legacy Login (/admin/login)
│       └── Simple sign-in only
│
└── Admin Pages (/admin/*)
    │
    ├── AdminLayout (wrapper)
    │   ├── Auth Check
    │   ├── Role Verification
    │   ├── Sidebar
    │   │   ├── Logo
    │   │   ├── Dashboard Link
    │   │   ├── Dataset Link
    │   │   └── Logout Button
    │   │
    │   └── Main Content Area
    │
    ├── Dashboard (/admin)
    │   ├── Total Counter
    │   └── Category Cards (10)
    │       ├── Disease Name
    │       ├── Count
    │       └── Percentage
    │
    └── Dataset (/admin/dataset)
        ├── Filters
        │   ├── Category Dropdown
        │   └── Search Input
        │
        ├── Data Table
        │   ├── Headers
        │   └── Rows (20 per page)
        │       ├── Thumbnail
        │       ├── Labels
        │       ├── Confidence
        │       ├── Date
        │       └── Actions
        │           ├── Preview
        │           ├── Relabel
        │           ├── Download
        │           └── Delete
        │
        ├── Pagination
        │   ├── Previous
        │   ├── Page Info
        │   └── Next
        │
        └── Export Buttons
            ├── CSV Export
            └── ZIP Export
```

---

## State Management

```
┌─────────────────────────────────────────────────────────────────────┐
│                         STATE FLOW                                  │
└─────────────────────────────────────────────────────────────────────┘

Login Page State:
├── isSignUp: boolean          (toggle between sign-in/sign-up)
├── email: string              (user email)
├── password: string           (user password)
├── confirmPassword: string    (password confirmation)
├── fullName: string           (user full name)
├── error: string              (error messages)
├── message: string            (success messages)
└── loading: boolean           (loading state)

AdminLayout State:
├── isAdmin: boolean           (admin verification)
├── loading: boolean           (auth check loading)
└── user: User | null          (current user data)

Dashboard State:
├── stats: CategoryStats[]     (category statistics)
├── loading: boolean           (data loading)
└── totalImages: number        (total predictions)

Dataset State:
├── predictions: Prediction[]  (all predictions)
├── filteredPredictions: []    (filtered results)
├── loading: boolean           (data loading)
├── selectedCategory: string   (filter by category)
├── searchQuery: string        (search term)
├── selectedImage: Prediction  (preview modal)
├── relabelId: string          (relabel modal)
├── newLabel: string           (new label value)
├── currentPage: number        (pagination)
└── itemsPerPage: number       (20 per page)
```

---

## API Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         API CALLS                                   │
└─────────────────────────────────────────────────────────────────────┘

Authentication:
│
├── Sign In
│   POST supabase.auth.signInWithPassword()
│   ├── Input: { email, password }
│   ├── Returns: { user, session }
│   └── Check: user.user_metadata.role === 'admin'
│
├── Sign Up
│   POST supabase.auth.signUp()
│   ├── Input: { email, password, options: { data: { full_name, role } } }
│   ├── Returns: { user, session }
│   └── Trigger: Auto-create admin_profiles entry
│
└── Sign Out
    POST supabase.auth.signOut()
    └── Redirect to /home

Admin Operations:
│
├── Get Statistics
│   GET /admin/stats
│   └── Returns: Category counts and percentages
│
├── Get Predictions
│   GET /admin/predictions?category=X&search=Y
│   └── Returns: Filtered predictions list
│
├── Update Prediction
│   PUT /admin/predictions/{id}
│   ├── Input: { final_label }
│   └── Returns: Updated prediction
│
├── Delete Prediction
│   DELETE /admin/predictions/{id}
│   └── Returns: Success message
│
├── Export CSV
│   GET /admin/export/csv?category=X
│   └── Returns: CSV file download
│
└── Export ZIP
    GET /admin/export/zip?category=X
    └── Returns: ZIP file with images
```

---

## Error Handling

```
┌─────────────────────────────────────────────────────────────────────┐
│                      ERROR HANDLING FLOW                            │
└─────────────────────────────────────────────────────────────────────┘

Login Errors:
│
├── Invalid Credentials
│   └── Display: "Invalid email or password"
│
├── Email Not Verified
│   └── Display: "Please verify your email address"
│
├── No Admin Role
│   └── Display: "Access denied. Admin privileges required."
│   └── Action: Auto sign out
│
├── Password Mismatch (Sign-Up)
│   └── Display: "Passwords do not match"
│
├── Weak Password
│   └── Display: "Password must be at least 6 characters"
│
└── Network Error
    └── Display: "Connection error. Please try again."

Admin Errors:
│
├── Not Authenticated
│   └── Redirect to /login
│
├── Not Admin
│   └── Redirect to /home
│
├── Inactive Account
│   └── Display: "Your account has been deactivated"
│   └── Action: Sign out
│
└── Database Error
    └── Display: "Failed to load data. Please refresh."
```

---

## Success Paths

```
┌─────────────────────────────────────────────────────────────────────┐
│                        SUCCESS SCENARIOS                            │
└─────────────────────────────────────────────────────────────────────┘

✅ Successful Sign-In:
   User enters credentials
   → Auth validates
   → Check admin role
   → Update last_login
   → Redirect to /admin
   → Show dashboard

✅ Successful Sign-Up:
   User fills form
   → Validation passes
   → Create account
   → Send verification email
   → Show success message
   → Auto-switch to sign-in (3s)
   → User verifies email
   → Admin adds role
   → User signs in
   → Access granted

✅ Successful Admin Operation:
   Admin views dashboard
   → Stats load
   → Navigate to dataset
   → Filter/search data
   → Edit prediction
   → Save changes
   → Success toast
   → Data refreshes

✅ Successful Logout:
   Admin clicks logout
   → Sign out from Supabase
   → Clear session
   → Redirect to /home
   → Show public pages
```

---

**Legend:**
- ⭐ = New feature
- ✅ = Success path
- ❌ = Error path
- → = Flow direction
- ├── = Branch
- └── = End of branch

---

**Last Updated**: November 1, 2025  
**Version**: 1.0.0

