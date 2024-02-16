# Standard Library
from typing import Optional

# Third Party Libraries
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ViteSettings(BaseSettings):
    # Application settings
    static_url: Optional[str] = None

    @field_validator("static_url", mode="before")
    @classmethod
    def ensure_slash_for_static_url(cls, v: Optional[str], info: ValidationInfo) -> str:
        if v and v.endswith("/"):
            return v
        elif v:
            return f"{v}/"
        return "/static/"

    static_path: str = "static/"
    hot_reload: Optional[bool] = None
    is_react: bool = False

    @field_validator("hot_reload", mode="before")
    @classmethod
    def detect_serve_mode(cls, v: Optional[bool], info: ValidationInfo) -> str:
        if v:
            return v
        elif info.data.get("DEBUG", None):
            return True
        return False

    assets_path: str = "static/"
    manifest_path: Optional[str]

    @field_validator("manifest_path", mode="before")
    @classmethod
    def assemble_manifest_path(cls, v: Optional[str], info: ValidationInfo) -> str:
        path: str = (
            info.data.get("assets_path")
            if info.data.get("hot_reload")
            else info.data.get("static_path")
        ).rstrip("/")
        return f"{path}/manifest.json"

    server_host: str = "localhost"
    server_protocol: str = "http"
    server_port: int = 3000

    model_config = SettingsConfigDict(
        extra="allow",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="VITE_",
    )


settings = ViteSettings()
