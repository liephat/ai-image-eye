from flask import Flask

from app.config.parser import ConfigParser


class EndpointBase:
    _config = None

    @classmethod
    def get_config(cls):
        if cls._config is None:
            cls._config = ConfigParser()
        return cls._config

    @classmethod
    def init(cls, app: Flask):
        raise NotImplementedError
