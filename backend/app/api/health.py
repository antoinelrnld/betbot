from typing import Annotated, Literal, cast

from fastapi import APIRouter, Depends, Request, Response, status
from pydantic import BaseModel

from app.infrastructure.database import DatabaseReadiness

router = APIRouter(tags=["health"])


class LivenessResponse(BaseModel):
    status: Literal["ok"]


class ReadinessResponse(BaseModel):
    status: Literal["ok", "unavailable"]
    database: Literal["ok", "unavailable"]


def get_database_readiness(request: Request) -> DatabaseReadiness:
    """Retrieve the app-owned database readiness dependency."""
    return cast(DatabaseReadiness, request.app.state.database)


@router.get("/health", response_model=LivenessResponse)
async def health_check() -> LivenessResponse:
    """Report that the API process is running."""
    return LivenessResponse(status="ok")


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ReadinessResponse}},
)
async def readiness_check(
    response: Response,
    database: Annotated[DatabaseReadiness, Depends(get_database_readiness)],
) -> ReadinessResponse:
    """Report whether the API can serve database-backed requests."""
    if await database.is_available():
        return ReadinessResponse(status="ok", database="ok")

    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return ReadinessResponse(status="unavailable", database="unavailable")
