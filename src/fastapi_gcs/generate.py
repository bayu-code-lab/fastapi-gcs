import os
import hashlib
import base64

class Generate:
    @classmethod
    async def __b64_encode_aes_key(cls):
        try:
            aes_key = os.urandom(32)
            b64_encoded_aes_key = base64.b64encode(aes_key)
            return b64_encoded_aes_key.decode('utf-8')
        except Exception as e:
            raise e

    @classmethod
    async def __b64_encode_sha256_key(cls, b64_encoded_aes_key: str):
        try:
            encoded_aes_key = b64_encoded_aes_key.encode('utf-8')
            b64_encoded_sha256_key = base64.b64encode(hashlib.sha256(encoded_aes_key).digest())
            return b64_encoded_sha256_key.decode('utf-8')
        except Exception as e:
            raise e

    @classmethod
    async def encryption_key(cls, include_sha256_key: bool = False):
        try:
            b64_encoded_aes_key = cls.__b64_encode_aes_key()
            if include_sha256_key:
                b64_encoded_sha256_key = cls.__b64_encode_sha256_key(b64_encoded_aes_key)
                return b64_encoded_aes_key, b64_encoded_sha256_key
            return b64_encoded_aes_key
        except Exception as e:
            raise e



print(GenerateKey.get_encryption_key(True))