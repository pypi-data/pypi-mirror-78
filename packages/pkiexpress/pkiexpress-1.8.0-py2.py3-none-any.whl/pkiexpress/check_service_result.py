class CheckServiceResult():
    def __init__(self, model):
        self.__user_has_certificates = model.get("userHasCertificates", None)

    def get_user_has_certificates(self):
        return self.__user_has_certificates

    def set_user_has_certificates(self, user_has_certificates):
        self.__user_has_certificates = user_has_certificates

    user_has_certificates = property(get_user_has_certificates, set_user_has_certificates)


__all__ = [
    'CheckServiceResult'
]