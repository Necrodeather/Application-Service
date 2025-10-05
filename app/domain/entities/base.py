from typing import Any

from pydantic import BaseModel, ConfigDict


class BaseEntity(BaseModel):
    """Base class for all entities."""

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_list(cls, obj: Any) -> list[BaseModel]:
        """Creates a list of entities from a list of objects.

        :param obj: The list of objects to convert.
        :type obj: Any
        :returns: A list of entities.
        :rtype: list[BaseModel]
        """
        return [cls.model_validate(item) for item in obj]
