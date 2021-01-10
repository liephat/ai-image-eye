from flask_restx import Namespace, Resource

from app.api import Types
from app.api.base import ApiBase
from app.data.ops import ImageDataHandler


class LabelsApi(ApiBase):
    NAMESPACE = 'labels'
    DESCRIPTION = 'Label operations'

    @classmethod
    def _init_endpoints(cls, ns: Namespace):
        # pylint: disable=unused-variable
        @ns.route('/all')
        class All(Resource):
            @ns.marshal_list_with(Types.label)
            def get(self):
                handler = ImageDataHandler()
                return handler.all_labels()
