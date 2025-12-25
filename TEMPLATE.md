# 🚀 Full-Stack Application Template

**A production-ready template for building modern web applications with authentication, CRUD operations, and best practices built-in.**

---

## ✨ What's Included

This template provides everything you need to start building your application:

### Authentication & Security
- ✅ Email/Password authentication with JWT
- ✅ Multi-Factor Authentication (TOTP)
- ✅ Email verification for new users
- ✅ Password reset functionality
- ✅ Role-Based Access Control (RBAC)
- ✅ Permission management system

### Backend (FastAPI + PostgreSQL)
- ✅ RESTful API with automatic documentation
- ✅ SQLAlchemy ORM with Alembic migrations
- ✅ Pydantic validation
- ✅ Database connection pooling
- ✅ CORS configuration
- ✅ Error handling middleware

### Frontend (Next.js + TypeScript)
- ✅ Modern React with TypeScript
- ✅ Server-side rendering (SSR)
- ✅ Responsive UI components
- ✅ Form validation
- ✅ API client with error handling
- ✅ Dark mode support

### DevOps & Deployment
- ✅ Docker Compose setup
- ✅ Local development scripts
- ✅ Environment configuration
- ✅ Database migrations
- ✅ Logging setup

---

## 🎯 Use This Template For

- SaaS applications
- Admin dashboards
- E-commerce platforms
- Content management systems
- Internal tools
- API-first applications

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the template
git clone <your-repo-url>
cd Learn_v1

# Start everything with one command
./setup.sh

# Access your app
open http://localhost:3000
```

### Option 2: Local Development

```bash
# Clone the template
git clone <your-repo-url>
cd Learn_v1

# Setup (one time)
./dev-setup.sh

# Start services
./dev-start.sh

# Access your app
open http://localhost:3000
```

---

## 📚 Customization Guides

### 1. Rename Your Project

```bash
# Update project name throughout
find . -type f -name "*.py" -o -name "*.ts" -o -name "*.tsx" -o -name "*.json" | \
  xargs sed -i '' 's/Learn App/Your App Name/g'

# Update in key files:
# - backend/app/core/config.py (PROJECT_NAME)
# - frontend/package.json (name)
# - README.md
# - docker-compose.yml (container names)
```

### 2. Update Branding

**Backend** (`backend/app/core/config.py`):
```python
PROJECT_NAME = "Your App Name"
VERSION = "1.0.0"
```

**Frontend** (`frontend/src/app/layout.tsx`):
```typescript
export const metadata = {
  title: 'Your App Name',
  description: 'Your app description',
}
```

### 3. Configure Environment

**Backend** (`.env`):
```env
SECRET_KEY=<generate-new-secret-key>
DATABASE_URL=postgresql://user:pass@host:port/dbname
SMTP_HOST=smtp.your-provider.com
```

**Frontend** (`.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🔨 Adding CRUD Operations

See [CRUD_GUIDE.md](./CRUD_GUIDE.md) for step-by-step instructions on adding new entities.

**Quick Example:**

1. **Create Model** (`backend/app/models/product.py`)
2. **Create Schemas** (`backend/app/schemas/product.py`)
3. **Create API** (`backend/app/api/v1/products.py`)
4. **Create Frontend Pages** (`frontend/src/app/products/`)

---

## 📖 Documentation

- [CRUD Guide](./CRUD_GUIDE.md) - Add new entities
- [Architecture](./ARCHITECTURE.md) - Project structure
- [Development](./DEVELOPMENT.md) - Local vs Docker
- [Integration Guide](./INTEGRATION_GUIDE.md) - Third-party services

---

## 🏗️ Project Structure

```
Learn_v1/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/v1/         # API endpoints
│   │   ├── core/           # Core config
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── alembic/            # Migrations
│   └── tests/              # Tests
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Pages (App Router)
│   │   ├── components/    # React components
│   │   └── lib/           # Utilities
│   └── public/            # Static files
├── scripts/               # Helper scripts
├── docker-compose.yml     # Docker setup
└── README.md             # This file
```

---

## 🔧 Available Scripts

### Docker Mode
```bash
./setup.sh      # First-time setup
./start.sh      # Start services
./stop.sh       # Stop services
```

### Local Development
```bash
./dev-setup.sh  # First-time setup
./dev-start.sh  # Start services
./dev-stop.sh   # Stop services
```

---

## 🌐 API Documentation

Once running, access interactive API docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

---

## 🚢 Deployment

### Docker Deployment

```bash
# Build for production
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment

See deployment guides for:
- AWS (EC2, ECS, Lambda)
- Google Cloud (Cloud Run, GKE)
- DigitalOcean (App Platform, Droplets)
- Heroku
- Vercel (Frontend) + Railway (Backend)

---

## 🔐 Security Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Update database credentials
- [ ] Configure SMTP for email sending
- [ ] Set up SSL/TLS certificates
- [ ] Update CORS origins
- [ ] Enable rate limiting
- [ ] Set up monitoring (Sentry, DataDog)
- [ ] Configure backups
- [ ] Review and update permissions
- [ ] Enable logging

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - feel free to use this template for your projects!

---

## 🆘 Support

- [Documentation](./docs/)
- [Issue Tracker](https://github.com/your-repo/issues)
- [Discussions](https://github.com/your-repo/discussions)

---

## 🎉 What to Build Next

Now that you have authentication and CRUD operations set up, consider adding:

- **File Uploads** - S3, Cloudinary integration
- **Payment Processing** - Stripe, PayPal
- **Real-time Features** - WebSockets, Server-Sent Events
- **Search** - Elasticsearch, Algolia
- **Analytics** - Google Analytics, Mixpanel
- **Notifications** - Push notifications, Email campaigns
- **API Rate Limiting** - Redis-based rate limiting
- **Caching** - Redis caching layer
- **Background Jobs** - Celery task queue
- **Multi-tenancy** - Organization/workspace support

---

**Happy Building! 🚀**
