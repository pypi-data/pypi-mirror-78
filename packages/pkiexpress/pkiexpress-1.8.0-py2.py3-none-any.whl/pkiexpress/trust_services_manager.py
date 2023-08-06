from .pki_express_operator import PkiExpressOperator, PkiExpressConfig
from .check_service_result import CheckServiceResult
from .discover_services_result import DiscoverServicesResult
from .trust_service_session_result import TrustServiceSessionResult
from pkiexpress import trust_service_session_types

class TrustServicesManager(PkiExpressOperator):

    def __init__(self, config=None):
        if not config:
            config = PkiExpressConfig()
        super(TrustServicesManager, self).__init__(config)


    def check_by_cpf(self, service, cpf):
        if not service:
            raise Exception("The provided service is not valid")
        if not cpf:
            raise Exception("The provided CPF is not valid")

        args = []
        args.append(service)
        args.append('--cpf')
        args.append(cpf)

        # This operation can only be used on versions greater than 1.18 of
        # the PKI Express.
        self._version_manager.require_version('1.18')

        # Invoke command.
        response = self._invoke(self.COMMAND_CHECK_SERVICE, args)

        # Parse output and return result.
        model = self._parse_output(response[0])
        return CheckServiceResult(model)


    def check_by_cnpj(self, service, cnpj):
        if not service:
            raise Exception("The provided service is not valid")
        if not cnpj:
            raise Exception("The provided CNPJ is not valid")

        args = []
        args.append(service)
        args.append('--cnpj')
        args.append(cnpj)

        # This operation can only be used on versions greater than 1.18 of
        # the PKI Express.
        self._version_manager.require_version('1.18')

        # Invoke command.
        response = self._invoke(self.COMMAND_CHECK_SERVICE, args)

        # Parse output and return result.
        model = self._parse_output(response[0])
        return CheckServiceResult(model)


    def discover_by_cpf(self, cpf, throw_exceptions=False):
        if not cpf:
            raise Exception("The provided CPF is not valid")

        args = []
        args.append('--cpf')
        args.append(cpf)

        if throw_exceptions:
            args.append('--throw')

        # This operation can only be used on versions greater than 1.18 of
        # the PKI Express.
        self._version_manager.require_version('1.18')

        # Invoke command.
        response = self._invoke(self.COMMAND_DISCOVER_SERVICES, args)

        # Parse output and return result.
        model = self._parse_output(response[0])

        return DiscoverServicesResult(model).services


    def discover_by_cnpj(self, cnpj, throw_exceptions=False):
        if not cnpj:
            raise Exception("The provided CNPJ is not valid")

        args = []
        args.append('--cnpj')
        args.append(cnpj)

        if throw_exceptions:
            args.append('--throw')

        # This operation can only be used on versions greater than 1.18 of
        # the PKI Express.
        self._version_manager.require_version('1.18')

        # Invoke command.
        response = self._invoke(self.COMMAND_DISCOVER_SERVICES, args)

        # Parse output and return result.
        model = self._parse_output(response[0])

        return DiscoverServicesResult(model).services


    def discover_by_cpf_and_start_auth(
        self,
        cpf,
        redirect_url,
        session_type = trust_service_session_types.SIGNATURE_SESSION,
        custom_state = None,
        throw_exceptions = False):

        if not cpf:
            raise Exception("The provided CPF is not valid")
        if not redirect_url:
            raise Exception("The provided redirectUrl is not valid")
        if not session_type:
            raise Exception("No session type was provided")

        args = []

        # Add CPF
        args.append('--cpf')
        args.append(cpf)

        # Add redirect URL
        args.append('--redirect-url')
        args.append(redirect_url)

        # Add session type
        args.append('--session-type')
        args.append(session_type)

        if custom_state is not None:
            args.append('--custom-state')
            args.append(custom_state)

        if throw_exceptions:
            args.append('--throw')

        # This operation can only be used on versions greater than 1.18 of
        # the PKI Express.
        self._version_manager.require_version('1.18')

        # Invoke command.
        response = self._invoke(self.COMMAND_DISCOVER_SERVICES, args)

        # Parse output and return result.
        model = self._parse_output(response[0])

        return DiscoverServicesResult(model).auth_parameters


    def discover_by_cnpj_and_start_auth(
        self,
        cnpj,
        redirect_url,
        session_type = trust_service_session_types.SIGNATURE_SESSION,
        custom_state = None,
        throw_exceptions = False):

        if not cnpj:
            raise Exception("The provided CNPJ is not valid")
        if not redirect_url:
            raise Exception("The provided redirectUrl is not valid")
        if not session_type:
            raise Exception("No session type was provided")

        args = []

        # Add CNPJ
        args.append('--cnpj')
        args.append(cnpj)

        # Add redirect URL
        args.append('--redirect-url')
        args.append(redirect_url)

        # Add session type
        args.append('--session-type')
        args.append(session_type)

        if custom_state is not None:
            args.append('--custom-state')
            args.append(custom_state)

        if throw_exceptions:
            args.append('--throw')

        # This operation can only be used on versions greater than 1.18 of
        # the PKI Express.
        self._version_manager.require_version('1.18')

        # Invoke command.
        response = self._invoke(self.COMMAND_DISCOVER_SERVICES, args)

        # Parse output and return result.
        model = self._parse_output(response[0])

        return DiscoverServicesResult(model).auth_parameters


    def password_authorize(self, service, username, password, session_type=trust_service_session_types.SIGNATURE_SESSION):
        if not service:
            raise Exception("The provided service is not valid")

        if not username:
           raise Exception("The provided username is not valid")

        if not password:
            raise Exception("The provided password is not valid")

        if not session_type:
            raise Exception("No session type was provided")

        args = []

        # Add service.
        args.append(service)

        # Add username.
        args.append(username)

        # Add password.
        args.append(password)

        # Add sessionType.
        args.append(session_type)

        # This operation can only be used on versions greater than 1.18 of
        # the PKI Express.
        self._version_manager.require_version('1.18')

        # Invoke command.
        response = self._invoke(self.COMMAND_PASSWORD_AUTHORIZE, args)

        # Parse output and return result.
        model = self._parse_output(response[0])

        return TrustServiceSessionResult(model)


    def complete_auth(self, code, state):
        if not code:
            raise Exception("The provided code is not valid")
        if not state:
            raise Exception("The provided state is not valid")

        args = []

        # Add code
        args.append(code)
        # Add state
        args.append(state)

        # This operation can only be used on versions greater than 1.18 of
        # the PKI Express.
        self._version_manager.require_version('1.18')

        # Invoke command.
        response = self._invoke(self.COMMAND_COMPLETE_SERVICE_AUTH, args)

        # Parse output and return result.
        model = self._parse_output(response[0])

        return TrustServiceSessionResult(model)

__all__ = [
    'TrustServicesManager'
]