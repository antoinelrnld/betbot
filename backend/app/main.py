from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.health import router as health_router
from app.config import Settings, get_settings
from app.infrastructure.database import Database


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    """Release application-owned infrastructure during shutdown."""
    yield
    await application.state.database.dispose()


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    application_settings = settings or get_settings()
    application = FastAPI(
        title="BetBot API",
        version="0.1.0",
        debug=application_settings.debug,
        lifespan=lifespan,
    )
    application.state.database = Database(application_settings.database_url)
    application.state.settings = application_settings
    application.include_router(health_router)
    return application


app = create_app()


def run() -> None:
    """Run the API server using the configured network address."""
    settings = get_settings()
    uvicorn.run(app, host=settings.app_host, port=settings.app_port)


if __name__ == "__main__":
    run()
