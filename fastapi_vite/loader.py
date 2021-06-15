try:
    import orjson as json

except ImportError:  # pragma: nocover
    import json

from pathlib import Path
from typing import Dict, Optional
from urllib.parse import urljoin

from jinja2 import Markup

from .config import settings
from typing import ClassVar


class ViteLoader(object):
    """Vite  manifest loader"""

    _instance = None
    _manifest: ClassVar[dict]

    def __new__(cls):
        """Singleton manifest loader"""
        if cls._instance is not None:
            return cls._instance
        cls._instance = super().__new__(cls)
        cls._instance.parse_manifest()
        return cls._instance

    def parse_manifest(self) -> None:
        """
        Read and parse the Vite manifest file.

        Raises:
            RuntimeError: if cannot load the file or JSON in file is malformed.
        """
        if not settings.VITE_SERVE_MODE:
            with open(settings.VITE_MANIFEST_PATH, "r") as manifest_file:
                manifest_content = manifest_file.read()
            try:
                self._manifest = json.loads(manifest_content)
            except Exception:
                raise RuntimeError(
                    "Cannot read Vite manifest file at {path}".format(
                        path=settings.VITE_MANIFEST_PATH,
                    )
                )

    def generate_vite_server_url(self, path: Optional[str] = None) -> str:
        """
        Generates an URL to and asset served by the Vite development server.

        Keyword Arguments:
            path {Optional[str]} -- Path to the asset. (default: {None})

        Returns:
            str -- Full URL to the asset.
        """
        base_path = "{protocol}://{host}:{port}".format(
            protocol=settings.VITE_SERVER_PROTOCOL,
            host=settings.VITE_SERVER_HOST,
            port=settings.VITE_SERVER_PORT,
        )
        return urljoin(
            base_path,
            urljoin(settings.STATIC_URL, path if path is not None else ""),
        )

    def generate_script_tag(
        self, src: str, attrs: Optional[Dict[str, str]] = None
    ) -> str:
        """Generates an HTML script tag."""
        attrs_str: str = ""
        if attrs is not None:
            attrs_str = " ".join(
                [
                    '{key}="{value}"'.format(key=key, value=value)
                    for key, value in attrs.items()
                ]
            )

        return '<script {attrs_str} src="{src}"></script>'.format(
            attrs_str=attrs_str,
            src=src,
        )

    def generate_stylesheet_tag(self, href: str) -> str:
        """
        Generates and HTML <link> stylesheet tag for CSS.

        Arguments:
            href {str} -- CSS file URL.

        Returns:
            str -- CSS link tag.
        """
        return '<link rel="stylesheet" href="{href}" />'.format(href=href)

    def generate_vite_ws_client(self) -> str:
        """
        Generates the script tag for the Vite WS client for HMR.

        Only used in development, in production this method returns
        an empty string.

        Returns:
            str -- The script tag or an empty string.
        """
        if not settings.VITE_SERVE_MODE:
            return ""

        return self.generate_script_tag(
            self.generate_vite_server_url(settings.VITE_WS_CLIENT),
            {"type": "module"},
        )

    def generate_vite_react_hmr(cls) -> str:
        """
        Generates the script tag for the Vite WS client for HMR.

        Only used in development, in production this method returns
        an empty string.

        Returns:
            str -- The script tag or an empty string.
        """
        if not settings.VITE_SERVE_MODE:
            return ""
        if settings.VITE_REACTJS_HMR:
            return f"""
                <script type="module">
                import RefreshRuntime from '{cls.generate_vite_server_url()}@react-refresh'
                RefreshRuntime.injectIntoGlobalHook(window)
                window.$RefreshReg$ = () => {{}}
                window.$RefreshSig$ = () => (type) => type
                window.__vite_plugin_react_preamble_installed__=true
                </script>
                """
        else:
            return ""

    def generate_vite_asset(
        self, path: str, scripts_attrs: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Generates all assets include tags for the file in argument.

        Returns:
            str -- All tags to import this asset in yout HTML page.
        """
        if settings.VITE_SERVE_MODE:
            return self.generate_script_tag(
                self.generate_vite_server_url(path),
                {"type": "module", "async": "", "defer": ""},
            )

        if path not in self._manifest:
            raise RuntimeError(
                "Cannot find {path} in Vite manifest at {manifest}".format(
                    path=path, manifest=settings.VITE_MANIFEST_PATH
                )
            )

        tags = []
        manifest_entry: dict = self._manifest[path]
        if not scripts_attrs:
            scripts_attrs = {"type": "module", "async": "", "defer": ""}

        # Add dependent CSS
        if "css" in manifest_entry:
            for css_path in manifest_entry.get("css"):
                tags.append(
                    self.generate_stylesheet_tag(urljoin(settings.STATIC_URL, css_path))
                )

        # Add dependent "vendor"
        if "imports" in manifest_entry:
            for vendor_path in manifest_entry.get("imports"):
                tags.append(
                    self.generate_vite_asset(vendor_path, scripts_attrs=scripts_attrs)
                )

        # Add the script by itself
        tags.append(
            self.generate_script_tag(
                urljoin(settings.STATIC_URL, manifest_entry["file"]),
                attrs=scripts_attrs,
            )
        )

        return "\n".join(tags)


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
    tags.append(ViteLoader().generate_vite_react_hmr())
    tags.append(ViteLoader().generate_vite_ws_client())
    return Markup("\n".join(tags))


def vite_asset(
    path: str, scripts_attrs: Optional[Dict[str, str]] = None
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
        ViteLoader().generate_vite_asset(
            path, scripts_attrs=scripts_attrs
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

    return ViteLoader().generate_vite_asset_url(path)
