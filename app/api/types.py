from flask_restx import Api, fields, Model


class ImagePathField(fields.Raw):
    def format(self, value):
        return f'images/{value}'


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
            file=fields.String(readOnly=True, description='Path to the image'),
            labels=fields.List(fields.Nested(cls.label), readOnly=True),
            path=ImagePathField(readOnly=True, attribute='file'),
        ))
