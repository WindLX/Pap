from typing import Optional

from model.config import BasicConfigModel, PathConfigModel
from service.logger import logger
from service.config import system_config, basic_config, path_config, dev_config

from uvicorn import run
from fastapi import FastAPI, HTTPException, status
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


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    """index route, main page

    Returns:
        FileResponse: HTML of main page
    """
    logger.debug("load index page")
    return FileResponse("dist/index.html")


@app.get("/api/get_config/{section}", response_model=BasicConfigModel | PathConfigModel)
async def get_config(section: str):
    """get all available config to frontend

    Returns:
        BasicConfigModel | PathConfigModel: config or error

    Raises:
        HTTPException: error response 404
    """
    logger.info(f"GET /api/get_config/{section}")
    data: Optional[BasicConfigModel | PathConfigModel] = None
    match section:
        case "basic":
            data = basic_config.model
        case "path":
            data = path_config.model
    if data is None:
        logger.warning(f"{section} not found")
        raise HTTPException(status_code=404, detail=f"{section} not found")
    else:

        return data


@app.put("/api/set_config/{section}", status_code=status.HTTP_202_ACCEPTED)
async def set_config(section: str, value: BasicConfigModel | PathConfigModel):
    """set all available config

    Args:
        section (str): section name
        value (BasicConfigModel | PathConfigModel): new config value

    Raises:
        HTTPException: error response 404
    """
    logger.info(f"PUT /api/set_config/{section}")
    match section:
        case "basic":
            if basic_config.model is not None and type(value) == BasicConfigModel:
                basic_config.model = value
            else:
                logger.warning(f"{section} not found")
                raise HTTPException(
                    status_code=404, detail=f"{section} not found")
        case "path":
            if path_config.model is not None and type(value) == PathConfigModel:
                path_config.model = value
                path_config.check_path()
            else:
                logger.warning(f"{section} not found")
                raise HTTPException(
                    status_code=404, detail=f"{section} not found")


def start_backend(is_dev: bool):
    """Start backend service
    """
    logger.info("start backend")
    run(app='backend:app', host=host, port=port, reload=is_dev)
