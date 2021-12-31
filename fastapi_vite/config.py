from typing import Any, Dict, Optional

from pydantic import BaseSettings, validator


class ViteSettings(BaseSettings):
    # Application settings
    STATIC_URL: str = "/static/"  # must end with a slash
    STATIC_PATH: str = "static/"
    VITE_SERVE_MODE: Optional[bool]

    @validator("VITE_SERVE_MODE", pre=True)
    def detect_serve_mode(cls, v: Optional[bool], values: Dict[str, Any]) -> str:
        url: str
        if v:
            return v

        if values.get("DEBUG"):
            return True

        else:
            return False

    VITE_ASSETS_PATH: str = "static/"
    VITE_MANIFEST_PATH: Optional[str] = "static/manifest.json"

    @validator("VITE_MANIFEST_PATH", pre=True)
    def assemble_manifest_path(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        path: str
        if v:
            return v

        if values.get("VITE_SERVE_MODE"):
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

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = ViteSettings()
