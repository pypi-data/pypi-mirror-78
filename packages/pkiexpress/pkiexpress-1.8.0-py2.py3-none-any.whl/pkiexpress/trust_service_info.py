class TrustServiceInfo():

    def __init__(self, model):
        self.__provider = model.get('provider', None)
        self.__badge_url = model.get('badgeUrl', None)

        self.__service = None
        service = model.get('service', None)
        if service is not None:
            self.__service = TrustServiceName(service)

    def get_service(self):
        return self.__service

    def set_service(self, service):
        self.__service = service

    def get_provider(self):
        return self.__provider

    def set_provider(self, provider):
        self.__provider = provider

    def get_badge_url(self):
        return self.__badge_url

    def set_badge_url(self, badge_url):
        self.__badge_url = badge_url

    service = property(get_service, set_service)
    provider = property(get_provider, set_provider)
    badge_url = property(get_badge_url, set_badge_url)


class TrustServiceName():

    def __init__(self, model):
        self.__name = model.get('name', None)

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    name = property(get_name, set_name)

__all__ = [
    'TrustServiceInfo',
    'TrustServiceName'
]