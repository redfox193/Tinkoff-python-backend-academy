import os

from pydantic import BaseSettings

env_file = os.path.dirname(__file__) + "/.env.app"


class AppSetting(BaseSettings):
    log_level: str = 'DEBUG'
    enable_file_logging: bool = False
    api_version: str = 'v1'
    weather_server_url: str = "http://localhost:8080/api"
    reserve_weather_server_url: str = "http://localhost:8081/weather"
    app_files_dir: str = os.path.dirname(__file__) + "/../files"

    class Config:
        env_prefix = 'APP_'
        env_file = env_file


app_settings = AppSetting()
