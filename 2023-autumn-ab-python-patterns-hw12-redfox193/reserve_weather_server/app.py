import logging.config

from fastapi import FastAPI

from config.settings import app_settings
from reserve_weather_server.api.forecast import router as weather_router


def init_logger():
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": app_settings.log_level,
            },
        },
        "root": {
            "handlers": ["console"],
            "level": app_settings.log_level,
        },
    }

    logging.config.dictConfig(logging_config)


def create_app() -> FastAPI:
    app = FastAPI()
    api_prefix = '/weather'
    app.include_router(weather_router, prefix=api_prefix, tags=['Weather'])
    return app
