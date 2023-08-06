from pkiexpress.utils import _convert_datetime_from_service

class TrustServiceSessionResult():
    def __init__(self, model):
        self.__session = model.get("session", None)
        self.__custom_state = model.get("customState", None)
        self.__service = model.get("service", None)
        self.__session_type = model.get("type", None)

        self.__expires_on = None
        self.__expires_on_str = model.get("expiresOn", None)
        if(self.__expires_on_str is not None):
            self.__expires_on = _convert_datetime_from_service(self.__expires_on_str)

    def get_session(self):
        return self.__session

    def set_session(self, session):
        self.__session = session

    def get_custom_state(self):
        return self.__custom_state

    def set_custom_state(self, customState):
        self.__custom_state = customState

    def get_service(self):
        return self.__service

    def set_service(self, service):
        self.__service = service

    def get_session_type(self):
        return self.__session_type

    def set_session_type(self, session_type):
        self.__session_type = session_type

    def get_expires_on(self):
        return self.__expires_on

    def set_expires_on(self, expires_on):
        self.__expires_on = expires_on

    def get_expires_on_str(self):
        return self.__expires_on_str

    def set_expires_on_str(self, expires_on_str):
        self.__expires_on_str = expires_on_str

    session = property(get_session, set_session)
    custom_state = property(get_custom_state, set_custom_state)
    service = property(get_service, set_service)
    session_type = property(get_session_type, set_session_type)
    expires_on = property(get_expires_on, set_expires_on)
    expires_on_str = property(get_expires_on_str, set_expires_on_str)

__all__ = [
    'TrustServiceSessionResult'
]