
from fastutils import jsonutils
from fastutils import strutils
from fastutils import cipherutils
from fastutils import rsautils
from django_middleware_global_request.middleware import get_request


class AbstractResultPacker(object):
    
    def pack_result(self, result):
        raise NotImplementedError()

    def pack_error(self, error):
        raise NotImplementedError()


class SimpleJsonResultPacker(AbstractResultPacker):

    def pack_result(self, result):
        return {
            "success": True,
            "result": result,
        }

    def pack_error(self, error):
        return {
            "success": False,
            "error": error,
        }


class SafeJsonResultPacker(SimpleJsonResultPacker):
    
    def __init__(self, result_encoder=cipherutils.SafeBase64Encoder(), password_length=32, encrypted_password_fieldname="encryptedPassword", encrypted_data_fieldname="encryptedData", client_rsa_publickey_fieldname="CLIENT_RSA_PUBLICKEY"):
        self.password_length = password_length
        self.encrypted_password_fieldname = encrypted_password_fieldname
        self.encrypted_data_fieldname = encrypted_data_fieldname
        self.client_rsa_publickey_fieldname = client_rsa_publickey_fieldname
        self.result_encoder = result_encoder

    def pack_result(self, result):
        result = super().pack_result(result)
        return self.encrypt_data(result)

    def pack_error(self, error):
        error =  super().pack_error(error)
        return self.encrypt_data(error)

    def encrypt_data(self, data):
        request = get_request()
        result_text = jsonutils.simple_json_dumps(data)
        password = strutils.random_string(self.password_length)
        result_cipher = cipherutils.AesCipher(password=password, result_encoder=self.result_encoder)
        result_data = result_cipher.encrypt(result_text.encode("utf-8"))
        encrypted_password = rsautils.encrypt(password.encode(), getattr(request, self.client_rsa_publickey_fieldname))
        return {
            self.encrypted_password_fieldname: encrypted_password,
            self.encrypted_data_fieldname: result_data,
        }
 