from abc import ABC, abstractmethod
from traceback import TracebackException
from typing import Any, Self, Type


class EventPublisher(ABC):
    """
    Abstract interface for publishing events/messages to a message broker.
    """

    @abstractmethod
    async def __aenter__(self) -> Self:
        """Connect to the message broker."""
        pass

    @abstractmethod
    async def publish(self, topic: str, message: dict[str, Any]) -> None:
        """
        Publish a message to the specified topic.

        :param topic: The topic to publish the message to
        :param message: The message content as a dictionary
        """
        pass

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: Type[Exception] | None,
        exc_value: Exception | None,
        traceback: TracebackException,
    ) -> None:
        """Stop the connection to the message broker."""
        pass
