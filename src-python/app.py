from argparse import ArgumentParser

from multiprocessing import Process

from frontend import start_frontend
from backend import start_backend


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--dev", type=bool, default=False)
    args = parser.parse_args()

    frontend_process = Process(target=start_frontend, args=(args.dev,))
    frontend_process.start()

    start_backend()
    frontend_process.terminate()
    frontend_process.join()
