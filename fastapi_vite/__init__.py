from .config import pkg_meta
from .loader import vite_asset, vite_asset_url, vite_hmr_client

__version__ = str(pkg_meta["version"])
__all__ = [vite_asset_url, vite_hmr_client, vite_asset]
