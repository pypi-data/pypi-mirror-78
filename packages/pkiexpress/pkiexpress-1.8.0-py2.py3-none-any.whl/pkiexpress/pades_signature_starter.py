"""

Module containing PadesSignatureStarter class.

"""
import base64
import binascii
import json
import os

from .pki_express_config import PkiExpressConfig
from .signature_starter import SignatureStarter


class PadesSignatureStarter(SignatureStarter):
    """

    Class that performs the initialization of a PAdES signature.

    """

    def __init__(self, config=None):
        if not config:
            config = PkiExpressConfig()
        super(PadesSignatureStarter, self).__init__(config)
        self.__pdf_to_sign_path = None
        self.__vr_json_path = None
        self.__suppress_default_visual_representation = False
        self.__custom_signature_field_name = None
        self.__certification_level = None

    # region set_pdf_to_sign

    def set_pdf_to_sign_from_path(self, path):
        """

        Sets the PDF to be signed from its path.
        :param path: The path of the PDF to be signed.

        """
        if not os.path.exists(path):
            raise Exception('The provided PDF to be signed was not found')
        self.__pdf_to_sign_path = path

    def set_pdf_to_sign_from_raw(self, content_raw):
        """

        Sets the PDF to be signed from its content.
        :param content_raw: The content of the PDF to be signed.

        """
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self.__pdf_to_sign_path = temp_file_path

    def set_pdf_to_sign_from_base64(self, content_base64):
        """

        Sets the PDF to be signed from its Base64-encoded content.
        :param content_base64: The Base64-encoded content of the the PDF to be
                               signed.

        """
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided PDF to be signed iw not '
                            'Base64-encoded')
        self.set_pdf_to_sign_from_raw(raw)

    # endregion

    # region set_visual_representation
    def set_suppress_default_visual_representation(self, value):
        """

        Sets whether or not the default visual representation should be 
        suppressed.
        :param value: Boolean of whether the default visual representation 
                      should be suppressed or not

        """
        self.__suppress_default_visual_representation = value

    def set_visual_representation_file(self, path):
        """

        Sets the visual representation for the signature from a JSON file.
        :param path: Path of the JSON file that represents the visual
                     representation.

        """
        if not os.path.exists(path):
            raise Exception('The provided visual representation file was not '
                            'found')
        self.__vr_json_path = path

    def set_visual_representation(self, representation):
        """

        Sets the visual representation for the signature from a model.
        :param representation: The model of the visual representation.

        """
        try:
            json_str = json.dumps(representation)
        except TypeError:
            raise Exception('The provided visual representation, was not valid')
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'w') as file_desc:
            file_desc.write(json_str)
        self.__vr_json_path = temp_file_path

    # endregion

    @property
    def custom_signature_field_name(self):
        return self.__custom_signature_field_name

    @custom_signature_field_name.setter
    def custom_signature_field_name(self, value):
        self.__custom_signature_field_name = value

    @property
    def certification_level(self):
        return self.__certification_level

    @certification_level.setter
    def certification_level(self, value):
        self.__certification_level = value

    def start(self):
        """

        Starts a PAdES signature.
        :return: The result of the signature init. These values are used by
                 SignatureFinisher.

        """
        if not self.__pdf_to_sign_path:
            raise Exception('The PDF to be signed was not set')

        if not self._certificate_path:
            raise Exception('The certificate was not set')

        # Generate transfer file
        transfer_file = self.get_transfer_file_name()

        args = [
            self.__pdf_to_sign_path,
            self._certificate_path,
            os.path.join(self._config.transfer_data_folder, transfer_file)
        ]

        # Verify and add common options between signers
        self._verify_and_add_common_options(args)

        if self.__vr_json_path:
            args.append('--visual-rep')
            args.append(self.__vr_json_path)

        if self.__custom_signature_field_name:
            args.append('--custom-signature-field-name')
            args.append(self.__custom_signature_field_name)

            # This option can only be used on versions greater than 1.15.0 of the PKI Express.
            self._version_manager.require_version('1.15')

        if self.__certification_level:
            args.append('--certification-level')
            args.append(self.__certification_level)

            # This option can only be used on versions greater than 1.16.0 of the PKI Express.
            self._version_manager.require_version('1.16')

        if self.__suppress_default_visual_representation:
            args.append('--suppress-default-visual-rep')
            self._version_manager.require_version('1.13.1')

        # Invoke command with plain text output (to support PKI Express < 1.3)
        response = self._invoke_plain(self.COMMAND_START_PADES, args)
        return self.get_result(response, transfer_file)


__all__ = ['PadesSignatureStarter']
