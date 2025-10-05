from traceback import TracebackException
from typing import Any, Self, Type

from faststream.kafka import KafkaBroker

from core.logger import get_logger

from .base import EventPublisher

logger = get_logger(__name__)


class KafkaEventPublisher(EventPublisher):
    """Kafka implementation of the EventPublisher interface."""

    def __init__(self, url: str):
        """Initialize the KafkaEventPublisher.

        :param url: The Kafka broker URL.
        :type url: str
        """
        self._broker = KafkaBroker(url)

    async def __aenter__(self) -> Self:
        """Connect to the Kafka broker."""
        logger.info('Attempting to connect to Kafka broker')
        await self._broker.connect()
        logger.info('Successfully connected to Kafka broker')
        return self

    async def publish(self, topic: str, message: dict[str, Any]) -> None:
        """Publish a message to the specified Kafka topic.

        :param topic: The topic to publish the message to.
        :type topic: str
        :param message: The message content as a dictionary.
        :type message: dict[str, Any]
        """
        logger.debug(f"Publishing message to Kafka topic '{topic}'")
        await self._broker.publish(message, topic=topic)
        logger.debug(
            f"Successfully published message to Kafka topic '{topic}'"
        )

    async def __aexit__(
        self,
        exc_type: Type[Exception] | None,
        exc_value: Exception | None,
        traceback: TracebackException,
    ) -> None:
        """Stop the Kafka broker connection."""
        logger.info('Stopping Kafka broker connection')
        await self._broker.stop()
        logger.info('Successfully stopped Kafka broker connection')
