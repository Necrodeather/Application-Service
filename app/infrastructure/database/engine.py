from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.logger import get_logger

logger = get_logger(__name__)


class SqlAlchemyEngine:
    """A wrapper around the SQLAlchemy async engine and session factory."""

    def __init__(self, uri: str, echo: bool = False) -> None:
        """Initializes the engine.

        :param uri: The database URI.
        :type uri: str
        :param echo: Whether to echo SQL statements.
        :type echo: bool
        """
        logger.info("Initializing database engine")
        self._engine = create_async_engine(url=uri, echo=echo)
        self._session_factory = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
            autoflush=False,
        )
        logger.info("Database engine initialized successfully")

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Provides a session to interact with the database.

        :returns: An async session.
        :rtype: AsyncGenerator[AsyncSession, None]
        """
        logger.debug("Creating database session")
        async with self._session_factory() as session:
            logger.debug("Database session created")
            try:
                yield session
            finally:
                logger.debug("Database session closed")
