from asyncio import get_event_loop

from config import debug, host, port

from uvicorn import run
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI(debug=debug)
app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")


@app.get("/", include_in_schema=False)
async def redirect_to_index():
    return FileResponse("dist/index.html")


async def start_backend():
    loop = get_event_loop()
    await loop.run_in_executor(None, lambda: run(app=app, host=host, port=port))


if __name__ == "__main__":
    run(app, host=host, port=port)
