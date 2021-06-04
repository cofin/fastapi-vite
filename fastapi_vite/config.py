from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    # Application settings
    STATIC_URL: str = "/static"
    STATIC_PATH: str = "static/"
    VITE_DEV_MODE: bool = True
    VITE_ASSETS_PATH: str = "static/"
    VITE_MANIFEST_PATH: Optional[str]

    @validator("VITE_MANIFEST_PATH", pre=True)
    def assemble_manifest_path(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        path: str
        if v:
            return v

        if values.get("VITE_DEV_MODE"):
            path = values.get("VITE_ASSETS_PATH")

        else:
            path = values.get("STATIC_PATH")

        return path

    VITE_WS_CLIENT: str = "@vite/client"
    VITE_SERVER_HOST: str = "localhost"
    VITE_SERVER_PROTOCOL: str = "http"
    VITE_SERVER_PORT: int = 3000
    VITE_REACTJS_HMR: bool = False
    VITE_ASSETS_URL: Optional[str]

    @validator("VITE_ASSETS_URL", pre=True)
    def assemble_asset_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        url: str
        if v:
            return v

        if values.get("VITE_DEV_MODE"):
            url = f"{values.get('VITE_SERVER_PROTOCOL')}://{values.get('VITE_SERVER_HOST')}:{values.get('VITE_SERVER_PORT')}"

        else:
            url = values.get("STATIC_URL")

        return url

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
