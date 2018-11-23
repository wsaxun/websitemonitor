import os
import yaml

from monitor.utils.env import get_env, get_root
from monitor.utils.exception import ConfigError


class _LazyProperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if not instance:
            return self
        else:
            value = self.func(instance)   # self.func 为Config实例方法， instance 为Config的self对象
            setattr(instance, self.func.__name__, value)
            return value


class Config:
    @staticmethod
    def _get_config(filename):
        yml = os.path.join(get_root(), filename)
        try:
            with open(yml, 'r') as f:
                all_config = yaml.load(f)
        except FileNotFoundError:
            raise ConfigError('FileNotFoundError')
        env = get_env()
        all_config = all_config.get(env)
        return all_config

    # @property
    @_LazyProperty
    def log_config(self):
        log_config = self._get_config('etc/monitor.yaml')
        log_config = log_config.get('log')
        return log_config

    # @property
    @_LazyProperty
    def credits_config(self):
        credits_config = self._get_config('etc/monitor.yaml')
        credits_config = credits_config.get('asm').get('credits')
        return credits_config

    # @property
    @_LazyProperty
    def city_config(self):
        city_config = self._get_config('etc/monitor.yaml')
        city_config = city_config.get('asm').get('city')
        return city_config

    # @property
    @_LazyProperty
    def cp_config(self):
        cp_config = self._get_config('etc/monitor.yaml')
        cp_config = cp_config.get('asm').get('cp')
        return cp_config

    # @property
    @_LazyProperty
    def codes_config(self):
        codes_config = self._get_config('etc/monitor.yaml')
        codes_config = codes_config.get('asm').get('codes')
        return codes_config

    # @property
    @_LazyProperty
    def sites_config(self):
        sites_config = self._get_config('etc/monitor.yaml')
        sites_config = sites_config.get('asm').get('sites')
        return sites_config

    # @property
    @_LazyProperty
    def country_code_config(self):
        country_code_config = self._get_config('etc/monitor.yaml')
        country_code_config = country_code_config.get('asm').get(
            'country_code_config')
        return country_code_config

    # @property
    @_LazyProperty
    def city_code_config(self):
        city_code_config = self._get_config('etc/monitor.yaml')
        city_code_config = city_code_config.get('asm').get('city_code_config')
        return city_code_config

    def __getattr__(self, item):
        raise ConfigError('ConfigNotFoundError')


CONFIG = Config()
