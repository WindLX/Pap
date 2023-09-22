from config import debug, host, port

from uvicorn import run
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# FastAPI app
app = FastAPI(debug=debug)
# static files
app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")


@app.get("/", include_in_schema=False)
async def index() -> FileResponse:
    """index route, main page

    Returns:
        FileResponse: HTML of main page
    """
    return FileResponse("dist/index.html")


def start_backend():
    """Start backend service
    """
    run(app=app, host=host, port=port)
