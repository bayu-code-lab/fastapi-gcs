import os
import hashlib
import base64
from datetime import timedelta
from google.cloud import storage

class FGCSGenerate:
    @classmethod
    async def b64_encode_aes_key(cls):
        try:
            aes_key = os.urandom(32)
            b64_encoded_aes_key = base64.b64encode(aes_key)
            return b64_encoded_aes_key.decode('utf-8')
        except Exception as e:
            raise e

    @classmethod
    async def b64_encode_sha256_key(cls, b64_encoded_aes_key: str):
        try:
            encoded_aes_key = b64_encoded_aes_key.encode('utf-8')
            b64_encoded_sha256_key = base64.b64encode(hashlib.sha256(encoded_aes_key).digest())
            return b64_encoded_sha256_key.decode('utf-8')
        except Exception as e:
            raise e

    @classmethod
    async def encryption_key(cls, include_sha256_key: bool = False):
        try:
            b64_encoded_aes_key = await cls.b64_encode_aes_key()
            if include_sha256_key:
                b64_encoded_sha256_key = await cls.b64_encode_sha256_key(b64_encoded_aes_key)
                return b64_encoded_aes_key, b64_encoded_sha256_key
            return b64_encoded_aes_key
        except Exception as e:
            raise e

    @classmethod
    async def signed_url(self, project_id: str, bucket_name: str, path: str, expiration_hour: int = 24):
        try:
            storage_client = storage.Client(project_id)
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(path) 
            url = blob.generate_signed_url(
                version="v4",
                expiration=timedelta(hours=expiration_hour),
                method="GET"
            )
            return url
        except Exception as e:
            raise e