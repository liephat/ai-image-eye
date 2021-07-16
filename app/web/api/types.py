from flask_restx import Api, fields, Model


class Types:
    """ Type definitions that are to be reused in API endpoints
    """
    image: Model = None
    label: Model = None
    label_assignment: Model = None
    box: Model = None

    @classmethod
    def init_models(cls, api: Api):
        cls.label = api.model('Label', dict(
            label_id=fields.String(readOnly=True),
            name=fields.String(readOnly=True),
            uri=fields.Url('labels_label'),
        ))

        cls.box = api.model('Box', dict(
            top=fields.Float(), left=fields.Float(), bottom=fields.Float(), right=fields.Float()
        ))

        cls.label_assignment = api.model('LabelAssignment', dict(
            label=fields.Nested(cls.label),
            label_assignment_id=fields.String(readOnly=True),
            box=fields.Nested(cls.box, allow_null=True),
            confidence=fields.Float(),
            origin=fields.String(),
            uri=fields.Url('labels_assignment'),
        ))

        cls.image = api.model('Image', dict(
            image_id=fields.String(readOnly=True, description='Image ID'),
            file=fields.String(readOnly=True, description='Image file name'),
            label_assignments=fields.List(fields.Nested(cls.label_assignment), readOnly=True),
            url=fields.String(readOnly=True, description='Image file url'),
            thumbnail_url=fields.String(readOnly=True, description='Thumbnail file url'),
            uri=fields.Url('images_image'),
        ))
