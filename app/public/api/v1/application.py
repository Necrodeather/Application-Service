from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query

from domain.entities.application import ApplicationCreate, ApplicationRead
from domain.entities.queries import ApplicationQuery
from services.application import ApplicationService

application_router = APIRouter(prefix='/applications')


@application_router.get('')
@inject
async def get(
    service: FromDishka[ApplicationService],
    query: Annotated[ApplicationQuery, Query()],
) -> list[ApplicationRead]:
    """Get a list of applications with optional filtering and pagination."""
    return await service.get_multi(query)


@application_router.post('')
@inject
async def create(
    service: FromDishka[ApplicationService],
    application: ApplicationCreate,
) -> ApplicationRead:
    """Create a new application."""
    return await service.create_application(application)
