from os import path, mkdir
from typing import Optional, Any

from schemas.config import BasicConfigSchema, PathConfigSchema

from toml import load as toml_load
from toml import dump as toml_dump


class ConfigManager:
    def __init__(self, config_file: str) -> None:
        self.__config_file = config_file
        self.__config = self.load_config()

    def load_config(self) -> dict:
        """load config file

        Returns:
            dict: config
        """
        try:
            with open(self.__config_file, 'r') as file:
                config = toml_load(file)
            return config
        except FileNotFoundError:
            print(
                f"Config file '{self.__config_file}' not found. Creating a new one.")
            return {}

    def save_config(self) -> None:
        """save config
        """
        with open(self.__config_file, 'w') as file:
            toml_dump(self.__config, file)

    def get_section(self, section: str) -> Optional[dict]:
        """get section by section name

        Args:
            section (str): section name

        Returns:
            Optional(dict): section
        """
        return self.__config.get(section, None)

    def get_value(self, section: str, key: str) -> Any:
        """get value by key of selected section

        Args:
            section (str): section name
            key (str): key name

        Returns:
            Any: value
        """
        return self.__config.get(section, {}).get(key, None)

    def set_section(self, section: str, value: dict) -> None:
        """set section data by section name

        Args:
            section (str): section name
            value (dict): section value
        """
        if section not in self.__config:
            self.__config[section] = {}
        self.__config[section] = value
        self.save_config()

    def set_value(self, section: str, key: str, value: str) -> None:
        """set new value by key of selected section

        Args:
            section (str): section name
            key (str): key name
            value (str): new value
        """
        if section not in self.__config:
            self.__config[section] = {}
        self.__config[section][key] = value
        self.save_config()


class BaseConfig:
    """设置的基础类
    """

    def __init__(self, config_manager: ConfigManager, section_name: str) -> None:
        self.config_manager = config_manager
        self.section_name = section_name

    def get_property(self, key: str) -> Any:
        """获取配置属性值

        Args:
            key (str): 键名

        Returns:
            Any: 键值
        """
        return self.config_manager.get_value(self.section_name, key)

    def set_property(self, key: str, value: Any):
        """设置配置属性值

        Args:
            key (str): 键名
            value (str): 新键值
        """
        self.config_manager.set_value(self.section_name, key, value)


class SystemConfig(BaseConfig):
    """系统设置
    """

    def __init__(self, config_manager: ConfigManager) -> None:
        super().__init__(config_manager, "system")

    @property
    def host(self) -> str:
        """webview 监听的 host 地址

        Returns:
            str: 主机地址
        """
        return self.get_property("host")

    @host.setter
    def host(self, value: str) -> None:
        self.set_property("host", value)

    @property
    def port(self) -> int:
        """webview 监听的 port 端口

        Returns:
            int: 端口
        """
        return self.get_property("port")

    @port.setter
    def port(self, value: int) -> None:
        self.set_property("port", value)


class BasicConfig(BaseConfig):
    """基础设置
    """

    def __init__(self, config_manager: ConfigManager) -> None:
        super().__init__(config_manager, "basic")

    @property
    def title(self) -> str:
        """窗口标题

        Returns:
            str: 窗口标题
        """
        return self.get_property("title")

    @title.setter
    def title(self, value: str) -> None:
        self.set_property("title", value)

    @property
    def log_level(self) -> str:
        """日志等级

        Returns:
            str: 日志等级
        """
        return self.get_property("log_level")

    @log_level.setter
    def log_level(self, value: str) -> None:
        self.set_property("log_level", value)

    @property
    def model(self) -> Optional[BasicConfigSchema]:
        if (data_dict := self.config_manager.get_section(self.section_name)) is not None:
            return BasicConfigSchema(**data_dict)
        else:
            return None

    @model.setter
    def model(self, value: BasicConfigSchema) -> None:
        new_data = value.model_dump()
        return self.config_manager.set_section(self.section_name, new_data)


class PathConfig(BaseConfig):
    """路径配置
    """

    def __init__(self, config_manager: ConfigManager) -> None:
        super().__init__(config_manager, "path")

    @property
    def resource_dir(self) -> str:
        """资源存储目录

        Returns:
            str: 资源存储目录
        """
        return self.get_property("resource_dir")

    @resource_dir.setter
    def resource_dir(self, value: str) -> None:
        self.set_property("resource_dir", value)

    @property
    def content_dir(self) -> str:
        """内容存储目录

        Returns:
            str: 内容存储目录
        """
        return self.get_property("content_dir")

    @content_dir.setter
    def content_dir(self, value: str) -> None:
        self.set_property("content_dir", value)

    @property
    def log_path(self) -> str:
        """日志文件路径

        Returns:
            str: 日志文件路径
        """
        return self.get_property("log_path")

    @log_path.setter
    def log_path(self, value: str) -> None:
        self.set_property("log_path", value)

    @property
    def tag_path(self) -> str:
        """标签文件路径

        Returns:
            str: 标签文件路径
        """
        return self.get_property("tag_path")

    @tag_path.setter
    def tag_path(self, value: str) -> None:
        self.set_property("tag_path", value)

    def check_path(self) -> None:
        dirs = [self.resource_dir, self.content_dir]
        files = [self.log_path, self.tag_path]

        def check_single_dir(_path: str):
            if not path.exists(_path):
                mkdir(_path)
                print(f'create folder {_path}')

        def check_single_file(_path: str):
            if not path.exists(_path):
                with open(_path, 'w'):
                    print(f'create file {_path}')

        for p in dirs:
            check_single_dir(p)

        for p in files:
            check_single_file(p)

    @property
    def model(self) -> Optional[PathConfigSchema]:
        if (data_dict := self.config_manager.get_section(self.section_name)) is not None:
            return PathConfigSchema(**data_dict)
        else:
            return None

    @model.setter
    def model(self, value: PathConfigSchema) -> None:
        new_data = value.model_dump()
        self.config_manager.set_section(self.section_name, new_data)


class DevConfig(BaseConfig):
    """开发配置
    """

    def __init__(self, config_manager: ConfigManager) -> None:
        super().__init__(config_manager, "dev")

    @property
    def debug(self) -> bool:
        """调试模式开关

        Returns:
            bool: 是否为调试模式
        """
        return self.get_property("debug")

    @property
    def dev_host(self) -> str:
        """开发时 Vite 的主机地址

        Returns:
            str: 主机地址
        """
        return self.get_property("dev_host")

    @property
    def dev_port(self) -> int:
        """开发时 Vite 的端口号

        Returns:
            int: 端口号
        """
        return self.get_property("dev_port")


config_manager = ConfigManager("./data/config.toml")
system_config = SystemConfig(config_manager=config_manager)
basic_config = BasicConfig(config_manager=config_manager)
path_config = PathConfig(config_manager=config_manager)
dev_config = DevConfig(config_manager=config_manager)
path_config.check_path()