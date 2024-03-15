from config.settings import app_settings
from server.app import create_app

app = create_app(app_settings.api_version, app_settings.enable_file_logging)
