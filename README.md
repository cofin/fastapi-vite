# fastapi-vite

Integration for FastAPI and Vite JS

## what?

This package is designed to make working with javascript assets easier.

fastapi-vite enables the jinja filters required to render asset URLs to jinja templates

## installation

Install using pip

```shell
pip install fastapi-vite
```

## Usage

Configure Jinja templating for FastAPI

```python
templates = Jinja2Templates(directory='templates')
templates.env.globals['render_vite_hmr_client'] = fastapi_vite.render_vite_hmr_client
templates.env.globals['asset_url'] = fastapi_vite.asset_url

```

### Configure Vite

### Configure Static Assets

### Configure Templates

\*render_vite_hmr no-op when in production.

```html
{{ render_vite_hmr_client() }}

<script
  type="text/javascript"
  defer
  src="{{ asset_url('javascript/main.tsx') }}"
></script>
```
