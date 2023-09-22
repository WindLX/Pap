from config import debug, host, port

from uvicorn import run
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI(debug=debug)
app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")


@app.get("/", include_in_schema=False)
async def index():
    return FileResponse("dist/index.html")


def start_backend():
    run(app=app, host=host, port=port)
