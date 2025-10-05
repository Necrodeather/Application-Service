from abc import ABC, abstractmethod
from typing import Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import BinaryExpression

from infrastructure.database.base import Base

ModelType = TypeVar('ModelType', bound=Base)
QueryType = TypeVar('QueryType', bound=BaseModel)


class BaseFilter(ABC):
    """Base class for all filters."""

    def __init__(
        self,
        model: Type[ModelType],
    ) -> None:
        """Initializes the filter.

        :param model: The database model.
        :type model: Type[ModelType]
        """
        self._model = model

    @abstractmethod
    def where(self, query: QueryType) -> BinaryExpression | None:
        """Creates a where clause for a query.

        :param query: The query model.
        :type query: QueryType
        :returns: A where clause for a query.
        :rtype: BinaryExpression | None
        """
        raise NotImplementedError()
