from fastapi import FastAPI

from app.api.health import router as health_router
from app.config import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(
        title="BetBot API",
        version="0.1.0",
    )
    application.state.settings = settings or get_settings()
    application.include_router(health_router)
    return application


app = create_app()
