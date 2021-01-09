from typing import List, Dict

from flask_restx import Api, Resource, Namespace, Model, fields


class ImagesApi:
    NAMESPACE = 'images'

    @classmethod
    def init(cls, api: Api, parentPath: str):
        ns = api.namespace(cls.NAMESPACE, 'Image operations', path=f'{parentPath}/{cls.NAMESPACE}')
        models = cls._init_models(api)
        cls._init_endpoints(ns, models)

    @staticmethod
    def _init_models(api: Api) -> Dict[str, Model]:
        models = dict(
            Image=api.model('Image', dict(
                id=fields.String(readOnly=True, description='Image ID'),
                path=fields.String(readOnly=True, description='Path to the image'),
                thumbnailPath=fields.String(readOnly=True, description='Path to the image thumbnail'),
            ))
        )
        return models

    @staticmethod
    def _init_endpoints(ns: Namespace, models: Dict[str, Model]):
        @ns.route('/all')
        class All(Resource):
            @ns.marshal_list_with(models['Image'])
            def get(self):
                return [
                    {'id': 'the:id', 'path': 'TheFullpath', 'thumbnailPath': 'TheThumbnailPath'},
                    {'id': 'the:id2', 'path': 'TheFullpath2', 'thumbnailPath': 'TheThumbnailPath2'},
                ]
