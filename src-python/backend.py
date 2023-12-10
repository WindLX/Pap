from router import login, config, note, tag, emoji, net, resource
from model.note_group import Base
from service.logger import logger
from service.config import system_config, dev_config
from service.database import engine
from service.security import authentication_manager

from uvicorn import run
from fastapi import FastAPI, Response, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

# system init
host = system_config.host
port = system_config.port
backend_host = system_config.backend_host
backend_port = system_config.backend_port

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
    'http://127.0.0.1:13956'
    "http://localhost:6174",
]

# middleware
if not dev_config.debug:
    @app.middleware("http")
    async def auth_middleware(request: Request, call_next):
        if request.url.path in ["/", "/login/", "/login"] or request.url.path.startswith("/assets/"):
            response = await call_next(request)
            return response
        if token := request.headers.get("Authorization"):
            exception = authentication_manager.check_jwt_token(token)
            if exception:
                return exception
            else:
                response = await call_next(request)
                return response
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
else:
    @app.middleware("http")
    async def dummy_middleware(request: Request, call_next):
        response = await call_next(request)
        return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# static files
app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")
app.mount("/data/note", StaticFiles(directory="data/note"), name="note")
app.mount("/data/res", StaticFiles(directory="data/res"), name="res")

# router
app.include_router(login.router)
app.include_router(config.router)
app.include_router(note.router)
app.include_router(tag.router)
app.include_router(emoji.router)
app.include_router(net.router)
app.include_router(resource.router)


@app.get("/", include_in_schema=False)
async def index(request: Request):
    """index route, main page

    Returns:
        _TemplateResponse : HTML of main page
    """
    logger.debug("GET / load index page")
    return templates.TemplateResponse("index.html", {"request": request, "host": host, "port": port})


def start_backend(is_dev: bool):
    """Start backend service
    """
    logger.info("start backend")
    run(app='backend:app', host=backend_host, port=backend_port, reload=is_dev)
