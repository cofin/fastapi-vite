from enum import Enum

from pydantic import BaseSettings


class AppMode(Enum):
    DEV = "development"
    PROD = "production"


class Settings(BaseSettings):
    # Application settings
    ENVIRONMENT: AppMode = AppMode.PROD
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    STATIC_URL: str = "/static"
    STATIC_PATH: str = "static/"
    VITE_DEV_MODE: bool = True
    VITE_MANIFEST_PATH: str = "dist/manifest.json"
    VITE_ASSETS_PATH: str = "static/dist"
    VITE_DEV_WS_CLIENT: str = "@vite/client"
    VITE_DEV_SERVER_HOST: str = "localhost"
    VITE_DEV_SERVER_PROTOCOL: str = "http"
    VITE_DEV_SERVER_PORT: int = 3000
    VITE_DEV_REACTJS: bool = True

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def is_dev(self) -> bool:
        return self.ENVIRONMENT == AppMode.DEV


settings = Settings()
