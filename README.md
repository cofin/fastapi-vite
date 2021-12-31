# fastapi-vite

Integration for FastAPI and Vite JS

## what?

This package is designed to make working with javascript assets easier.

fastapi-vite enables the jinja filters required to render asset URLs to jinja templates

Inspired by `django-vite` @ [https://github.com/MrBin99/django-vite]

## installation

Install using pip

```shell
pip install fastapi-vite
```

## Usage

Configure Jinja templating for FastAPI

```python
import fastapi_vite

templates = Jinja2Templates(directory='templates')
templates.env.globals['vite_hmr_client'] = fastapi_vite.vite_hmr_client
templates.env.globals['vite_asset'] = fastapi_vite.vite_asset

```

### Configure Vite

Here is an example used to test this plugin

```javascript
import { defineConfig } from 'vite'
import reactRefresh from '@vitejs/plugin-react-refresh'
const Dotenv = require("dotenv");
import path from "path";
Dotenv.config({ path: path.join(__dirname, ".env") });

const STATIC_URL = process.env.STATIC_URL;
// https://vitejs.dev/config/
export default defineConfig({
  base: `${STATIC_URL}`,
  clearScreen: false,
  plugins: [
    reactRefresh(),

  ],
  build: {
    target: "esnext",
    outDir: "./static/",
    emptyOutDir: true,
    assetsDir: "",
    manifest: true,
    rollupOptions: {
      input:  "./assets/javascript/main.tsx"
    },
  },

  root: ".", // You can change the root path as you wish

})

```

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
