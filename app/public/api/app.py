from typing import Any, Sequence

from dishka import Provider, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from core.config import cors_settings

from .error_handlers import error_handlers
from .utils import read_pyproject_toml
from .v1.routers import api_router


class Server:
    """Server configuration class to set up FastAPI application with
    dependencies."""

    app: FastAPI = FastAPI

    def __init__(self, app: FastAPI, providers: list[Provider]) -> None:
        """Initializes the server with FastAPI app and dependency providers.

        :param app: The FastAPI application instance.
        :type app: FastAPI
        :param providers: List of dependency injection providers.
        :type providers: list[Provider]
        """
        self.app = app
        self.container = make_async_container(*providers)

        setup_dishka(self.container, app)

        self._register_middleware(app)
        self._register_routers(app)
        self._base_information(app)
        self._register_exception_handlers(app, error_handlers)

    def get_app(self) -> FastAPI:
        """Returns the configured FastAPI application.

        :returns: Configured FastAPI application.
        :rtype: FastAPI
        """
        return self.app

    @staticmethod
    def _base_information(app: FastAPI) -> None:
        """Sets up basic OpenAPI information for the application.

        :param app: The FastAPI application instance.
        :type app: FastAPI
        """
        if app.openapi_schema:
            return app.openapi_schema

        project_info = read_pyproject_toml()
        app.openapi_schema = get_openapi(
            title=project_info['project']['name'],
            version=project_info['project']['version'],
            description=project_info['project']['description'],
            routes=app.routes,
        )

    @staticmethod
    def _register_middleware(app: FastAPI) -> None:
        """Registers middleware for the FastAPI application.

        :param app: The FastAPI application instance.
        :type app: FastAPI
        """
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_settings.allow_origins,
            allow_credentials=cors_settings.allow_credentials,
            allow_methods=cors_settings.allow_methods,
            allow_headers=cors_settings.allow_headers,
        )

    @staticmethod
    def _register_routers(app: FastAPI) -> None:
        """Registers API routers for the FastAPI application.

        :param app: The FastAPI application instance.
        :type app: FastAPI
        """
        app.include_router(api_router)

    @staticmethod
    def _register_exception_handlers(
        app: FastAPI,
        exception_handlers: Sequence[object],
    ) -> None:
        """Registers exception handlers for the FastAPI application.

        :param app: The FastAPI application instance.
        :type app: FastAPI
        :param exception_handlers: Sequence of exception handlers.
        :type exception_handlers: Sequence[object]
        """
        for handler in exception_handlers:
            app.add_exception_handler(handler.__annotations__['exc'], handler)


def create_app(
    providers: list[Provider],
    *args: Any,
    **kwargs: Any,
) -> FastAPI:
    app = FastAPI(*args, **kwargs)
    return Server(app=app, providers=providers).get_app()
