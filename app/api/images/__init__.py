
from flask_restx import Api, Resource, Namespace

from app.api.base import ApiBase
from app.api.types import Types
from app.data.ops import ImageDataHandler


class ImagesApi(ApiBase):
    NAMESPACE = 'images'
    DESCRIPTION = 'Image operations'

    @classmethod
    def _init_endpoints(cls, ns: Namespace):
        @ns.route('/all')
        class All(Resource):
            @ns.marshal_list_with(Types.image)
            def get(self):
                handler = ImageDataHandler()
                all_images = handler.all_images()
                return all_images