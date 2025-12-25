# Project Context - Quick Reference

**Last Updated:** December 25, 2025  
**Status:** ✅ Production-ready template

---

## What This Is

A full-stack application template with:
- Complete authentication system (email/password, MFA, email verification)
- Role-based access control
- Docker & local development support
- Comprehensive documentation
- Ready to customize for any project

---

## Quick Start

### Docker
```bash
./setup.sh && ./start.sh
```

### Local Development
```bash
./dev-setup.sh && ./dev-start.sh
```

---

## Current Features

✅ Authentication (JWT, MFA, Email verification, Password reset)  
✅ User management with RBAC  
✅ Docker deployment  
✅ Local development setup  
✅ Email service (SMTP/console)  
✅ API documentation  
✅ Template documentation  

---

## Documentation

- **TEMPLATE.md** - How to use as template
- **CRUD_GUIDE.md** - Add new entities
- **ARCHITECTURE.md** - System design
- **DEVELOPMENT.md** - Docker vs Local
- **SMTP_SETUP.md** - Email config

---

## Tech Stack

**Backend:** FastAPI, PostgreSQL, SQLAlchemy  
**Frontend:** Next.js 14, TypeScript, React  
**DevOps:** Docker, Docker Compose  

---

## Ports

**Docker:** Frontend:3000, Backend:8000, DB:5434  
**Local:** Frontend:3000, Backend:8000, DB:5432  

---

## Next Enhancements

Ideas for future development:
- Example CRUD (Product model)
- File uploads (S3)
- Payments (Stripe)
- Real-time features
- Search functionality
- Background jobs
- API rate limiting

---

## Key Files

- `backend/app/core/config.py` - Configuration
- `backend/app/api/v1/auth.py` - Auth endpoints
- `backend/app/models/user.py` - User model
- `frontend/src/lib/api.ts` - API client
- `docker-compose.yml` - Docker setup
- `dev-setup.sh` - Local setup (FIXED)

---

## Environment Setup

1. Copy `.env.example` to `.env` in backend/
2. Update `SECRET_KEY` (production)
3. Configure SMTP (optional)
4. Run setup script

---

For complete details, see the walkthrough artifact or documentation files.
