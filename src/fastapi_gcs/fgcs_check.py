from google.cloud import storage
import base64

class FGCSCheck:
    @classmethod
    async def file(cls, project_id: str, bucket_name: str, path: str):
        try:
            storage_client = storage.Client(project_id)
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(path)
            return blob.exists()
        except Exception as e:
            raise e

    @classmethod
    async def encrypted_file(cls, project_id: str, bucket_name: str, path: str, encryption_key: str):
        try:
            storage_client = storage.Client(project_id)
            bucket = storage_client.bucket(bucket_name)
            b64_decode_key = base64.b64decode(encryption_key)
            blob = bucket.blob(path, encryption_key=b64_decode_key)
            return blob.exists()
        except Exception as e:
            raise e