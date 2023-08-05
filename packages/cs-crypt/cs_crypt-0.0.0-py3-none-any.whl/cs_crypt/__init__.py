import base64
import binascii
import os


from cryptography.fernet import Fernet, MultiFernet


KEY_ENV = "CS_CRYPT_KEY"


def _validate_key(key):
    """
    Validate and return a 32B key.

    Key can be generated via:
    - openssl rand -hex 32
    - Fernet.generate_key()
    
    Returns:
    - key (bytes): raw 32B key
    """
    if isinstance(key, str):
        key = key.encode("ascii")

    if len(key) == 44:
        try:
            key = base64.urlsafe_b64decode(key)
        except ValueError:
            pass

    elif len(key) == 64:
        try:
            # 64B could be 32B, hex-encoded
            return binascii.a2b_hex(key)
        except ValueError:
            # not 32B hex
            pass

    if len(key) != 32:
        raise ValueError("Encryption keys must be 32 bytes, hex or base64-encoded.")

    return key


class CryptKeeper:
    def __init__(self):
        self._keys = [
            _validate_key(key) for key in os.environ[KEY_ENV].split(";") if key.strip()
        ]
        self._fernet = MultiFernet(
            [Fernet(base64.urlsafe_b64encode(key)) for key in self._keys]
        )

    def encrypt(self, data):
        return self._fernet.encrypt(data.encode("utf8")).decode("utf-8")

    def decrypt(self, data):
        return self._fernet.decrypt(data.encode("utf-8")).decode("utf-8")

