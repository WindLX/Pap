from service.logger import logger
from service.config import dev_config, system_config

from webview import create_window, start


def start_frontend(is_dev: bool):
    """Create a WebView window and run

    Args:
        is_dev (bool): develop mode switch
    """
    url = f"http://{system_config.host}:{system_config.port}" if not is_dev else f"http://{dev_config.dev_host}:{dev_config.dev_port}"
    title = system_config.title
    logger.info("start frontend")
    create_window(title=title, url=url, maximized=True)
    start(debug=dev_config.debug)
