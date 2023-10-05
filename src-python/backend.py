from router import config

from service.logger import logger
from service.config import system_config, dev_config

from uvicorn import run
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

host = system_config.host
port = system_config.port

# FastAPI app
app = FastAPI(debug=dev_config.debug)
# static files
app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")

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

app.include_router(config.router)


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    """index route, main page

    Returns:
        FileResponse: HTML of main page
    """
    logger.debug("load index page")
    return FileResponse("dist/index.html")


def start_backend(is_dev: bool):
    """Start backend service
    """
    logger.info("start backend")
    run(app='backend:app', host=host, port=port, reload=is_dev)
