import os


def get_env():
    env = os.environ.get('MONITOR', 'DEV')
    return env


def get_root():
    project_path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return project_path
