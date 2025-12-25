# Learn App - Development Guide

## Two Ways to Run the Application

### Option 1: Docker (Recommended for Production-like Environment)

**Prerequisites:**
- Docker Desktop

**Commands:**
```bash
# First time setup
./setup.sh

# Start services
./start.sh

# Stop services
./stop.sh
```

**Ports:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- PostgreSQL: localhost:5434

---

### Option 2: Local Development (Recommended for Active Development)

**Prerequisites:**
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

**Commands:**
```bash
# First time setup
./dev-setup.sh

# Start services
./dev-start.sh

# Stop services
./dev-stop.sh
```

**Ports:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- PostgreSQL: localhost:5432

---

## Comparison

| Feature | Docker | Local Dev |
|---------|--------|-----------|
| **Setup Time** | Slower (builds images) | Faster |
| **Hot Reload** | Limited | Full support |
| **Debugging** | More complex | Easier |
| **Isolation** | Complete | Shared with system |
| **Production Parity** | High | Medium |
| **Resource Usage** | Higher | Lower |

---

## When to Use Each

### Use Docker When:
- Testing production deployment
- Sharing with team members
- Need consistent environment
- Deploying to production

### Use Local Dev When:
- Active development
- Debugging issues
- Running tests
- Quick iterations

---

## Switching Between Modes

### From Docker to Local:
```bash
./stop.sh              # Stop Docker containers
./dev-start.sh         # Start local services
```

### From Local to Docker:
```bash
./dev-stop.sh          # Stop local services
./start.sh             # Start Docker containers
```

---

## Troubleshooting

### Port Conflicts
If ports are already in use:

**Docker Mode:**
- Edit `docker-compose.yml` to change ports
- PostgreSQL: Change `5434:5432` to another port
- Backend: Change `8000:8000` to another port
- Frontend: Change `3000:3000` to another port

**Local Mode:**
- Backend uses port 8000 (change in `dev-start.sh`)
- Frontend uses port 3000 (change in `frontend/package.json`)
- PostgreSQL uses port 5432 (system default)

### Database Issues

**Docker:**
```bash
docker-compose exec postgres psql -U postgres -d admin_dashboard
```

**Local:**
```bash
psql -h localhost -U postgres -d admin_dashboard
```

---

## Logs

### Docker Logs:
```bash
docker-compose logs -f           # All services
docker-compose logs -f backend   # Backend only
docker-compose logs -f frontend  # Frontend only
```

### Local Logs:
```bash
tail -f logs/backend.log    # Backend
tail -f logs/frontend.log   # Frontend
```

---

## Environment Variables

Both modes use the same `.env` files:
- `backend/.env` - Backend configuration
- `frontend/.env.local` - Frontend configuration

Make sure these are configured before starting either mode.
