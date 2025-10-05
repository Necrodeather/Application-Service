from core.logger import get_logger
from domain.entities.application import ApplicationCreate, ApplicationRead
from infrastructure.broker.base import EventPublisher
from infrastructure.database.repository.application import (
    ApplicationRepository,
)

from .base import BaseService

logger = get_logger(__name__)


class ApplicationService(
    BaseService[
        ApplicationCreate,
        ApplicationRead,
    ]
):
    """Service for applications."""

    def __init__(
        self,
        repository: ApplicationRepository,
        read_entity: ApplicationRead,
        event_publisher: EventPublisher,
    ) -> None:
        super().__init__(repository, read_entity)
        self._event_publisher = event_publisher

    async def create_application(
        self,
        application: ApplicationCreate,
    ) -> ApplicationRead:
        """Creates a new application and publishes the event to Kafka.

        :param application: The application data to create.
        :type application: ApplicationCreate
        :returns: The created application.
        :rtype: ApplicationRead
        """
        logger.info(
            f'Creating new application for user: {application.user_name}'
        )
        result = await self.create(application)
        logger.info(f'Application created successfully, ID: {result.id}')

        logger.debug("Publishing application event to Kafka 'applications'")
        try:
            await self._publish_message(result)
        except Exception as exc:
            logger.error(
                f'Failed to publish to Kafka, deleting record {result.id}: '
                f'{str(exc)}'
            )
            await self.delete_by_id(result.id)
            raise exc

        logger.info(
            f'Application event published to Kafka successfully, '
            f'ID: {result.id}'
        )

        return result

    async def _publish_message(self, message: ApplicationRead) -> None:
        async with self._event_publisher as connect:
            await connect.publish(
                topic='applications',
                message=message.model_dump(),
            )
