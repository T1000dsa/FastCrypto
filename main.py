from contextlib import asynccontextmanager
from logging.config import dictConfig
from fastapi import FastAPI
import uvicorn
import logging

from src.core.config.settings import settings
from src.core.dependencies.db_helper import db_helper
from src.core.config.logger import LOG_CONFIG

from src.api.v1.endpoints.healthcheck import router as health_router
from src.api.v1.endpoints.index import router as index_router
from src.api.v1.auth.authentication import router as auth_router


app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    dictConfig(LOG_CONFIG)
    logger = logging.getLogger(__name__)
    
    yield  # FastAPI handles requests here

    try:
        await db_helper.dispose()
        logger.info("✅ Connection pool closed cleanly")
    except Exception as e:
        logger.warning(f"⚠️ Error closing connection pool: {e}")


app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
app.include_router(index_router)
app.include_router(auth_router)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.run.host,
        port=settings.run.port,
        reload=True
        )