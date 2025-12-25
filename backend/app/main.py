"""
FastAPI Main Application
=========================

This is the entry point for the FastAPI backend application.
It configures the FastAPI app, sets up middleware, includes routers,
and provides API documentation.

Run this application with:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import check_db_connection
# Import models to ensure proper initialization order
from app.models import role  # noqa: F401 - Import Role before User
from app.models import user  # noqa: F401
from app.api.v1 import auth, users, roles, mfa


# ============================================================================
# CREATE FASTAPI APPLICATION
# ============================================================================

# Create the FastAPI application instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Admin Dashboard API with JWT authentication, LLM integration, and real-time messaging",
    docs_url="/docs",  # Swagger UI documentation
    redoc_url="/redoc",  # ReDoc documentation
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


# ============================================================================
# CONFIGURE CORS MIDDLEWARE
# ============================================================================

# Add CORS middleware to allow requests from the frontend
# This is essential for the Next.js frontend to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # List of allowed origins from settings
    allow_credentials=True,  # Allow cookies and authorization headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# ============================================================================
# INCLUDE API ROUTERS
# ============================================================================

# Include authentication router
# All routes from this router will be prefixed with /api/v1/auth
app.include_router(
    auth.router,
    prefix=settings.API_V1_STR,
    tags=["authentication"]
)

# Include users router
# All routes from this router will be prefixed with /api/v1/users
app.include_router(
    users.router,
    prefix=settings.API_V1_STR,
    tags=["users"]
)

# Include roles router
# All routes from this router will be prefixed with /api/v1/roles
app.include_router(
    roles.router,
    prefix=settings.API_V1_STR,
    tags=["roles"]
)

# Include MFA router
# All routes from this router will be prefixed with /api/v1/auth/mfa
app.include_router(
    mfa.router,
    prefix=settings.API_V1_STR,
    tags=["mfa"]
)

# TODO: Include other routers as they are created
# app.include_router(chat.router, prefix=settings.API_V1_STR)
# app.include_router(messages.router, prefix=settings.API_V1_STR)


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get(
    "/",
    tags=["root"],
    summary="Root endpoint",
    description="Returns basic API information"
)
def read_root():
    """
    Root endpoint
    
    Returns basic information about the API.
    Useful for health checks and verifying the API is running.
    
    Returns:
        dict: API information
        
    Example Response:
        ```json
        {
            "message": "Admin Dashboard API",
            "version": "1.0.0",
            "docs": "/docs"
        }
        ```
    """
    return {
        "message": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.get(
    "/health",
    tags=["health"],
    summary="Health check",
    description="Check if the API and database are healthy"
)
def health_check():
    """
    Health check endpoint
    
    Verifies that the API is running and the database connection is working.
    Useful for monitoring and load balancers.
    
    Returns:
        dict: Health status
        
    Example Response:
        ```json
        {
            "status": "healthy",
            "database": "connected"
        }
        ```
    """
    # Check database connection
    db_status = "connected" if check_db_connection() else "disconnected"
    
    return {
        "status": "healthy",
        "database": db_status,
        "version": settings.VERSION
    }


# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Startup event handler
    
    This function runs when the application starts.
    Use it to:
    - Initialize database connections
    - Load ML models
    - Set up background tasks
    - Perform health checks
    """
    print(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"🔧 Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Not configured'}")
    
    # Check database connection
    if check_db_connection():
        print("✅ Database connection successful")
    else:
        print("❌ Database connection failed")


# ============================================================================
# SHUTDOWN EVENT
# ============================================================================

@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler
    
    This function runs when the application shuts down.
    Use it to:
    - Close database connections
    - Clean up resources
    - Save state
    """
    print(f"👋 Shutting down {settings.PROJECT_NAME}")


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler
    
    Catches all unhandled exceptions and returns a consistent error response.
    In production, you should log these errors to a monitoring service.
    
    Args:
        request: The request that caused the exception
        exc: The exception that was raised
        
    Returns:
        JSONResponse: Error response
    """
    # In production, log this to a monitoring service (e.g., Sentry)
    print(f"❌ Unhandled exception: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.LOG_LEVEL == "DEBUG" else "An error occurred"
        }
    )


# ============================================================================
# MAIN ENTRY POINT (for running directly with python)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    # In production, use a production-grade ASGI server like Gunicorn with Uvicorn workers
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (development only)
        log_level="info"
    )
