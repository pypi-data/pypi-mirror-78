import base64
import binascii
import os

from .cades_signature import CadesSignature
from .pki_express_config import PkiExpressConfig
from .signature_explorer import SignatureExplorer


class CadesSignatureExplorer(SignatureExplorer):

    def __init__(self, config=None):
        if not config:
            config = PkiExpressConfig()
        super(CadesSignatureExplorer, self).__init__(config)

        self._data_file_path = None
        self._extract_content_path = None

    @property
    def data_file_path(self):
        return self._data_file_path

    # region set_data_file

    def set_data_file_from_path(self, path):
        """

        Sets the path of the data file, which is necessary when is opening and
        validating a detached signature.
        :param path: The path of data file to be used in the validation.

        """
        if not os.path.exists(path):
            raise Exception('The provided data file to opened was not found')
        self._data_file_path = path

    def set_data_file_from_raw(self, content_raw):
        """

        Sets the content of the data file, which is necessary when is opening
        and validating a detached signature.
        :param content_raw: The content of the data file to be used in the
        validation.

        """
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self._data_file_path = temp_file_path

    def set_data_file_from_base64(self, content_base64):
        """

        Sets the base64-encoded content of the data file, which is necessary
        when is opening and validating a detached signature.
        :param content_base64: The base64-encoded content of the data file to be
        used in the validation.

        """
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided file to be signed is not '
                            'base64-encoded')
        self.set_signature_file_from_raw(raw)

    # endregion

    @property
    def extract_content_path(self):
        return self._extract_content_path

    @extract_content_path.setter
    def extract_content_path(self, value):
        self._extract_content_path = value

    def open(self):
        if not self._signature_file_path:
            raise Exception('The provided signature file was not set')

        args = [self._signature_file_path]

        # Verify and add common options
        self._verify_and_add_common_options(args)

        if self._data_file_path:
            args.append('--data-file')
            args.append(self._data_file_path)

        if self._extract_content_path:
            args.append('--extract-content')
            args.append(self._extract_content_path)

        # This operation can only be used on versions greater than 1.3 of the
        # PKI Express.
        self._version_manager.require_version('1.3')

        # Invoke command.
        response = self._invoke(self.COMMAND_OPEN_CADES, args)
        output = CadesSignatureExplorer._parse_output(response[0])
        return CadesSignature(output)


__all__ = ['CadesSignatureExplorer']
