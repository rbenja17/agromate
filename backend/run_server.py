"""Simple script to run the Agromate API server."""

import uvicorn
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("="*80)
    logger.info("🌾 Starting Agromate API Server")
    logger.info("="*80)
    logger.info("")
    logger.info("📡 Server will start on: http://localhost:8000")
    logger.info("📚 API Documentation: http://localhost:8000/docs")
    logger.info("🔍 Alternative docs: http://localhost:8000/redoc")
    logger.info("")
    logger.info("Press CTRL+C to stop the server")
    logger.info("="*80)
    logger.info("")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )
