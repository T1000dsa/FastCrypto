from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from logging.config import dictConfig
from fastapi import FastAPI
import uvicorn
import logging

from src.core.config.settings import settings
from src.core.dependencies.db_helper import db_helper
from src.core.config.logger import LOG_CONFIG

from src.api.v1.endpoints.healthcheck import router as health_router
from src.api.v1.endpoints.markets import router as markets_router
from src.api.v1.endpoints.orders import router as orders_router
from src.api.v1.endpoints.users import router as users_router
from src.api.v1.endpoints.wallets import router as wallets_router
from src.api.v1.auth.authentication import router as auth_router
from src.api.v1.endpoints.index import router as index_router
from src.api.v1.endpoints.general_work import router as general_router


app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    dictConfig(LOG_CONFIG)
    logger = logging.getLogger(__name__)
    logger.info(settings)
    logger.info(await db_helper.health_check())
    
    yield  # FastAPI handles requests here

    try:
        await db_helper.dispose()
        logger.info("✅ Connection pool closed cleanly")
    except Exception as e:
        logger.warning(f"⚠️ Error closing connection pool: {e}")


app = FastAPI(lifespan=lifespan, title='CryptoExchange MVP')

"""app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors,
    allow_methods=["*"],
    allow_headers=["*"]
)"""

app.include_router(health_router)
app.include_router(auth_router)

app.include_router(markets_router)
app.include_router(orders_router)
app.include_router(users_router)
app.include_router(wallets_router)
app.include_router(index_router)
app.include_router(general_router)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        log_config=LOG_CONFIG
        )