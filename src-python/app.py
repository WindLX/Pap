import asyncio
from multiprocessing import Process

from frontend import start_frontend
from backend import start_backend


async def main():
    frontend_process = Process(target=start_frontend)
    frontend_process.start()

    server_task = asyncio.create_task(await start_backend())

    frontend_process.join()

    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    asyncio.run(main())
