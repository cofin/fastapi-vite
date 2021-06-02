try:
    import orjson as json

except ImportError:  # pragma: nocover
    import json

from pathlib import Path
from urllib.parse import urljoin

from jinja2 import Markup

from .config import settings


class ViteAssetLoader(object):
    _instance = None
    _encoding: str = settings.__config__.env_file_encoding
    _manifest: dict = {}
    _manifest_path: str = None

    def __init__(self):
        raise RuntimeError("Call instance() instead")

    @classmethod
    def instance(
        cls,
        manifest_path: str = f"{settings.STATIC_PATH}/{settings.VITE_MANIFEST_PATH}",
    ):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
            cls._encoding = settings.__config__.env_file_encoding
            cls._manifest_path = manifest_path
            cls._manifest = json.loads(Path(manifest_path).read_text(cls._encoding))
        return cls._instance

    def asset_url(self, path: str) -> str:
        """
        Generates only the URL of an asset managed by ViteJS.
        Warning, this function does not generate URLs for dependant assets.
        Arguments:
            path {str} -- Path to a Vite asset.
        Raises:
            RuntimeError: If cannot find the asset path in the manifest (only in production).
        Returns:
            str -- The URL of this asset.
        """
        static_url: str
        full_url: str
        if path not in self._manifest:
            raise RuntimeError(
                f"Cannot find {path} in Vite manifest " f"at {self._manifest_path}"
            )
        if settings.VITE_DEV_MODE:
            static_url = f"{settings.VITE_DEV_SERVER_PROTOCOL}://{settings.VITE_DEV_SERVER_HOST}:{settings.VITE_DEV_SERVER_PORT}/"
            full_url = urljoin(static_url, urljoin(static_url, path))
        else:
            static_url = f"{settings.STATIC_URL}"
            full_url = urljoin(static_url, self._manifest[path]["file"])
        return full_url


def render_vite_hmr_client(react_enabled: bool = settings.VITE_DEV_REACTJS) -> Markup:
    """
    Generates the script tag for the Vite WS client for HMR.
    Only used in development, in production this method returns
    an empty string.

    If react is enabled,
    Returns:
        str -- The script tag or an empty string.
    """
    tags: list = []
    if settings.VITE_DEV_MODE:
        tags.append(
            f"""
            <script type="text/javascript" src="{settings.VITE_DEV_SERVER_PROTOCOL}://{settings.VITE_DEV_SERVER_HOST}:{settings.VITE_DEV_SERVER_PORT}/{settings.VITE_DEV_WS_CLIENT}"></script>
            """
        )
    if react_enabled:
        tags.append(
            f"""
                <script type="module" >
                    import RefreshRuntime from '{settings.VITE_DEV_SERVER_PROTOCOL}://{settings.VITE_DEV_SERVER_HOST}:{settings.VITE_DEV_SERVER_PORT}/@react-refresh'
                    RefreshRuntime.injectIntoGlobalHook(window)
                    window.$RefreshReg$=()=> {{}}
                    window.$RefreshSig$=()= > (type) = > type
                    window.__vite_plugin_react_preamble_installed__=true
                </script >
                """
        )
    return Markup("\n".join(tags))


def asset_url(path: str) -> str:
    assert path is not None
    loader = ViteAssetLoader.instance()
    return loader.asset_url(path)
