"""Runtime PostgreSQL connectivity support."""

from collections.abc import Awaitable
from typing import Protocol

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


class DatabaseReadiness(Protocol):
    """Provide the database operations required by readiness checks."""

    def is_available(self) -> Awaitable[bool]:
        """Return whether PostgreSQL can accept a simple query."""

    def dispose(self) -> Awaitable[None]:
        """Release database resources during application shutdown."""


class Database:
    """Own the application's async PostgreSQL engine."""

    def __init__(self, database_url: str) -> None:
        self._engine: AsyncEngine = create_async_engine(database_url)

    async def is_available(self) -> bool:
        """Probe PostgreSQL without depending on application schema."""
        try:
            async with self._engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
        except (OSError, SQLAlchemyError):
            return False
        return True

    async def dispose(self) -> None:
        """Dispose pooled connections during graceful shutdown."""
        await self._engine.dispose()
