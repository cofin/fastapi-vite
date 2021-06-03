from .config import pkg_meta
import re
from pathlib import Path
from typing import Optional, Union
from .loader import render_vite_hmr_client, asset_url


__version__ = str(pkg_meta['version'])
__all__ = [render_vite_hmr_client, asset_url]
