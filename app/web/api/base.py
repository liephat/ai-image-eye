from flask_restx import Api, Namespace


class ApiBase:
    """ Base class for sub-APIs
    """
    NAMESPACE: str = ''
    DESCRIPTION: str = ''

    @classmethod
    def init(cls, api: Api, parent_path: str):
        ns = api.namespace(cls.NAMESPACE, cls.DESCRIPTION, path=f'{parent_path}/{cls.NAMESPACE}')
        cls._init_endpoints(ns)

    @classmethod
    def _init_endpoints(cls, ns: Namespace):
        """ Initialization of endpoints in the current sub API

        Must be overridden in concrete class
        """
        raise NotImplementedError()
