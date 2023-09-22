from config import debug, host, port, dev_host, dev_port

from uvicorn import run
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# FastAPI app
app = FastAPI(debug=debug)
# static files
app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")

# CORS config
origins = [
    f"http://{dev_host}:{dev_port}",
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
    return FileResponse("dist/index.html")


@app.get("/hello")
async def hello() -> str:
    """hello route, return `hello` to frontend

    Returns:
        str: `hello`
    """
    return "hello"


def start_backend(is_dev: bool):
    """Start backend service
    """
    run(app='backend:app', host=host, port=port, reload=is_dev)
