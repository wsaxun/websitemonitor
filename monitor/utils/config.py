import os
import yaml

from monitor.utils.env import get_env, get_root


def _get_config(filename):
    yml = os.path.join(get_root(), filename)
    with open(yml, 'r') as f:
        all_config = yaml.load(f)
    return all_config


def get_log_config():
    log_config = _get_config('etc/monitor.yaml')
    env = get_env()
    log_config = log_config.get(env)
    return log_config
