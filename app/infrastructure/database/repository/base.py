from typing import Any, Sequence, Type

from pydantic import BaseModel
from sqlalchemy import (
    delete,
    insert,
    select,
)

from core.logger import get_logger
from domain.entities.queries import BaseQuery
from infrastructure.database.base import Base
from infrastructure.database.engine import SqlAlchemyEngine
from infrastructure.database.filter.base import BaseFilter

logger = get_logger(__name__)


class BaseRepository[
    ModelType: Base,
    CreateSchemaType: BaseModel,
]:
    """Base class for all repositories."""

    def __init__(
        self,
        engine: SqlAlchemyEngine,
        model: Type[ModelType],
        filter: BaseFilter,
    ) -> None:
        """Initializes the repository.

        :param engine: The database engine.
        :type engine: SqlAlchemyEngine
        :param model: The database model.
        :type model: Type[ModelType]
        :param filter: The filter for the model.
        :type filter: BaseFilter
        """
        self._model = model
        self._engine = engine
        self._filter = filter

    async def get_multi(
        self,
        query: Type[BaseQuery],
    ) -> Sequence[ModelType]:
        """Gets multiple records from the database.

        :param query: The query to filter the records.
        :type query: Type[BaseQuery]
        :returns: A list of records.
        :rtype: Sequence[ModelType]
        """
        logger.debug(
            f'Getting multiple records of type {self._model.__name__}'
        )

        stmt = select(self._model).limit(query.size)

        where_expression = self._filter.where(query)
        if where_expression is not None:
            logger.debug(f'Applying filter: {where_expression}')
            stmt = stmt.where(where_expression)

        if query.page:
            logger.debug(f'Applying offset: {query.page}')
            stmt = stmt.offset(query.page)

        async with self._engine.session() as session:
            result = await session.execute(stmt)
        records = result.scalars().all()
        logger.info(
            f'Retrieved {len(records)} records of type {self._model.__name__}'
        )
        return records

    async def create(self, object: CreateSchemaType) -> ModelType:
        """Creates a new record.

        :param object: The data to create the record with.
        :type object: CreateSchemaType
        :returns: The created record.
        :rtype: ModelType
        """
        logger.debug(f'Creating new record of type {self._model.__name__}')

        stmt = (
            insert(self._model)
            .values(object.model_dump())
            .returning(self._model)
        )

        async with self._engine.session() as session:
            async with session.begin():
                result = await session.execute(stmt)
                await session.commit()
        record = result.scalar()
        logger.info(
            f'Created record ID: {
                record.id if hasattr(record, "id") else "unknown"
            }'
        )
        return record

    async def delete_by_id(self, entity_id: Any) -> None:
        """Deletes a record by its ID.

        :param entity_id: The ID of the record to delete.
        :type entity_id: Any
        """
        stmt = delete(self._model).where(self._model.id == entity_id)
        async with self._engine.session() as session:
            await session.execute(stmt)
            await session.commit()
