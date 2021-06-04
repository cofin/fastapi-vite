import fastapi_vite
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

templates = Jinja2Templates(directory='assets/templates')
templates.env.globals['vite_hmr_client'] = fastapi_vite.vite_hmr_client
templates.env.globals['vite_asset'] = fastapi_vite.vite_asset


async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})

routes = [
    Route('/', endpoint=homepage),
    Mount(fastapi_vite.settings.STATIC_URL, StaticFiles(
        directory=fastapi_vite.settings.STATIC_PATH), name='static')
]

app = Starlette(debug=True, routes=routes)
