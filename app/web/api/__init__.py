from flask import Flask
from flask_restx import Api

from app.web.api.types import Types
from app.web import EndpointBase


class RestApi(EndpointBase):
    """ Entry point for REST API definitions
    """
    API = None

    @classmethod
    def init(cls, app: Flask):
        cls.API = Api(app, version='1.0', title='FlaskImageGallery API',
                      description='RESTful API for the Image Gallery',
                      endpoint='/api',  # BUG: this parameter is not considered:
                                        # https://github.com/python-restx/flask-restx/issues/249
                      doc='/api/doc')

        Types.init_models(cls.API)

        from app.web.api.images import ImagesApi
        from app.web.api.labels import LabelsApi
        ImagesApi.init(cls.API, '/api')
        LabelsApi.init(cls.API, '/api')
