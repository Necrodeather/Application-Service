from domain.entities.application import ApplicationCreate
from infrastructure.database.models.application import Application

from .base import BaseRepository


class ApplicationRepository(BaseRepository[Application, ApplicationCreate]):
    """Repository for managing application entities in the database.

    Provides methods for creating, reading, updating, and deleting
    application records in the database.
    """

    pass
