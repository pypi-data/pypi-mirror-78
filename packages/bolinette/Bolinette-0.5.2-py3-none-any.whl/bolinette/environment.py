import os
from typing import Dict, Any

import yaml
from bolinette_common import paths


class Settings:
    def __init__(self):
        self._settings: Dict[str, Any] = {}

    def __getitem__(self, key: str):
        return self._settings.get(key.lower(), None)

    def __contains__(self, key: str):
        return key.lower() in self._settings

    def get(self, key: str, default=None):
        item = self[key]
        return item if item is not None else default

    def _reset(self, settings: Dict[str, Any]):
        self._settings = {}
        for key, value in settings.items():
            self._settings[key.lower()] = value


class Environment(Settings):
    def __init__(self):
        super().__init__()
        self.cwd = paths.cwd()
        self.origin = paths.dirname(__file__)
        self.init = Settings()
        self.init._reset(self.load_from_file('init.yaml'))

    def instance_path(self, *path):
        return self.root_path('instance', *path)

    def root_path(self, *path):
        return paths.join(self.cwd, *path)

    def internal_path(self, *path):
        return paths.join(self.origin, *path)

    @property
    def default_env(self):
        return {
            'APP_NAME': 'DEFAULT_NAME',
            'APP_DESC': 'DEFAULT_DESCRIPTION',
            'APP_VERSION': '0.0.1',
            'DBMS': 'SQLITE',
            'DEBUG': True,
            'HOST': '127.0.0.1',
            'PORT': '5000',
            'WEBAPP_FOLDER': self.root_path('webapp', 'dist')
        }

    def read_profile(self):
        try:
            with open(self.instance_path('.profile')) as f:
                for line in f:
                    return line.strip().replace('\n', '')
        except FileNotFoundError:
            return None

    def init_app(self, *, profile=None, overrides=None):
        profile = profile or self.read_profile() or 'development'
        self._reset(self.merge_env_stack([
            self.default_env,
            self.load_from_file(f'env.{profile}.yaml'),
            self.load_from_file(f'env.local.{profile}.yaml'),
            self.load_from_os(),
            overrides or {},
            {'profile': profile}
        ]))

    def load_from_os(self):
        keys = {}
        for key in os.environ:
            if key.startswith('BLNT_'):
                keys[key[5:]] = os.environ[key]
        return keys

    def load_from_file(self, file_name):
        try:
            with open(self.instance_path(file_name), 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {}

    def merge_env_stack(self, stack):
        settings = {}
        for source in stack:
            for key, value in source.items():
                settings[key.lower()] = value
        return settings


env = Environment()
