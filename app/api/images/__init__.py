from typing import List, Dict

from flask_restx import Api, Resource, Namespace, Model, fields

from app.data.ops import ImageDataHandler


class ImagesApi:
    NAMESPACE = 'images'

    @classmethod
    def init(cls, api: Api, parentPath: str):
        ns = api.namespace(cls.NAMESPACE, 'Image operations', path=f'{parentPath}/{cls.NAMESPACE}')
        models = cls._init_models(api)
        cls._init_endpoints(ns, models)

    @staticmethod
    def _init_models(api: Api) -> Dict[str, Model]:
        label = api.model('Label', dict(
            label_id=fields.String(readOnly=True),
            name=fields.String(readOnly=True),
        ))
        image = api.model('Image', dict(
            image_id=fields.String(readOnly=True, description='Image ID'),
            file=fields.String(readOnly=True, description='Path to the image'),
            labels=fields.List(fields.Nested(label)),
        ))
        models = dict(
            image=image,
            label=label,
        )
        return models

    @staticmethod
    def _init_endpoints(ns: Namespace, models: Dict[str, Model]):
        @ns.route('/all')
        class All(Resource):
            @ns.marshal_list_with(models['image'])
            def get(self):
                handler = ImageDataHandler()
                all_images = handler.all_images()
                return all_images
