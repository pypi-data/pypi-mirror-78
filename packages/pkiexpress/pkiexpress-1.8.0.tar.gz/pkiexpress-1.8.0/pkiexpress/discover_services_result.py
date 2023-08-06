from .trust_service_info import TrustServiceInfo
from .trust_service_auth_parameters import TrustServiceAuthParameters

class DiscoverServicesResult():

    def __init__(self, model):
        self.__services = []
        services = model.get('services', None)
        if services is not None:
            self.__services = [TrustServiceInfo(s) for s in services]
        
        self.__auth_parameters = []
        auth_parameters = model.get('authParameters', None)
        if auth_parameters is not None:
            self.__auth_parameters = [TrustServiceAuthParameters(p) for p in auth_parameters]

    def get_services(self):
        return self.__services

    def set_services(self, services):
        self.__services = services

    def get_auth_parameters(self):
        return self.__auth_parameters

    def set_auth_parameters(self, auth_parameters):
        self.__auth_parameters = auth_parameters

    services = property(get_services, set_services)
    auth_parameters = property(get_auth_parameters, set_auth_parameters)


__all__ = [
    'DiscoverServicesResult'
]