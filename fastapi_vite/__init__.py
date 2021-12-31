from fastapi_vite.config import settings
from fastapi_vite.loader import vite_asset, vite_asset_url, vite_hmr_client

__version__ = "0.3.1"

__all__ = ['vite_asset_url', 'vite_hmr_client', 'vite_asset', 'settings']
