import fastapi_vite
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

templates = Jinja2Templates(directory='templates')
templates.env.globals['render_vite_hmr_client'] = fastapi_vite.render_vite_hmr_client
templates.env.globals['asset_url'] = fastapi_vite.asset_url


async def homepage(request):
    return templates.TemplateResponse('index.html', {'request': request})

routes = [
    Route('/', endpoint=homepage),
    Mount('/static', StaticFiles(directory='static'), name='static')
]

app = Starlette(debug=True, routes=routes)
