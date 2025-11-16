# 🍅 Fito - Tomato Leaf Disease Detection

AI-powered tomato leaf disease detection using deep learning. This project helps farmers identify 10 different tomato diseases and healthy plants through image analysis.

## 🚀 Quick Start

### Backend Setup (FastAPI)
```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API will be available at: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Frontend Setup (Next.js)
```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at: http://localhost:3000

### Admin Setup (Database & Authentication)
```bash
# 1. Run database schemas in Supabase SQL Editor
# - supabase_schema.sql (main schema)
# - admin_profiles_schema.sql (admin authentication)

# 2. Create admin user via Supabase UI
# - Authentication → Users → Add User
# - Add user metadata: {"role": "admin", "full_name": "Your Name"}

# 3. Access admin dashboard
# - Visit: http://localhost:3000/login
# - Sign in with admin credentials
# - Redirects to: http://localhost:3000/admin
```

📚 **See [ADMIN_SETUP_GUIDE.md](ADMIN_SETUP_GUIDE.md) for detailed setup instructions**

## 🎯 Features

### Public Features
- **10 Disease Classes**: Detects 10 different tomato diseases + healthy plants
- **Real-time Analysis**: Instant predictions with confidence scores
- **Modern UI**: Clean, responsive interface with primary color #47f793
- **Drag & Drop**: Easy image upload with preview
- **Detailed Results**: Shows all predictions with confidence percentages

### Admin Features
- **🔐 Authentication System**: Sign-in/Sign-up with email verification
- **📊 Admin Dashboard**: Real-time statistics and category analytics
- **🗄️ Dataset Management**: View, edit, delete, and export predictions
- **👥 Admin Profiles**: Role-based access control (Admin & Super Admin)
- **📈 Analytics**: Track predictions, confidence scores, and trends
- **💾 Data Export**: CSV and ZIP export functionality

## 🧠 Disease Classes Detected

1. **Healthy** - Normal tomato leaf
2. **Early Blight** - Fungal disease (Alternaria solani)
3. **Late Blight** - Oomycete infection (Phytophthora infestans)
4. **Septoria Leaf Spot** - Fungal disease (Septoria lycopersici)
5. **Bacterial Spot** - Bacterial infection (Xanthomonas campestris)
6. **Leaf Mold** - Fungal disease (Cladosporium fulvum)
7. **Yellow Leaf Curl Virus** - Viral disease (TYLCV)
8. **Mosaic Virus** - Viral disease (TMV/ToMV)
9. **Target Spot** - Fungal disease (Corynespora cassiicola)
10. **Spider Mites** - Pest infestation (Tetranychus urticae)

## 🛠️ Technical Stack

- **Backend**: FastAPI + TensorFlow + MobileNetV2
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **Model**: Transfer learning with MobileNetV2 (128x128 input)
- **API**: RESTful endpoints with CORS support

## 📁 Project Structure

```
Fito/
├── backend/                 # FastAPI backend
│   ├── app.py              # Main API server
│   ├── model_handler.py    # Model loading & prediction
│   ├── requirements.txt    # Python dependencies
│   └── trained_model_fito.h5  # Trained model
├── frontend/               # Next.js frontend
│   ├── src/app/           # App router pages
│   └── package.json
├── assets/                 # Shared assets
│   └── fito_logo.png
└── docs/                  # Documentation
```

## 🔧 API Endpoints

### Public Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /predict` - Upload image and get prediction
- `GET /classes` - Get list of all disease classes

### Admin Endpoints
- `GET /admin/stats` - Get category statistics
- `GET /admin/predictions` - Get all predictions with filters
- `PUT /admin/predictions/{id}` - Update prediction label
- `DELETE /admin/predictions/{id}` - Delete prediction
- `GET /admin/export/csv` - Export data as CSV
- `GET /admin/export/zip` - Export images as ZIP

## 🔐 Authentication Routes

- `/login` - Sign-in/Sign-up page (minimalist design)
- `/admin` - Admin dashboard (protected)
- `/admin/login` - Legacy admin login (still available)
- `/admin/dataset` - Dataset management (protected)

## 🎨 Design

- **Primary Color**: #47f793 (Bright Green)
- **UI Style**: Modern, clean, professional
- **Responsive**: Mobile-first design
- **Accessibility**: WCAG compliant

## 🚀 Deployment

Ready for deployment on:
- **Frontend**: Vercel, Netlify
- **Backend**: Railway, Render, Heroku
- **Model**: Can be optimized for production

## 📚 Documentation

- **[ADMIN_SETUP_GUIDE.md](ADMIN_SETUP_GUIDE.md)** - Complete admin authentication setup
- **[LOGIN_QUICK_REFERENCE.md](LOGIN_QUICK_REFERENCE.md)** - Quick reference for login system
- **[AUTHENTICATION_README.md](AUTHENTICATION_README.md)** - Detailed authentication documentation
- **[DATABASE_SCHEMA.md](DATABASE_SCHEMA.md)** - Database schema and structure
- **[SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)** - System architecture overview
- **[ADMIN_DASHBOARD_README.md](ADMIN_DASHBOARD_README.md)** - Admin dashboard features

## 📝 License

This project is for educational and agricultural purposes.
