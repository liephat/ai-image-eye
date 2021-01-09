
from flask_restx import Api, Resource, Namespace

from app.api.types import Types
from app.data.ops import ImageDataHandler


class ImagesApi:
    NAMESPACE = 'images'

    @classmethod
    def init(cls, api: Api, parentPath: str):
        ns = api.namespace(cls.NAMESPACE, 'Image operations', path=f'{parentPath}/{cls.NAMESPACE}')
        cls._init_endpoints(ns)

    @staticmethod
    def _init_endpoints(ns: Namespace):
        @ns.route('/all')
        class All(Resource):
            @ns.marshal_list_with(Types.image)
            def get(self):
                handler = ImageDataHandler()
                all_images = handler.all_images()
                return all_images
