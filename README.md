# Learn App - Full-Stack Admin Dashboard Template

A production-ready, full-stack admin dashboard template with authentication, role-based access control, MFA, and more.

## 🚀 Quick Start

Get the entire stack running with one command:

```bash
./setup.sh
```

That's it! The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## ✨ Features

### Authentication & Security
- ✅ Email/Password authentication
- ✅ Email verification for new users
- ✅ Password reset via email
- ✅ Multi-Factor Authentication (TOTP)
- ✅ JWT-based sessions
- ✅ Role-based access control (RBAC)
- ✅ Permission management

### User Management
- ✅ User CRUD operations
- ✅ Role assignment
- ✅ User activation/deactivation
- ✅ Profile management

### UI/UX
- ✅ Modern, responsive design
- ✅ Dark mode support
- ✅ Glassmorphism effects
- ✅ Smooth animations
- ✅ Mobile-friendly

### Developer Experience
- ✅ Docker Compose setup
- ✅ One-command deployment
- ✅ Hot reload in development
- ✅ Comprehensive API documentation
- ✅ Type-safe frontend (TypeScript)
- ✅ Database migrations (Alembic)

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **JWT** - Authentication tokens
- **TOTP** - Multi-factor authentication

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Axios** - HTTP client
- **CSS Modules** - Styling

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **PostgreSQL 15** - Database

## 📋 Prerequisites

- Docker (20.10+)
- Docker Compose (2.0+)

That's all! No need to install Node.js, Python, or PostgreSQL separately.

## 🎯 Usage

### First Time Setup
```bash
./setup.sh
```

### Start Services
```bash
./start.sh
```

### Stop Services
```bash
./stop.sh
```

### View Logs
```bash
docker-compose logs -f
```

### Access Database
```bash
docker-compose exec postgres psql -U postgres -d admin_dashboard
```

## 📁 Project Structure

```
Learn_v1/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Core functionality
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/            # Next.js frontend
│   ├── src/
│   │   ├── app/        # Pages
│   │   ├── components/ # React components
│   │   └── lib/        # Utilities
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml   # Docker orchestration
├── setup.sh            # Setup script
├── start.sh            # Start script
└── stop.sh             # Stop script
```

## ⚙️ Configuration

### Backend Environment Variables

Copy `backend/.env.example` to `backend/.env` and configure:

```env
# Security
SECRET_KEY=your-secret-key-here

# Database (auto-configured for Docker)
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/admin_dashboard

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Frontend Environment Variables

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🔐 Default Access

After setup, register a new account at http://localhost:3000/register

**Note**: Email verification links will be printed in the backend logs if SMTP is not configured.

## 📚 API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Development

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## 🚢 Production Deployment

1. Update environment variables for production
2. Change `SECRET_KEY` to a secure random value
3. Configure SMTP for email sending
4. Set up SSL/TLS certificates
5. Use a production-grade database
6. Enable logging and monitoring

## 📝 License

MIT License - feel free to use this template for your projects!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

Made with ❤️ using FastAPI and Next.js
