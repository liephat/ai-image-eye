from flask_restx import Namespace, Resource

from app.web.api.types import Types
from app.web.api.base import ApiBase
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
                return ImageDataHandler.all_labels()

        @ns.route('/label/<string:label_id>')
        class Label(Resource):
            @ns.marshal_with(Types.label)
            def get(self, label_id):
                return ImageDataHandler.get_label_by_id(label_id)

        @ns.route('/assignment/<string:label_assignment_id>')
        class Assignment(Resource):
            @ns.marshal_with(Types.label_assignment)
            def get(self, label_assignment_id):
                return ImageDataHandler.get_label_assignment_by_id(label_assignment_id)
