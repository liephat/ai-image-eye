from flask_restx import Api, fields, Model


class Types:
    """ Type definitions that are to be reused in API endpoints
    """
    image: Model = None
    label: Model = None

    @classmethod
    def init_models(cls, api: Api):
        cls.label = api.model('Label', dict(
            label_id=fields.String(readOnly=True),
            name=fields.String(readOnly=True),
        ))
        cls.image = api.model('Image', dict(
            image_id=fields.String(readOnly=True, description='Image ID'),
            file=fields.String(readOnly=True, description='Image file name'),
            labels=fields.List(fields.Nested(cls.label), readOnly=True),
            url=fields.String(readOnly=True, description='Image file url'),
            thumbnail_url=fields.String(readOnly=True, description='Thumbnail file url'),
        ))
