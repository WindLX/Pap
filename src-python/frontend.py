import webview
import threading
from config import debug, host, port, title

from webview import create_window, start


def start_frontend() -> None:
    window = create_window(
        title, url=f"http://{host}:{port}")
    start(debug=debug)


if __name__ == "__main__":
    start_frontend()
