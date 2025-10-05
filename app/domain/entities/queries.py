from pydantic import BaseModel, Field, ValidationInfo, field_validator

MAX_PER_PAGE = 50
MIN_PER_PAGE = 25


class BaseQuery(BaseModel):
    """Base class for all query models."""

    size: int = Field(
        MIN_PER_PAGE,
        ge=MIN_PER_PAGE,
        le=MAX_PER_PAGE,
        description=f'Items per page (min {MIN_PER_PAGE}, max {MAX_PER_PAGE})',
    )
    page: int | None = Field(
        default=None,
        description='Page number to retrieve.',
    )

    @field_validator('size')
    @classmethod
    def limit(cls, value: int) -> int:
        """Limits the number of items per page.

        :param value: The number of items per page.
        :type value: int
        :returns: The limited number of items per page.
        :rtype: int
        """
        return MAX_PER_PAGE if value >= MAX_PER_PAGE else MIN_PER_PAGE

    @field_validator('page')
    @classmethod
    def offset(cls, value: int | None, values: ValidationInfo) -> int | None:
        """Calculates the offset for pagination.

        :param value: The page number.
        :type value: int | None
        :param values: The validation info.
        :type values: ValidationInfo
        :returns: The offset for pagination.
        :rtype: int | None
        """
        return (value - 1) * values.data['size'] if value else None


class ApplicationQuery(BaseQuery):
    user_name: str | None = Field(
        description='Match against user_name using operator.',
        default=None,
    )
