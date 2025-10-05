from aiokafka.errors import KafkaConnectionError
from fastapi import Request
from fastapi.responses import JSONResponse

from core.logger import get_logger
from domain.exceptions import (
    NotFoundError,
)

logger = get_logger(__name__)


async def kafka_connection_error(
    request: Request,
    exc: KafkaConnectionError,
) -> JSONResponse:
    """Handles Kafka connection error exceptions.

    :param request: The request that caused the exception.
    :type request: Request
    :param exc: The exception that was raised.
    :type exc: KafkaConnectionError
    :returns: A JSON response with a 503 status code.
    :rtype: JSONResponse
    """
    logger.error('Kafka connection error: ', extra={'url': str(request.url)})
    return JSONResponse(
        status_code=503,
        content={'message': 'Unable to connect to Kafka'},
    )


async def database_connection_error(
    request: Request,
    exc: ConnectionRefusedError,
) -> JSONResponse:
    """Handles database connection error exceptions.

    :param request: The request that caused the exception.
    :type request: Request
    :param exc: The exception that was raised.
    :type exc: ConnectionRefusedError
    :returns: A JSON response with a 503 status code.
    :rtype: JSONResponse
    """
    logger.error(
        f'Database connection error: {str(exc)}',
        extra={'url': str(request.url)},
    )
    return JSONResponse(
        status_code=503,
        content={'message': 'Unable to connect to the database'},
    )


async def not_found(
    request: Request,
    exc: NotFoundError,
) -> JSONResponse:
    """Handles the NotFoundError exception.

    :param request: The request that caused the exception.
    :type request: Request
    :param exc: The exception that was raised.
    :type exc: NotFoundError
    :returns: A JSON response with a 404 status code.
    :rtype: JSONResponse
    """
    return JSONResponse(
        status_code=404,
        content={'message': exc.message},
    )


error_handlers = [
    not_found,  # 404
    kafka_connection_error,  # 503
    database_connection_error,  # 503
]
