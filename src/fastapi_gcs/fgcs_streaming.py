import io
from google.cloud import storage
import base64

class FGCSStreaming:
    @classmethod
    async def file(cs, project_id: str, bucket_name: str, blob_path:str):
        try:
            storage_client = storage.Client(project_id)
            bucket = storage_client.bucket(bucket_name)
            file_obj = io.BytesIO()
            blob = bucket.blob(blob_path)
            blob.download_to_file(file_obj)
            return file_obj
        except Exception as e:
            raise e
            
    @classmethod
    async def encrypted_file(cs, project_id: str, bucket_name: str, blob_path:str, encryption_key: str):
        try:
            storage_client = storage.Client(project_id)
            bucket = storage_client.bucket(bucket_name)
            file_obj = io.BytesIO()
            key = base64.b64decode(encryption_key)
            blob = bucket.blob(blob_path, encryption_key=key)
            blob.download_to_file(file_obj)
            return file_obj
        except Exception as e:
            raise e