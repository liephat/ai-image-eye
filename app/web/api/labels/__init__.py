from flask_restx import Namespace, Resource, abort

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
                return ImageDataHandler.get_label_by_id(label_id) or abort(404)

        @ns.route('/assignment/<string:label_assignment_id>')
        class Assignment(Resource):
            @ns.marshal_with(Types.label_assignment)
            def get(self, label_assignment_id):
                return ImageDataHandler.get_label_assignment_by_id(label_assignment_id) \
                       or abort(404)

            @ns.marshal_with(Types.label_assignment)
            def put(self, label_assignment_id):
                """ Update an existing label assignment """

                # FIXME: This isn't called from the main thread which may result in SQL Alchemy
                #        session problems.
                #     ... but somehow it also works like this most of the time.

                data = self.api.payload or {}
                label_data = data.get('label')
                if label_data and label_data.get('name'):
                    assignment = ImageDataHandler.update_label_assignment_label_name(label_assignment_id,
                                                                                     label_data['name']) or abort(404)
                else:
                    assignment = ImageDataHandler.get_label_assignment_by_id(label_assignment_id) or abort(404)
                return assignment
