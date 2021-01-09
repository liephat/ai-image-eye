from flask import Flask
from flask_restx import Api

from app.api.images import ImagesApi


class RestApi:
    API = None

    @classmethod
    def init(cls, app: Flask):
        cls.API = Api(app, version='1.0', title='FlaskImageGallery API',
                      description='RESTful API for the Image Gallery',
                      endpoint='/api',  # BUG: this parameter is not considered:
                                        # https://github.com/python-restx/flask-restx/issues/249
                      doc='/api/doc')

        ImagesApi.init(cls.API, '/api')
