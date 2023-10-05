import logging

from service.config import basic_config, path_config

logger = logging.getLogger("logger")
logger.setLevel(basic_config.log_level)

# shell output
sh = logging.StreamHandler()
# file output
fh = logging.FileHandler(filename=path_config.log_path, mode='a')

fmt = logging.Formatter(
    fmt="%(levelname)-8s - %(asctime)s - %(filename)-8s : %(lineno)s line - '%(message)s'")

sh.setFormatter(fmt)
fh.setFormatter(fmt)

logger.addHandler(sh)
logger.addHandler(fh)
