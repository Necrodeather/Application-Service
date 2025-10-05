from enum import StrEnum, auto
from typing import TypeVar

from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

TSettings = TypeVar('TSettings', bound=BaseSettings)


def get_settings(cls: type[TSettings]) -> TSettings:
    return cls()


class DatabaseSettings(BaseSettings):
    """Pydantic model for database settings.

    This model contains the configuration for connecting to a PostgreSQL
    database using SQLAlchemy.

    :param driver: The driver to use when connecting to the database.
    :type driver: str
    :param user: The username to use when connecting to the database.
    :type user: str
    :param password: The password to use when connecting to the database.
    :type password: str
    :param host: The hostname of the database server.
    :type host: str, optional
    :param port: The port number of the database server.
    :type port: int, optional
    :param db: The name of the database to connect to.
    :type db: str
    :param echo: Whether to enable logging of SQL statements.
    :type echo: bool, optional
    :param uri: The connection URI for connecting to the database.
    :type uri: str, optional
    """

    model_config = SettingsConfigDict(
        env_file='./.env',
        env_prefix='postgres_',
        extra='ignore',
    )

    driver: str = 'postgresql+asyncpg'
    user: str
    password: str
    host: str = 'postgres'
    port: int = 5432
    db: str = 'applications'
    echo: bool = False
    uri: str = ''

    @field_validator('uri')
    @classmethod
    def get_uri(cls, value: str, values: ValidationInfo) -> str:
        """Generates a connection URI for connecting to the database.

        :param value: The current value of the `uri` field. If provided, it
        will be returned as-is.
        :type value: str
        :param values: A dictionary containing the values of all
        fields in the model.
        :type values: ValidationInfo
        :returns: The connection URI for connecting to the database.
        :rtype: str
        """
        if value:
            return value
        driver = values.data['driver']
        user = values.data['user']
        password = values.data['password']
        host = values.data['host']
        port = values.data['port']
        db = values.data['db']
        return f'{driver}://{user}:{password}@{host}:{port}/{db}'


class AppSettings(BaseSettings):
    """Pydantic model for application settings.

    This model contains the configuration for running a web application using
    FastAPI and Uvicorn.

    :param host: The hostname to bind the server to.
    :type host: str, optional
    :param port: The port number to listen on. Defaults to 8000.
    :type port: int, optional
    """

    class LogLevel(StrEnum):
        debug = auto()
        info = auto()
        warning = auto()
        error = auto()

    model_config = SettingsConfigDict(
        env_file='./.env',
        env_prefix='app_',
        extra='ignore',
    )
    host: str = 'backend'
    port: int = 8000
    log_level: LogLevel
    debug_reload: bool = False
    workers: int = 1


class KafkaSettings(BaseSettings):
    """Pydantic model for Kafka settings.

    This model contains the configuration for connecting to a Kafka
    message broker.

    :param host: The hostname of the Kafka server.
    :type host: str
    :param port: The port number of the Kafka server.
    :type port: int
    :param uri: The connection URI for connecting to Kafka.
    :type uri: str, optional
    """

    model_config = SettingsConfigDict(
        env_file='./.env',
        env_prefix='kafka_',
        extra='ignore',
    )

    host: str = "kafka"
    port: int = 9092
    uri: str = ''

    @field_validator('uri')
    @classmethod
    def get_uri(cls, value: str, values: ValidationInfo) -> str:
        """Generates a connection URI for connecting to Kafka.

        :param value: The current value of the `uri` field. If provided, it
        will be returned as-is.
        :type value: str
        :param values: A dictionary containing the values of all
        fields in the model.
        :type values: ValidationInfo
        :returns: The connection URI for connecting to Kafka.
        :rtype: str
        """
        if value:
            return value
        host = values.data['host']
        port = values.data['port']
        return f'{host}:{port}'


class CORSSettings(BaseSettings):
    """Pydantic model for CORS settings.

    This model contains the configuration for Cross-Origin Resource Sharing.

    :param allow_origins: List of origins that are allowed to make requests
    :type allow_origins: list[str]
    :param allow_credentials: Whether to allow credentials in requests
    :type allow_credentials: bool
    :param allow_methods: List of HTTP methods that are allowed
    :type allow_methods: list[str]
    :param allow_headers: List of headers that are allowed
    :type allow_headers: list[str]
    """

    model_config = SettingsConfigDict(
        env_file='./.env',
        env_prefix='cors_',
        extra='ignore',
    )

    allow_origins: list[str] = ['http://localhost', 'http://127.0.0.1']
    allow_credentials: bool = True
    allow_methods: list[str] = ['GET', 'POST']
    allow_headers: list[str] = [
        'Content-Type',
        'Authorization',
        'X-Requested-With',
        'Accept',
        'Origin',
    ]


cors_settings: CORSSettings = get_settings(CORSSettings)
app_settings: AppSettings = get_settings(AppSettings)
