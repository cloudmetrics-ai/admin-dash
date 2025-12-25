/**
 * Comprehensive Setup and Usage Guide
 * ====================================
 * 
 * This guide provides step-by-step instructions for:
 * 1. Setting up the development environment
 * 2. Running the application
 * 3. Adding new pages and features
 * 4. Database operations
 * 5. Deployment
 */

# Full-Stack Admin Dashboard - Complete Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Running the Application](#running-the-application)
4. [Project Structure](#project-structure)
5. [Adding New Pages](#adding-new-pages)
6. [Database Operations](#database-operations)
7. [API Documentation](#api-documentation)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

### Required Software
- **Node.js** 18+ and npm
- **Python** 3.11+
- **PostgreSQL** 15+
- **Git**

### Optional (for advanced features)
- **Redis** (for caching and background tasks)
- **Docker** (for containerized deployment)

---

## 🚀 Initial Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install email validator (required for Pydantic email validation)
pip install pydantic[email]

# Create .env file from template
cp .env.example .env

# Edit .env file with your configuration
# IMPORTANT: Change SECRET_KEY in production!
nano .env
```

**Configure .env file:**
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/admin_dashboard
SECRET_KEY=your-secret-key-here-change-in-production
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
OPENAI_API_KEY=sk-your-key-here  # Optional, for LLM features
```

> **Important**: `CORS_ORIGINS` must be in JSON array format with square brackets and quotes.

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb admin_dashboard

# Or using psql:
psql -U postgres
CREATE DATABASE admin_dashboard;
\q

# Initialize database tables
# Option 1: Using Python
python -c "from app.core.database import init_db; init_db()"

# Option 2: Using Alembic (recommended for production)
alembic upgrade head
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Install additional packages
npm install axios zustand

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

---

## ▶️ Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn app.main:app --reload

# Backend will run on: http://localhost:8000
# API docs available at: http://localhost:8000/docs
```

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev

# Frontend will run on: http://localhost:3000
```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

---

## 📁 Project Structure

```
Learn_v1/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/v1/            # API endpoints
│   │   │   ├── auth.py        # Authentication routes
│   │   │   └── ...
│   │   ├── core/              # Core functionality
│   │   │   ├── config.py      # Configuration
│   │   │   ├── database.py    # Database setup
│   │   │   └── security.py    # JWT & hashing
│   │   ├── models/            # Database models
│   │   │   └── user.py
│   │   ├── schemas/           # Pydantic schemas
│   │   │   ├── user.py
│   │   │   └── token.py
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt
│   └── .env
│
├── frontend/                   # Next.js frontend
│   ├── app/                   # App router pages
│   ├── components/            # React components
│   ├── lib/                   # Utilities
│   │   └── api.ts            # API client
│   └── .env.local
│
└── README.md
```

---

## ➕ Adding New Pages

### Step-by-Step Guide

#### 1. Create Database Model (Backend)

```python
# backend/app/models/product.py
from sqlalchemy import Column, String, Integer, Float
from app.core.database import Base
import uuid

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
```

#### 2. Create Pydantic Schema

```python
# backend/app/schemas/product.py
from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float

class ProductResponse(ProductCreate):
    id: str
    
    class Config:
        from_attributes = True
```

#### 3. Create API Endpoint

```python
# backend/app/api/v1/products.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
```

#### 4. Register Router in main.py

```python
# backend/app/main.py
from app.api.v1 import products

app.include_router(
    products.router,
    prefix=settings.API_V1_STR
)
```

#### 5. Create Database Migration

```bash
cd backend
alembic revision --autogenerate -m "Add products table"
alembic upgrade head
```

#### 6. Create Frontend Page

```typescript
// frontend/app/(dashboard)/products/page.tsx
'use client';

import { useState, useEffect } from 'react';
import api from '@/lib/api';

export default function ProductsPage() {
  const [products, setProducts] = useState([]);
  
  useEffect(() => {
    fetchProducts();
  }, []);
  
  const fetchProducts = async () => {
    try {
      const response = await api.get('/api/v1/products');
      setProducts(response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };
  
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Products</h1>
      <div className="grid gap-4">
        {products.map((product: any) => (
          <div key={product.id} className="p-4 bg-white rounded-lg shadow">
            <h2 className="font-semibold">{product.name}</h2>
            <p className="text-gray-600">{product.description}</p>
            <p className="text-lg font-bold">${product.price}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

#### 7. Add Navigation Link

Update your sidebar component to include the new page.

---

## 🗄️ Database Operations

### Creating Migrations

```bash
cd backend

# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# View migration history
alembic history
```

### Manual Database Operations

```python
# backend/scripts/seed_data.py
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()

# Create admin user
admin = User(
    email="admin@example.com",
    username="admin",
    hashed_password=hash_password("admin123"),
    is_superuser=True
)
db.add(admin)
db.commit()
```

---

## 📚 API Documentation

### Authentication Flow

1. **Register**: `POST /api/v1/auth/register`
2. **Login**: `POST /api/v1/auth/login` → Returns tokens
3. **Use Token**: Include in headers: `Authorization: Bearer <token>`
4. **Refresh**: `POST /api/v1/auth/refresh` → Get new access token

### Example API Calls

```javascript
// Register
const user = await authApi.register({
  email: 'john@example.com',
  password: 'SecurePass123',
  username: 'johndoe'
});

// Login
const { access_token } = await authApi.login(
  'john@example.com',
  'SecurePass123'
);
localStorage.setItem('access_token', access_token);

// Get current user
const currentUser = await authApi.getCurrentUser();
```

---

## 🚢 Deployment

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Deployment

#### Backend (Heroku/Railway/Render)

```bash
# Install production server
pip install gunicorn

# Run with Gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

#### Frontend (Vercel/Netlify)

```bash
# Build for production
npm run build

# The build output will be in .next/ directory
```

---

## 🔍 Troubleshooting

### Common Issues

**Database Connection Error**
```
Solution: Check DATABASE_URL in .env file
Verify PostgreSQL is running: pg_isready
```

**CORS Error**
```
Solution: Add frontend URL to CORS_ORIGINS in backend/.env
Example: CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
Note: Must be in JSON array format with square brackets and quotes
```

**Token Expired**
```
Solution: Implement token refresh in frontend
Or increase ACCESS_TOKEN_EXPIRE_MINUTES in backend
```

**Import Errors**
```
Solution: Ensure virtual environment is activated
Run: pip install -r requirements.txt
```

**Email Validator Error**
```
Error: email-validator is not installed
Solution: pip install pydantic[email]
```

**CORS_ORIGINS Configuration Error**
```
Error: error parsing value for field "CORS_ORIGINS"
Solution: Use JSON array format in .env file
Example: CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

---

## 📞 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Review the code comments
3. Create an issue in the repository

---

**Built with ❤️ using Next.js 14 and FastAPI**
