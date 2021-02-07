from flask_restx import Namespace, Resource

from app.web.api.types import Types
from app.web.api.base import ApiBase
from app.data.ops import ImageDataHandler


class QueryApi(ApiBase):
    NAMESPACE = 'query'
    DESCRIPTION = 'Query stuff'

    @classmethod
    def _init_endpoints(cls, ns: Namespace):
        # pylint: disable=unused-variable
        @ns.route('/images/<string:q>')
        class Images(Resource):
            @ns.marshal_list_with(Types.image)
            def get(self, q):
                images = ImageDataHandler.filtered_images(q)
                return images
