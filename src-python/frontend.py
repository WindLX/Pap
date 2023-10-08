from service.logger import logger
from service.config import dev_config, system_config, basic_config

from webview import create_window, start  # type: ignore


def start_frontend(is_dev: bool):
    """Create a WebView window and run

    Args:
        is_dev (bool): develop mode switch
    """
    url = f"http://{system_config.host}:{system_config.port}" if not is_dev else f"http://{dev_config.dev_host}:{dev_config.dev_port}"
    title = basic_config.title
    logger.info("start frontend")
    create_window(title=title, url=url, maximized=True, min_size=(1080, 800))
    start(debug=dev_config.debug)
