from google.cloud import storage
from .fgcs_generate import FGCSGenerate
import base64

class FGCSDelete:
    @classmethod
    async def encryption_file(cls, project_id: str, bucket_name: str, path: str, encryption_key: str):
        try:
            storage_client = storage.Client(project_id)
            bucket = storage_client.bucket(bucket_name)
            b64_decode_key = base64.b64decode(encryption_key)
            blob = bucket.blob(path, encryption_key=b64_decode_key)
            blob.delete()
        except Exception as e:
            raise e

    @classmethod
    async def file(cls, project_id: str, bucket_name: str, path: str):
        try:
            storage_client = storage.Client(project_id)
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(path)
            blob.delete()
        except Exception as e:
            raise e

    @classmethod
    async def multiple_file(cls, project_id: str, bucket_name: str, path: list):
        try:
            storage_client = storage.Client(project_id)
            bucket = storage_client.bucket(bucket_name)
            for i in path:
                blob = bucket.blob(i)
                blob.delete()
        except Exception as e:
            raise e