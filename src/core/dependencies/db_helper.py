from fastapi import Depends
from typing import AsyncGenerator, Annotated
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
    )
import logging

from src.core.config.settings import settings


logger = logging.getLogger(__name__)

class DbHelper:
    def __init__(
            self, 
            url:str, 
            echo:bool=True, 
            echo_pool:bool=False,
            pool_size:int=5,
            max_overflow:int=10):
        
        self.engine:AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow
        )
        
        self.session_factory:async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )
    async def dispose(self) -> None:
        await self.engine.dispose()
    
    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session

    async def health_check(self) -> bool:
        """Check database connectivity"""
        try:
            async for session in self.session_getter():  # Properly consume the async generator
                try:
                    await session.execute(text("SELECT 1"))  # Simple test query
                    return True
                finally:
                    await session.close()  # Ensure session is closed
            return False  # This line is theoretically unreachable
        
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False


db_helper = DbHelper(
    url=str(settings.db.give_url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow
)
DBDI = Annotated[AsyncSession, Depends(db_helper.session_getter)]
DBDI_WIPING = Annotated[AsyncSession, Depends(db_helper.dispose)]