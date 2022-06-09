# Third Party Libraries
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

# Fastapi Vite
from fastapi_vite import runner, settings, vite_asset, vite_hmr_client

templates = Jinja2Templates(directory="assets/templates")
templates.env.globals["vite_hmr_client"] = vite_hmr_client
templates.env.globals["vite_asset"] = vite_asset


async def homepage(request):
    return templates.TemplateResponse("index.html", {"request": request})


async def on_startup():
    await runner.ViteRunner.start()


async def on_shutdown():
    await runner.ViteRunner.stop()


routes = [
    Route("/", endpoint=homepage),
    Mount(
        settings.static_url,
        StaticFiles(directory=settings.static_path),
        name="static",
    ),
]

app = Starlette(
    debug=True,
    routes=routes,
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
)
