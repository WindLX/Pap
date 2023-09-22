from config import debug, host, port, title, dev_host, dev_port

from webview import create_window, start


def start_frontend(is_dev: bool):
    url = f"http://{host}:{port}" if not is_dev else f"http://{dev_host}:{dev_port}"
    create_window(title, url=url)
    start(debug=debug)
