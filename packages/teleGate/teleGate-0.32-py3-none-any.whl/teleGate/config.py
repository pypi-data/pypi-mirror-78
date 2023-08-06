SUBSCRIBERS_FILE = 'shared/subscribers.data'

API_HOST = '0.0.0.0'
API_PORT = 35001
API_BACKLOG_SIZE = 10000

TG_NAME = None
TG_API_ID = None
TG_API_HASH = None
TG_PROXY = None
TG_TOKEN = None

SHARED_CONFIG_FILE = 'shared/config.py'

from os.path import isfile, abspath, expanduser

SHARED_CONFIG_FILE = abspath(expanduser(SHARED_CONFIG_FILE))
if isfile(SHARED_CONFIG_FILE):
    import importlib.util

    shared_config_spec = importlib.util.spec_from_file_location('shared_config', SHARED_CONFIG_FILE)
    shared_config_module = importlib.util.module_from_spec(shared_config_spec)
    shared_config_spec.loader.exec_module(shared_config_module)
    for k in dir(shared_config_module):
        if k.startswith('__'): continue
        globals()[k] = getattr(shared_config_module, k)
else:
    print(f'Warning: Shared config not found!')
