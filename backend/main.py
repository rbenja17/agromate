"""FastAPI main application."""

import logging
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import news_router
from routers.trends import router as trends_router
from schemas import HealthResponse
from database import get_supabase_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup/shutdown events.
    """
    # Startup
    logger.info("🚀 Agromate API starting up...")
    
    # Test database connection
    try:
        client = get_supabase_client()
        logger.info(f"✅ Connected to Supabase: {client.supabase_url}")
    except Exception as e:
        logger.error(f"❌ Failed to connect to database: {e}")
    
    yield
    
    # Shutdown
    logger.info("👋 Agromate API shutting down...")


# Initialize FastAPI app
app = FastAPI(
    title="Agromate API",
    description="API REST para análisis de sentimiento del mercado agropecuario argentino (Matba Rofex)",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# Configure CORS - Production origins
import os

# Allowed origins for CORS
# Using wildcard for initial deployment - can be restricted later
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://agromate.pages.dev",
]

# For stricter security later, use:
# ALLOWED_ORIGINS = [
#     "https://agromate.pages.dev",
#     "https://*.pages.dev",
#     "http://localhost:3000",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Include routers
app.include_router(news_router)
app.include_router(trends_router)


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint - API information.
    """
    return {
        "name": "Agromate API",
        "version": "1.0.0",
        "description": "Análisis de sentimiento para mercado agropecuario argentino",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "news": "/api/news",
            "stats": "/api/stats",
            "recent": "/api/recent",
            "pipeline": "/api/pipeline/run",
            "trends_daily": "/api/trends/daily",
            "trends_by_source": "/api/trends/by-source",
            "trends_timeline": "/api/trends/timeline"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """
    Health check endpoint to verify service status.
    
    Returns:
        Service health status and database connectivity
    """
    try:
        # Test database connection
        client = get_supabase_client()
        db_status = "connected"
        
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = f"error: {str(e)}"
    
    return HealthResponse(
        status="healthy" if db_status == "connected" else "degraded",
        timestamp=datetime.utcnow(),
        database=db_status
    )


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler."""
    return {
        "error": "Not Found",
        "message": f"The endpoint {request.url.path} does not exist",
        "status_code": 404
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler."""
    logger.error(f"Internal server error: {exc}")
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "status_code": 500
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Agromate API server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
