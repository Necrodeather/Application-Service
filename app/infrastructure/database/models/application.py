from sqlalchemy import Index
from sqlalchemy.orm import Mapped

from infrastructure.database.base import str_64, text

from .mixins import BaseMixin, CreatedAtMixin


class Application(BaseMixin, CreatedAtMixin):
    """Model for applications."""

    __tablename__ = 'applications'

    user_name: Mapped[str_64]
    description: Mapped[text]

    __table_args__ = (
        Index(
            'ix_user_name_trgm',
            'user_name',
            postgresql_using='gin',
            postgresql_ops={'user_name': 'gin_trgm_ops'},
        ),
    )
