try:
    import orjson as json

except ImportError:  # pragma: nocover
    import json

from pathlib import Path
from typing import Dict, Optional
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

    def generate_vite_asset(
        self,
        path: str,
        scripts_attrs: Optional[Dict[str, str]] = None,
        with_imports: bool = True,
    ) -> str:
        """
        Generates all assets include tags for the file in argument.
        Generates all scripts tags for this file and all its dependencies
        (JS and CSS) by reading the manifest file (for production only).
        In development Vite imports all dependencies by itself.
        Place this tag in <head> section of yout page
        (this function marks automaticaly <script> as "async" and "defer").

        Arguments:
            path {str} -- Path to a Vite asset to include.

        Returns:
            str -- All tags to import this asset in yout HTML page.

        Keyword Arguments:
            scripts_attrs {Optional[Dict[str, str]]} -- Override attributes added to scripts tags. (default: {None})
            with_imports {bool} -- If generate assets for dependant assets of this one. (default: {True})

        Raises:
            RuntimeError: If cannot find the asset path in the manifest (only in production).

        Returns:
            str -- All tags to import this asset in yout HTML page.
        """

        if settings.VITE_DEV_MODE:
            return ViteAssetLoader._generate_script_tag(
                ViteAssetLoader._generate_vite_server_url(path),
                {"type": "module", "async": "", "defer": ""},
            )

        if path not in self._manifest:
            raise RuntimeError(
                f"Cannot find {path} in Vite manifest "
                f"at {settings.VITE_MANIFEST_PATH}"
            )

        tags = []
        manifest_entry = self._manifest[path]
        scripts_attrs = scripts_attrs or {"type": "module", "async": "", "defer": ""}

        # Add dependent CSS
        if "css" in manifest_entry:
            for css_path in manifest_entry["css"]:
                tags.append(
                    ViteAssetLoader._generate_stylesheet_tag(
                        urljoin(settings.STATIC_URL, css_path)
                    )
                )

        # Add dependent "vendor"
        if with_imports and "imports" in manifest_entry:
            for vendor_path in manifest_entry["imports"]:
                tags.append(
                    self.generate_vite_asset(
                        vendor_path,
                        scripts_attrs=scripts_attrs,
                        with_imports=with_imports,
                    )
                )

        # Add the script by itself
        tags.append(
            ViteAssetLoader._generate_script_tag(
                urljoin(settings.STATIC_URL, manifest_entry["file"]),
                attrs=scripts_attrs,
            )
        )

        return "\n".join(tags)

    def generate_vite_asset_url(self, path: str) -> str:
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

        if settings.VITE_DEV_MODE:
            return ViteAssetLoader._generate_vite_server_url(path)

        if path not in self._manifest:
            raise RuntimeError(
                f"Cannot find {path} in Vite manifest "
                f"at {settings.VITE_MANIFEST_PATH}"
            )

        return urljoin(settings.STATIC_URL, self._manifest[path]["file"])

    @classmethod
    def instance(
        cls,
        manifest_path: str = settings.VITE_MANIFEST_PATH,
    ):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
            cls._encoding = settings.__config__.env_file_encoding
            cls._manifest_path = manifest_path
            if not settings.VITE_DEV_MODE:
                cls._manifest = json.loads(Path(manifest_path).read_text(cls._encoding))
        return cls._instance

    @classmethod
    def generate_vite_ws_client(cls) -> str:
        """
        Generates the script tag for the Vite WS client for HMR.
        Only used in development, in production this method returns
        an empty string.

        Returns:
            str -- The script tag or an empty string.
        """

        if not settings.VITE_DEV_MODE:
            return ""

        return cls._generate_script_tag(
            cls._generate_vite_server_url(settings.VITE_WS_CLIENT),
            {"type": "module"},
        )

    @classmethod
    def generate_vite_react_hmr(cls) -> str:
        """
        Generates the script tag for the Vite WS client for HMR.
        Only used in development, in production this method returns
        an empty string.

        Returns:
            str -- The script tag or an empty string.
        """

        if not settings.VITE_DEV_MODE:
            return ""
        if settings.VITE_REACTJS_HMR:
            return f"""
                    <script type="module">
                    import RefreshRuntime from '{cls._generate_vite_server_url()}/@react-refresh'
                    RefreshRuntime.injectIntoGlobalHook(window)
                    window.$RefreshReg$ = () => {{}}
                    window.$RefreshSig$ = () => (type) => type
                    window.__vite_plugin_react_preamble_installed__=true
                    </script>
                    """
        else:
            return ""

    @staticmethod
    def _generate_script_tag(src: str, attrs: Optional[Dict[str, str]] = None) -> str:
        """
        Generates an HTML script tag.

        Arguments:
            src {str} -- Source of the script.

        Keyword Arguments:
            attrs {Optional[Dict[str, str]]} -- List of custom attributes for the tag (default: {None})

        Returns:
            str -- The script tag.
        """

        attrs_str = (
            " ".join([f'{key}="{value}"' for key, value in attrs.items()])
            if attrs is not None
            else ""
        )

        return f'<script {attrs_str} src="{src}"></script>'

    @staticmethod
    def _generate_stylesheet_tag(href: str) -> str:
        """
        Generates and HTML <link> stylesheet tag for CSS.

        Arguments:
            href {str} -- CSS file URL.

        Returns:
            str -- CSS link tag.
        """

        return f'<link rel="stylesheet" href="{href}" />'

    @staticmethod
    def _generate_vite_server_url(path: Optional[str] = None) -> str:
        """
        Generates an URL to and asset served by the Vite development server.

        Keyword Arguments:
            path {Optional[str]} -- Path to the asset. (default: {None})

        Returns:
            str -- Full URL to the asset.
        """

        return urljoin(settings.VITE_ASSETS_URL, path if path is not None else "")


def vite_hmr_client() -> Markup:
    """
    Generates the script tag for the Vite WS client for HMR.
    Only used in development, in production this method returns
    an empty string.

    If react is enabled,
    Returns:
        str -- The script tag or an empty string.
    """
    tags: list = []
    tags.append(ViteAssetLoader.generate_vite_react_hmr())
    tags.append(ViteAssetLoader.generate_vite_ws_client())
    return Markup("\n".join(tags))


def vite_asset(
    path: str, scripts_attrs: Optional[Dict[str, str]] = None, with_imports: bool = True
) -> Markup:
    """
    Generates all assets include tags for the file in argument.
    Generates all scripts tags for this file and all its dependencies
    (JS and CSS) by reading the manifest file (for production only).
    In development Vite imports all dependencies by itself.
    Place this tag in <head> section of yout page
    (this function marks automaticaly <script> as "async" and "defer").

    Arguments:
        path {str} -- Path to a Vite asset to include.

    Keyword Arguments:
        scripts_attrs {Optional[Dict[str, str]]} -- Override attributes added to scripts tags. (default: {None})
        with_imports {bool} -- If generate assets for dependant assets of this one. (default: {True})

    Returns:
        str -- All tags to import this asset in yout HTML page.
    """

    assert path is not None

    return Markup(
        ViteAssetLoader.instance().generate_vite_asset(
            path, scripts_attrs=scripts_attrs, with_imports=with_imports
        )
    )


def vite_asset_url(path: str) -> str:
    """
    Generates only the URL of an asset managed by ViteJS.
    Warning, this function does not generate URLs for dependant assets.

    Arguments:
        path {str} -- Path to a Vite asset.

    Returns:
        [type] -- The URL of this asset.
    """

    assert path is not None

    return ViteAssetLoader.instance().generate_vite_asset_url(path)
