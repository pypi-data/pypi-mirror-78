from . import defaults
import os


class CommandLineConfig(object):
    def get_host(self):
        return None


class EnvConfig(object):
    def get_host(self):
        return os.environ.get("ATHENA_HOST", None)


class BaseConfig(object):
    def __init__(self):
        self.command_line = CommandLineConfig()
        self.env = EnvConfig()

    @property
    def host(self):
        return self.command_line.get_host() or self.env.get_host() or defaults.HOST

    @property
    def traces_url(self):
        return defaults.TRACES_URL

    @property
    def metrics_url(self):
        return defaults.METRICS_URL

    @property
    def request_buffer_size(self):
        return defaults.REQUEST_BUFFER_SIZE
