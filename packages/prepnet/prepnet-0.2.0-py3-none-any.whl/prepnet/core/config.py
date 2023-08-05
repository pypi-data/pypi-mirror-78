from contextlib import contextmanager

config = {
    'keep_original': True
}

@contextmanager
def config_context(key, value):
    old = config[key]
    yield
    config[key] = old

@contextmanager
def set_config(key, value):
    config[key] = value

def get_config(key):
    return config[key]
