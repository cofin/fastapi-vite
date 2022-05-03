# Standard Library
from typing import Any, Dict, Optional

# Third Party Libraries
from pydantic import BaseSettings, validator


class ViteSettings(BaseSettings):
    # Application settings
    static_url: Optional[str]

    @validator("static_url", pre=True)
    def ensure_slash_for_static_url(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> str:
        if v and v.endswith("/"):
            return v
        elif v:
            return f"{v}/"
        return "/static/"

    static_path: str = "static/"
    hot_reload: Optional[bool]
    is_react: bool = False

    @validator("hot_reload", pre=True)
    def detect_serve_mode(cls, v: Optional[bool], values: Dict[str, Any]) -> str:
        if v:
            return v
        elif values.get("DEBUG", None):
            return True
        return False

    assets_path: str = "static/"
    manifest_path: Optional[str]

    @validator("manifest_path", pre=True, always=True)
    def assemble_manifest_path(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        path: str = (
            values.get("assets_path")
            if values.get("hot_reload")
            else values.get("static_path")
        )
        return f"{path}/manifest.json"

    server_host: str = "localhost"
    server_protocol: str = "http"
    server_port: int = 3000

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "VITE_"


settings = ViteSettings()
