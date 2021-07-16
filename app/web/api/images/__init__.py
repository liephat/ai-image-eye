
from flask_restx import Resource, Namespace

from app.web.api.base import ApiBase
from app.web.api.types import Types
from app.data.ops import ImageDataHandler


class ImagesApi(ApiBase):
    NAMESPACE = 'images'
    DESCRIPTION = 'Image operations'

    @classmethod
    def _init_endpoints(cls, ns: Namespace):
        # pylint: disable=unused-variable
        @ns.route('/all')
        class All(Resource):
            @ns.marshal_list_with(Types.image)
            def get(self):
                all_images = ImageDataHandler.all_images()
                return all_images

        @ns.route('/image/<string:image_id>')
        class Image(Resource):
            @ns.marshal_with(Types.image)
            def get(self, image_id):
                return ImageDataHandler.get_image_by_id(image_id)
