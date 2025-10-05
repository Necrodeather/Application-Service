from typing import Type
from uuid import UUID

from pydantic import BaseModel

from core.logger import get_logger
from domain.entities.queries import BaseQuery
from domain.exceptions import NotFoundError
from infrastructure.database.base import Base
from infrastructure.database.repository.base import BaseRepository

logger = get_logger(__name__)


class BaseService[
    CreateSchemaType: BaseModel,
    ReadSchemaType: BaseModel,
]:
    """Base class for all services."""

    def __init__(
        self,
        repository: BaseRepository[Base, CreateSchemaType],
        read_entity: Type[ReadSchemaType],
    ) -> None:
        """Initializes the service.

        :param repository: The repository for the service.
        :type repository: BaseRepository
        :param read_entity: The read entity for the service.
        :type read_entity: Type[ReadSchemaType]
        """
        self._repository = repository
        self._read_entity = read_entity

    async def get_multi(self, query: Type[BaseQuery]) -> list[ReadSchemaType]:
        """Gets multiple records.

        :param query: The query to filter the records.
        :type query: Type[BaseQuery]
        :returns: A list of records.
        :rtype: list[ReadSchemaType]
        """
        logger.debug(f'Getting multiple records with query: {query}')
        result = await self._repository.get_multi(query)
        if not result:
            logger.warning('No records found, raising NotFoundError')
            raise NotFoundError()
        logger.info(f'Retrieved {len(result)} records')
        return self._read_entity.from_list(result)

    async def create(self, entity: CreateSchemaType) -> ReadSchemaType:
        """Creates a new record.

        :param entity: The data to create the record with.
        :type entity: CreateSchemaType
        :returns: The created record.
        :rtype: ReadSchemaType
        """
        logger.debug(
            f'Creating new record of type {entity.__class__.__name__}'
        )
        result = await self._repository.create(entity)
        logger.info('Record created successfully')
        return self._read_entity.model_validate(result)

    async def delete_by_id(self, entity_id: UUID) -> None:
        """Deletes a record by its ID.

        :param entity_id: The ID of the record to delete.
        :type entity_id: UUID
        """
        await self._repository.delete_by_id(entity_id)
