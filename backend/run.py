"""Entry point for running the backend server"""

if __name__ == "__main__":
    import uvicorn
    from app.config import API_HOST, API_PORT, DEBUG
    
    uvicorn.run(
        "app.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=DEBUG
    )
