from flask_restx import Api, Namespace


class ApiBase:
    NAMESPACE: str = ''
    DESCRIPTION: str = ''

    @classmethod
    def init(cls, api: Api, parentPath: str):
        ns = api.namespace(cls.NAMESPACE, cls.DESCRIPTION, path=f'{parentPath}/{cls.NAMESPACE}')
        cls._init_endpoints(ns)

    @classmethod
    def _init_endpoints(cls, ns: Namespace):
        raise NotImplementedError()
