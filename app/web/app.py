import logging
import os
from typing import Type, List, Optional

from flask import Flask, render_template
from flask_cors import CORS

from app.web.api import RestApi
from app.data.ops import ImageDataHandler
from app.web import EndpointBase
from app.web.routes.images import ImagesEndpoints
from app.web.util.filters import init_filters

logger = logging.getLogger(__name__)


class AppWrapper:
    APP_NAME = 'flask-image-gallery'

    @classmethod
    def get_asset_folder(cls, subfolder):
        return os.path.join(os.path.dirname(__file__), subfolder)

    @classmethod
    def get_endpoint_classes(cls) -> List[Type[EndpointBase]]:
        return [ImagesEndpoints, RestApi]

    def __init__(self, debug=False):
        self.app: Optional[Flask] = None
        self.debug = debug

    def init_flask_app(self):
        assert self.app is None
        self.app = Flask(self.APP_NAME,
                         template_folder=self.get_asset_folder('templates'),
                         static_folder=self.get_asset_folder('static'))
        self.app.config['EXPLAIN_TEMPLATE_LOADING'] = False

        self.__enable_cors()

        init_filters(self.app)
        self._init_endpoints()

        logger.info('Starting up ... welcome to flask-image-gallery')
        logger.debug(f'\n{self.app.url_map}')
        return self.app

    def __enable_cors(self):
        if not self.debug:
            # only enable CORS in a debug environment where the react-app
            # runs from a different host
            return
        CORS(self.app)
        self.app.config['CORS_HEADERS'] = 'Content-Type'

    def _init_endpoints(self):
        @self.app.route('/')
        def index():
            return render_template('index.html', images=ImageDataHandler.all_images())

        for endpoint_class in self.get_endpoint_classes():
            endpoint_class.init(self.app)
