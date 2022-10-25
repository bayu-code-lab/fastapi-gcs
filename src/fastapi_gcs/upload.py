import base64
from fastapi import UploadFile
from .upload_validation import UploadValidation
from .generate import Generate
from google.cloud import storage

class FailedValidation(Exception):
    def __init__(self, reason: str, message: str, file_name: str) -> None:
        self.reason = reason
        self.message = message
        self.file_name = file_name
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message} on {self.file_name}: {self.reason}'

class Upload:
    @classmethod
    async def encrypted_file(cls, project_id: str, bucket_name: str,  file: UploadFile, path: str, maximum_size: int, allowed_extension: list):
        try:
            storage_client = storage.Client(project_id)
            bucket = storage_client.bucket(bucket_name)
            file_size = len(await file.read())
            if await UploadValidation.extensions_validation(file, allowed_extension):
                if await UploadValidation.size_validation(file_size, maximum_size):
                    blob_path = f'{path}/{file.filename}'
                    key = await Generate.encryption_key()
                    b64_decode_key = base64.b64decode(key)
                    blob = bucket.blob(blob_path, encryption_key=b64_decode_key)
                    file.file.seek(0)
                    blob.upload_from_file(file_obj=file.file, content_type=file.content_type)
                    return {
                                'name': file.filename, 
                                'file_url': blob_path, 
                                'file_size': await UploadValidation.convert_size(file_size), 
                                'content_type': file.content_type,
                                'encryption_key': key
                            }
                else:
                    raise FailedValidation(reason='attachment size exceeds the maximum size', message='validation failed', file_name=file.filename)
            else:
                raise FailedValidation(reason='unsupported extension', message='validation failed', file_name=file.filename)
        except Exception as e:
            raise e
