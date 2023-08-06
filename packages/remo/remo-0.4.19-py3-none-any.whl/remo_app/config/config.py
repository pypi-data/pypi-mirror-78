import os
import json
from pathlib import Path

from remo_app.cmd.log import Log
from remo_app.cmd.uuid import get_uuid


REMO_HOME_ENV = 'REMO_HOME'
default_remo_home = str(Path.home().joinpath('.remo'))
default_colab_remo_home = '/gdrive/My Drive/RemoApp'


def is_default_remo_home():
    return get_remo_home() == default_remo_home


def get_remo_home():
    return os.getenv(REMO_HOME_ENV, default_remo_home)


def set_remo_home(path: str, skip_dir_create=False):
    if not skip_dir_create:
        os.makedirs(path, exist_ok=True)
    os.environ[REMO_HOME_ENV] = path

    if path != default_remo_home:
        config = Config(remo_home=path, uuid='undefined')
        config.save(default_remo_home)


class ViewerOptions:
    electron = 'electron'
    browser = 'browser'
    jupyter = 'jupyter'


class CloudPlatformOptions:
    colab = 'colab'
    kaggle = 'kaggle'


class Config:
    name = 'remo.json'
    default_port = '8123'
    local_server = 'http://localhost'
    default_viewer = ViewerOptions.electron
    __slots__ = [
        'db_url',
        'port',
        'server',
        'user_name',
        'user_email',
        'user_password',
        'conda_env',
        'viewer',
        'debug',
        'uuid',
        'public_url',
        'remo_home',
        'cloud_platform'
    ]

    def __init__(self, **kwargs):
        for name in self.__slots__:
            setattr(self, name, kwargs.get(name, ''))
        self.validate()

    def validate(self):
        if not isinstance(self.debug, bool):
            self.debug = False

        if not self.server:
            self.server = self.local_server

        if not self.port:
            self.port = self.default_port

        if not self.viewer:
            self.viewer = self.default_viewer

        if not self.uuid:
            self.uuid = get_uuid()

        self.conda_env = os.getenv('CONDA_PREFIX', '')

    def update(self, **kwargs):
        for name, value in kwargs.items():
            if name in self.__slots__:
                setattr(self, name, value)
        self.validate()

    @staticmethod
    def from_dict(values: dict):
        return Config(**values)

    def is_local_server(self):
        return self.server == self.local_server

    def get_host_address(self):
        skip_port = (self.server.startswith('http://') and self.port == "80") or (
            self.server.startswith('https://') and self.port == "443"
        )
        if skip_port:
            return self.server
        else:
            return '{}:{}'.format(self.server, self.port)

    def parse_db_params(self, url: str = None):
        if not url:
            url = self.db_url
        return parse_db_url(url)

    @staticmethod
    def default_path():
        return Config.path(default_remo_home)

    @staticmethod
    def path(dir_path: str = None):
        if not dir_path:
            dir_path = get_remo_home()
        if not dir_path:
            dir_path = default_remo_home
        return str(os.path.join(dir_path, Config.name))

    @staticmethod
    def is_exists() -> bool:
        return os.path.exists(Config.path())

    @staticmethod
    def load(config_path: str = None):
        if not config_path:
            config_path = Config.path()
        return Config.load_from_path(config_path)

    @staticmethod
    def safe_load(config_path: str = None, exit_on_error: bool = True):
        try:
            return Config.load(config_path)
        except Exception:
            if exit_on_error:
                Log.exit(
                    f'failed to load config from {Config.path()}, please check that file not corrupted or delete config file',
                    report=True,
                )

    @staticmethod
    def load_from_path(config_path: str):
        if not os.path.exists(config_path):
            return None

        with open(config_path) as cfg_file:
            config = json.load(cfg_file)

        return Config.from_dict(config)

    def to_dict(self) -> dict:
        return {name: getattr(self, name) for name in self.__slots__}

    def save(self, dir_path: str = None):
        if not dir_path:
            dir_path = get_remo_home()
        os.makedirs(dir_path, exist_ok=True)

        with open(Config.path(dir_path), 'w') as cfg:
            json.dump(self.to_dict(), cfg, indent=2, sort_keys=True)


def parse_db_url(url: str) -> dict:
    if not url:
        return

    params = {
        'engine': 'postgres',
        'database': '',
        'user': '',
        'password': '',
        'host': 'localhost',
        'port': '5432',
    }

    pos = url.find("://")
    if pos == -1:
        return
    params['engine'] = url[:pos]
    url = url[pos + len('://'):]
    pos = url.rfind('/')
    if pos == -1:
        return

    params['database'] = url[pos + 1:]
    url = url[:pos]
    pos = url.rfind('@')
    if pos != -1:
        user_pass = url[:pos]
        host_port = url[pos + 1:]
        pos = host_port.rfind(':')
        if pos == -1:
            params['host'] = host_port
        else:
            params['host'] = host_port[:pos]
            params['port'] = host_port[pos + 1:]

        pos = user_pass.find(':')
        if pos == -1:
            params['user'] = user_pass
        else:
            params['user'] = user_pass[:pos]
            params['password'] = user_pass[pos + 1:]

    return params
