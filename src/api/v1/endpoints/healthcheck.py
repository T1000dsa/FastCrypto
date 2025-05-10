from fastapi import APIRouter
import logging

from src.core.dependencies.db_helper import DBDI
from src.core.config.settings import settings


router = APIRouter()
logger = logging.getLogger(__name__)

@router.get('/ping')
async def some_func(db:DBDI):
    logger.info(f'{db.is_active=}')
    logger.info(f'{settings}')
    logger.info('Everything is fine.')
    return 'pong'