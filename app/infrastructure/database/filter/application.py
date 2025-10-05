from sqlalchemy import BinaryExpression, and_

from domain.entities.queries import ApplicationQuery
from infrastructure.database.filter.base import BaseFilter


class ApplicationFilter(BaseFilter):
    """Filter for applications."""

    def where(self, query: ApplicationQuery) -> BinaryExpression | None:
        """Creates a where clause for a application query.

        :param query: The application query.
        :type query: ApplicationQuery
        :returns: A where clause for a application query.
        :rtype: BinaryExpression | None
        """

        if query.user_name:
            return and_(self._model.user_name.ilike(f'%{query.user_name}%'))

        return None
