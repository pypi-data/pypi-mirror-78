from .trust_service_info import TrustServiceInfo

class TrustServiceAuthParameters():

    def __init__(self, model):
        self.__auth_url = model.get('authUrl', None)

        self.__service_info = None
        service_info = model.get('serviceInfo', None)
        if service_info is not None:
            self.__service_info = TrustServiceInfo(service_info)

    def get_service_info(self):
        return self.__service_info

    def set_service_info(self, service_info):
        self.__service_info = service_info

    def get_auth_url(self):
        return self.__auth_url

    def set_auth_url(self, auth_url):
        self.__auth_url = auth_url

    service_info = property(get_service_info, set_service_info)
    auth_url = property(get_auth_url, set_auth_url)

__all__ = [
    'TrustServiceAuthParameters'
]