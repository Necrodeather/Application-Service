from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import (
    FastapiProvider,
)

from domain.entities.application import ApplicationRead
from infrastructure.broker.kafka_publisher import KafkaEventPublisher
from infrastructure.database.engine import SqlAlchemyEngine
from infrastructure.database.filter.application import ApplicationFilter
from infrastructure.database.models.application import Application
from infrastructure.database.repository.application import (
    ApplicationRepository,
)
from services.application import ApplicationService

from .config import DatabaseSettings, KafkaSettings, get_settings


class SqlAlchemyProvider(Provider):
    scope = Scope.APP

    @provide
    def get_database_settings(self) -> DatabaseSettings:
        return get_settings(DatabaseSettings)

    @provide
    async def engine(
        self,
        database_settings: DatabaseSettings,
    ) -> SqlAlchemyEngine:
        return SqlAlchemyEngine(
            database_settings.uri,
            database_settings.echo,
        )


class KafkaProvider(Provider):
    scope = Scope.APP

    @provide
    def get_kafka_settings(self) -> KafkaSettings:
        return get_settings(KafkaSettings)

    @provide
    async def kafka_event_publisher(
        self,
        kafka_settings: KafkaSettings,
    ) -> KafkaEventPublisher:
        return KafkaEventPublisher(kafka_settings.uri)


class ApplicationProvider(Provider):
    @provide(scope=Scope.APP)
    async def filter(self) -> ApplicationFilter:
        return ApplicationFilter(Application)

    @provide(scope=Scope.REQUEST)
    async def repository(
        self,
        engine: SqlAlchemyEngine,
        filter: ApplicationFilter,
    ) -> ApplicationRepository:
        return ApplicationRepository(engine, Application, filter)

    @provide(scope=Scope.REQUEST)
    async def service(
        self,
        repository: ApplicationRepository,
        kafka_event_publisher: KafkaEventPublisher,
    ) -> ApplicationService:
        return ApplicationService(
            repository, ApplicationRead, kafka_event_publisher
        )


providers = [
    SqlAlchemyProvider(),
    KafkaProvider(),
    ApplicationProvider(),
    FastapiProvider(),
]
