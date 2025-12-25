# Project Architecture

This document explains the architecture, design decisions, and structure of the application template.

---

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration tool
- **Pydantic** - Data validation
- **PostgreSQL** - Relational database
- **JWT** - Authentication tokens
- **TOTP** - Multi-factor authentication

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Axios** - HTTP client
- **CSS Modules** - Component-scoped styling

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

---

## Project Structure

```
Learn_v1/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API Layer
│   │   │   └── v1/           # API version 1
│   │   │       ├── auth.py   # Authentication endpoints
│   │   │       ├── users.py  # User management
│   │   │       └── __init__.py
│   │   ├── core/             # Core Functionality
│   │   │   ├── config.py     # Configuration
│   │   │   ├── database.py   # Database connection
│   │   │   ├── security.py   # Security utilities
│   │   │   └── deps.py       # Dependencies
│   │   ├── models/           # Database Models
│   │   │   ├── user.py       # User model
│   │   │   └── __init__.py
│   │   ├── schemas/          # Pydantic Schemas
│   │   │   ├── user.py       # User schemas
│   │   │   ├── auth.py       # Auth schemas
│   │   │   └── __init__.py
│   │   ├── services/         # Business Logic
│   │   │   ├── email_service.py
│   │   │   └── __init__.py
│   │   └── main.py           # Application entry point
│   ├── alembic/              # Database Migrations
│   │   ├── versions/         # Migration files
│   │   └── env.py
│   ├── tests/                # Tests
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile           # Docker configuration
│   └── .env                 # Environment variables
│
├── frontend/                  # Next.js Frontend
│   ├── src/
│   │   ├── app/              # Pages (App Router)
│   │   │   ├── login/
│   │   │   ├── register/
│   │   │   ├── dashboard/
│   │   │   └── layout.tsx
│   │   ├── components/       # React Components
│   │   │   ├── ui/          # UI components
│   │   │   └── layouts/     # Layout components
│   │   └── lib/             # Utilities
│   │       ├── api.ts       # API client
│   │       └── auth.ts      # Auth utilities
│   ├── public/              # Static files
│   ├── package.json         # Node dependencies
│   ├── Dockerfile          # Docker configuration
│   └── .env.local          # Environment variables
│
├── docker-compose.yml        # Docker orchestration
├── setup.sh                 # Docker setup script
├── dev-setup.sh            # Local setup script
└── README.md               # Documentation
```

---

## Backend Architecture

### Layered Architecture

```
┌─────────────────────────────────────┐
│         API Layer (FastAPI)         │
│  - Request validation               │
│  - Response serialization           │
│  - Error handling                   │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│      Business Logic (Services)      │
│  - Email sending                    │
│  - Authentication                   │
│  - Authorization                    │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│      Data Layer (SQLAlchemy)        │
│  - Database operations              │
│  - Model definitions                │
│  - Relationships                    │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│         Database (PostgreSQL)        │
└─────────────────────────────────────┘
```

### Request Flow

1. **Request** → API endpoint receives HTTP request
2. **Validation** → Pydantic validates request data
3. **Authentication** → JWT token verified
4. **Authorization** → Permissions checked
5. **Business Logic** → Service layer processes request
6. **Database** → SQLAlchemy executes queries
7. **Response** → Pydantic serializes response
8. **Return** → JSON response sent to client

### Key Components

#### 1. Configuration (`core/config.py`)
- Environment-based settings
- Pydantic BaseSettings for validation
- Centralized configuration management

#### 2. Database (`core/database.py`)
- Connection pooling
- Session management
- Dependency injection

#### 3. Security (`core/security.py`)
- Password hashing (bcrypt)
- JWT token creation/verification
- TOTP for MFA

#### 4. Models (`models/`)
- SQLAlchemy ORM models
- Database table definitions
- Relationships between entities

#### 5. Schemas (`schemas/`)
- Request validation
- Response serialization
- Type safety

#### 6. Services (`services/`)
- Business logic
- External integrations
- Reusable functionality

---

## Frontend Architecture

### Component Structure

```
App (layout.tsx)
├── AuthProvider
├── ThemeProvider
└── Pages
    ├── Public Pages
    │   ├── Login
    │   ├── Register
    │   └── Forgot Password
    └── Protected Pages
        ├── Dashboard
        ├── Profile
        └── Admin
```

### State Management

- **Server State**: API calls with axios
- **Client State**: React useState/useContext
- **Form State**: Controlled components
- **Auth State**: localStorage + Context API

### Routing

Using Next.js App Router:
- File-based routing
- Server components by default
- Client components with 'use client'
- Dynamic routes with [id]

---

## Authentication Flow

### Registration
```
1. User submits registration form
2. Backend validates data
3. Password hashed with bcrypt
4. User created in database (email_verified=false)
5. Verification token generated
6. Verification email sent
7. User clicks link in email
8. Token validated
9. email_verified set to true
10. User can now login
```

### Login
```
1. User submits credentials
2. Backend validates email/password
3. Check if email is verified
4. If MFA enabled, require TOTP code
5. Generate JWT access token
6. Generate refresh token
7. Return tokens to client
8. Client stores tokens
9. Client redirects to dashboard
```

### Protected Routes
```
1. Client makes API request
2. Axios interceptor adds JWT token
3. Backend validates token
4. Check token expiration
5. Extract user from token
6. Check permissions
7. Process request or return 401/403
```

---

## Database Design

### User Table
```sql
users
├── id (PK)
├── email (unique)
├── hashed_password
├── full_name
├── is_active
├── is_superuser
├── email_verified
├── verification_token
├── verification_token_expires
├── reset_token
├── reset_token_expires
├── mfa_enabled
├── mfa_secret
├── mfa_backup_codes
├── created_at
└── updated_at
```

### Roles & Permissions (RBAC)
```sql
roles                    user_roles              permissions
├── id (PK)             ├── user_id (FK)        ├── id (PK)
├── name                ├── role_id (FK)        ├── name
└── description         └── assigned_at         └── description

role_permissions
├── role_id (FK)
└── permission_id (FK)
```

---

## Security Considerations

### Password Security
- Bcrypt hashing with salt
- Minimum 8 characters
- No password in logs/responses

### Token Security
- Short-lived access tokens (30 min)
- Long-lived refresh tokens (7 days)
- Tokens stored securely (httpOnly cookies recommended)

### API Security
- CORS configuration
- Rate limiting
- Input validation
- SQL injection prevention (ORM)
- XSS prevention

### MFA
- TOTP (Time-based One-Time Password)
- QR code generation
- Backup codes
- Recovery options

---

## Performance Optimizations

### Backend
- Database connection pooling
- Query optimization with indexes
- Lazy loading relationships
- Response caching (Redis)

### Frontend
- Server-side rendering (SSR)
- Code splitting
- Image optimization
- Static generation where possible

---

## Deployment Architecture

### Production Setup

```
┌──────────────┐
│   Nginx      │  ← Reverse proxy, SSL termination
└──────────────┘
       ↓
┌──────────────┐
│  Next.js     │  ← Frontend (port 3000)
└──────────────┘
       ↓
┌──────────────┐
│  FastAPI     │  ← Backend API (port 8000)
└──────────────┘
       ↓
┌──────────────┐
│  PostgreSQL  │  ← Database (port 5432)
└──────────────┘
```

### Scaling Strategies

1. **Horizontal Scaling**
   - Multiple backend instances
   - Load balancer
   - Shared database

2. **Caching**
   - Redis for sessions
   - CDN for static assets
   - Database query caching

3. **Database**
   - Read replicas
   - Connection pooling
   - Query optimization

---

## Development Workflow

1. **Local Development**
   - Use `dev-start.sh`
   - Hot reload enabled
   - Direct database access

2. **Docker Development**
   - Use `setup.sh`
   - Isolated environment
   - Production parity

3. **Testing**
   - Unit tests (pytest)
   - Integration tests
   - E2E tests

4. **Deployment**
   - Build Docker images
   - Push to registry
   - Deploy to production

---

## Best Practices

### Code Organization
- Separation of concerns
- Single responsibility principle
- DRY (Don't Repeat Yourself)
- Clear naming conventions

### API Design
- RESTful conventions
- Consistent error responses
- Versioning (/api/v1/)
- Comprehensive documentation

### Database
- Migrations for all schema changes
- Indexes on frequently queried fields
- Foreign key constraints
- Soft deletes where appropriate

### Security
- Never commit secrets
- Use environment variables
- Regular dependency updates
- Security audits

---

## Extending the Template

### Adding New Features

1. **New Entity**
   - Create model
   - Create schemas
   - Create API endpoints
   - Create frontend pages
   - Run migration

2. **Third-party Integration**
   - Add to services/
   - Configure in .env
   - Create API wrapper
   - Add error handling

3. **Background Jobs**
   - Use Celery
   - Configure Redis
   - Create tasks
   - Monitor execution

---

This architecture provides a solid foundation for building scalable, maintainable web applications. Customize as needed for your specific requirements.
