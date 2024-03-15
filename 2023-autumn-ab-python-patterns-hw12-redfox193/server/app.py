import logging
import logging.config
from typing import Any

from fastapi import FastAPI, Request, Response

from config.settings import app_settings
from server.api.parents import router as parents_router
from server.api.weather import router as weather_router


class AppBuilder:
    def __init__(self) -> None:
        self.version: str = ''
        self.enable_file_logging: bool = False
        self.handlers = {
            "console": {
                "class": "logging.StreamHandler",
                "level": app_settings.log_level,
            }
        }

    def set_api_version(self, version: str) -> 'AppBuilder':
        self.version = f'{version}/'
        return self

    def enable_logging_to_file(self, enable: bool = False) -> 'AppBuilder':
        self.enable_file_logging = enable
        return self

    def build(self) -> FastAPI:
        app = FastAPI()

        if self.enable_file_logging:
            self.handlers["file"] = {
                "class": "logging.FileHandler",
                "filename": "log.txt",
                "level": app_settings.log_level,
            }

        logging_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": self.handlers,
            "root": {
                "handlers": list(self.handlers.keys()),
                "level": app_settings.log_level,
            },
        }
        logging.config.dictConfig(logging_config)

        if self.enable_file_logging:

            @app.middleware("http")
            async def log_requests(
                request: Request, call_next: Any
            ) -> Response:
                logger = logging.getLogger()
                logger.info("Request: %s %s", request.method, request.url)
                response: Response = await call_next(request)
                logger.info("Response: %s", response.status_code)
                return response

        app.include_router(
            parents_router,
            prefix=f'/api/{self.version}parents',
            tags=['ParentsSearch'],
        )
        app.include_router(
            weather_router,
            prefix=f'/api/{self.version}weather',
            tags=['WeatherReport'],
        )

        return app


def create_app(api_version: str, file_logging: bool) -> FastAPI:
    app_builder = AppBuilder()
    return (
        app_builder.set_api_version(api_version)
        .enable_logging_to_file(file_logging)
        .build()
    )
