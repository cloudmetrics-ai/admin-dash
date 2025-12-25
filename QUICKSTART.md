# Quick Start Guide - Running Locally
## Step-by-Step Instructions

Follow these steps exactly to get your application running on localhost.

---

## ✅ Prerequisites Check

Before starting, ensure you have:
- [ ] **Python 3.11+** installed (`python --version`)
- [ ] **Node.js 18+** installed (`node --version`)
- [ ] **PostgreSQL 15+** installed and running (`pg_isready`)
- [ ] **Git** installed

---

## 🗄️ Step 1: Set Up Database (5 minutes)

### Option A: Using Terminal
```bash
# Create the database
createdb admin_dashboard

# Verify it was created
psql -l | grep admin_dashboard
```

### Option B: Using psql
```bash
# Open PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE admin_dashboard;

# Exit psql
\q
```

**✅ Checkpoint**: Database `admin_dashboard` should exist

---

## 🐍 Step 2: Set Up Backend (10 minutes)

### 2.1 Navigate to Backend Directory
```bash
cd /Users/sai/Visual_Studio_Projects/Learn_v1/backend
```

### 2.2 Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

### 2.3 Install Dependencies
```bash
# Install all Python packages
pip install -r requirements.txt

# Install email validator (required for Pydantic email validation)
pip install pydantic[email]

# This will take 2-3 minutes
```

### 2.4 Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit the .env file
nano .env
```

**Minimum required configuration** in `.env`:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/admin_dashboard
SECRET_KEY=your-secret-key-change-this-in-production
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

> [!IMPORTANT]
> Note: `CORS_ORIGINS` must be in JSON array format (with square brackets and quotes), not a comma-separated string.

Press `Ctrl+X`, then `Y`, then `Enter` to save and exit nano.

### 2.5 Initialize Database Tables
```bash
# Create tables using Python
python -c "from app.core.database import init_db; init_db()"
```

### 2.6 Start Backend Server
```bash
# Start the FastAPI server
uvicorn app.main:app --reload
```

**✅ Checkpoint**: You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Keep this terminal open!** The backend is now running.

**Test it**: Open http://localhost:8000/docs in your browser

---

## ⚛️ Step 3: Set Up Frontend (5 minutes)

### 3.1 Open New Terminal Window
**Important**: Open a NEW terminal (don't close the backend terminal)

### 3.2 Navigate to Frontend Directory
```bash
cd /Users/sai/Visual_Studio_Projects/Learn_v1/frontend
```

### 3.3 Install Dependencies
```bash
# Install Node packages
npm install

# Install additional required packages
npm install axios zustand
```

### 3.4 Configure Environment
```bash
# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

### 3.5 Start Frontend Server
```bash
# Start Next.js development server
npm run dev
```

**✅ Checkpoint**: You should see:
```
- Local:        http://localhost:3000
- Ready in X.Xs
```

**Keep this terminal open too!**

---

## 🎉 Step 4: Verify Everything Works

### 4.1 Check Backend
Open in browser: http://localhost:8000/docs

You should see the **Swagger API documentation** with endpoints like:
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/auth/me

### 4.2 Check Frontend
Open in browser: http://localhost:3000

You should see the **Next.js default page**.

### 4.3 Test API Connection
Open browser console (F12) and run:
```javascript
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(console.log)
```

You should see:
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

---

## 🧪 Step 5: Create Your First User

### Using API Docs (Recommended)

1. Go to http://localhost:8000/docs
2. Click on **POST /api/v1/auth/register**
3. Click **"Try it out"**
4. Enter this JSON:
```json
{
  "email": "admin@example.com",
  "password": "Admin123!",
  "username": "admin",
  "full_name": "Admin User"
}
```
5. Click **"Execute"**
6. You should get a **201 Created** response with user data

### Using curl (Alternative)
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "Admin123!",
    "username": "admin",
    "full_name": "Admin User"
  }'
```

---

## 🔐 Step 6: Test Login

1. Go to http://localhost:8000/docs
2. Click on **POST /api/v1/auth/login**
3. Click **"Try it out"**
4. Enter:
```json
{
  "email": "admin@example.com",
  "password": "Admin123!"
}
```
5. Click **"Execute"**
6. You should receive **access_token** and **refresh_token**

**Copy the access_token** - you'll need it for authenticated requests!

---

## 📊 Summary - What's Running

| Service | URL | Status |
|---------|-----|--------|
| **Backend API** | http://localhost:8000 | ✅ Running |
| **API Docs** | http://localhost:8000/docs | ✅ Available |
| **Frontend** | http://localhost:3000 | ✅ Running |
| **Database** | localhost:5432 | ✅ Connected |

---

## 🛑 Stopping the Servers

### Stop Backend
In the backend terminal, press: `Ctrl+C`

### Stop Frontend
In the frontend terminal, press: `Ctrl+C`

### Deactivate Python Virtual Environment
```bash
deactivate
```

---

## 🔄 Restarting Later

### Start Backend
```bash
cd /Users/sai/Visual_Studio_Projects/Learn_v1/backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Start Frontend (in new terminal)
```bash
cd /Users/sai/Visual_Studio_Projects/Learn_v1/frontend
npm run dev
```

---

## ❌ Troubleshooting

### "Database connection failed"
```bash
# Check if PostgreSQL is running
pg_isready

# If not running, start it:
brew services start postgresql@15  # macOS with Homebrew
```

### "Port 8000 already in use"
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9
```

### "Port 3000 already in use"
```bash
# Find and kill the process
lsof -ti:3000 | xargs kill -9
```

### "Module not found" errors
```bash
# Backend: Reinstall dependencies
cd backend
pip install -r requirements.txt

# Frontend: Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### "CORS error" in browser
Check that `CORS_ORIGINS` in `backend/.env` is in JSON array format:
```env
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

### "email-validator is not installed" error
```bash
# Install the missing dependency
cd backend
source venv/bin/activate
pip install pydantic[email]
```

---

## 🎯 Next Steps

1. ✅ Both servers running
2. ✅ User created and logged in
3. 📝 Start building your dashboard pages
4. 🎨 Convert HTML designs to React components
5. 🤖 Add LLM chat features
6. 🚀 Deploy to production

---

**Need help?** Check the comprehensive guide: [SETUP_GUIDE.md](file:///Users/sai/Visual_Studio_Projects/Learn_v1/SETUP_GUIDE.md)
