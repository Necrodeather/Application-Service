from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import DateTime, MetaData, String, Text
from sqlalchemy.orm import DeclarativeBase, mapped_column, registry
from sqlalchemy_utils import UUIDType

uuid_pk = Annotated[
    UUID,
    mapped_column(
        UUIDType(binary=False),
        primary_key=True,
        default=uuid4,
    ),
]

uuid = Annotated[UUID, False]
str_64 = Annotated[str, 64]
datetime_timezone = Annotated[datetime, True]
text = Annotated[str, str]

meta = MetaData(
    naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s',
    },
)


class Base(DeclarativeBase):
    """Base class for all database models."""

    metadata = meta

    registry = registry(
        type_annotation_map={
            text: Text,
            str_64: String(64),
            datetime_timezone: DateTime(timezone=True),
        },
    )
