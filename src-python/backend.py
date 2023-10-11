from router import config, resource, content, tag
from model.resource_group import Base
from service.logger import logger
from service.config import system_config, dev_config
from service.database import engine

from uvicorn import run
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

# system init
host = system_config.host
port = system_config.port

# database ORM init
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(debug=dev_config.debug)

# templates
templates = Jinja2Templates(directory="dist")

# CORS config
origins = [
    f"http://{dev_config.dev_host}:{dev_config.dev_port}",
    f"http://{host}:{port}",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# static files
app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")
app.mount("/data", StaticFiles(directory="data"), name="data")

# router
app.include_router(config.router)
app.include_router(resource.router)
app.include_router(content.router)
app.include_router(tag.router)


@app.get("/", include_in_schema=False)
async def index(request: Request):
    """index route, main page

    Returns:
        _TemplateResponse : HTML of main page
    """
    logger.debug("load index page")
    return templates.TemplateResponse("index.html", {"request": request, "host": host, "port": port})


def start_backend(is_dev: bool):
    """Start backend service
    """
    logger.info("start backend")
    run(app='backend:app', host=host, port=port, reload=is_dev)
