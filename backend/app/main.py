"""
Main FastAPI application
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import DEBUG, API_PORT
from app.database import init_db
from app.api import router


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI app
    """
    # Startup
    logger.info("NeuroTask backend starting...")
    init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("NeuroTask backend shutting down...")


# Create FastAPI app
app = FastAPI(
    title="NeuroTask API",
    description="AI-powered NLP To-Do List Application",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "NeuroTask API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=API_PORT,
        reload=DEBUG
    )
