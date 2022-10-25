import base64
from uuid import uuid4
from fastapi import UploadFile
from .fgcs_upload_validation import FGCSUploadValidation
from .fgcs_generate import FGCSGenerate
from google.cloud import storage

class FailedValidation(Exception):
    def __init__(self, reason: str, message: str, file_name: str) -> None:
        self.reason = reason
        self.message = message
        self.file_name = file_name
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.message} on {self.file_name}: {self.reason}'

class FGCSUpload:
    @classmethod
    async def encrypted_file(cls, project_id: str, bucket_name: str,  file: UploadFile, file_path: str, maximum_size: int, allowed_extension: list, file_name: str = None):
        try:
            storage_client = storage.Client(project_id)
            bucket = storage_client.bucket(bucket_name)
            file_size = len(await file.read())
            if await FGCSUploadValidation.extensions_validation(file, allowed_extension):
                if await FGCSUploadValidation.size_validation(file_size, maximum_size):
                    blob_path = f'{file_path}/{file_name}' if file_name else f'{file_path}/{file.filename}'
                    key = await FGCSGenerate.encryption_key()
                    b64_decode_key = base64.b64decode(key)
                    blob = bucket.blob(blob_path, encryption_key=b64_decode_key)
                    file.file.seek(0)
                    blob.upload_from_file(file_obj=file.file, content_type=file.content_type)
                    return {
                                'file_name': file_name if file_name else file.filename, 
                                'file_path': blob_path, 
                                'file_size': await FGCSUploadValidation.convert_size(file_size), 
                                'content_type': file.content_type,
                                'encryption_key': key
                            }
                else:
                    raise FailedValidation(reason='attachment size exceeds the maximum size', message='validation failed', file_name=file.filename)
            else:
                raise FailedValidation(reason='unsupported extension', message='validation failed', file_name=file.filename)
        except Exception as e:
            raise e

    @classmethod
    async def file(cls, project_id: str, bucket_name: str,  file: UploadFile, file_path: str, maximum_size: int, allowed_extension: list, file_name: str = None):
        try:
            storage_client = storage.Client(project_id)
            bucket = storage_client.bucket(bucket_name)
            file_size = len(await file.read())
            if await FGCSUploadValidation.extensions_validation(file, allowed_extension):
                if await FGCSUploadValidation.size_validation(file_size, maximum_size):
                    blob_path = f'{file_path}/{file_name}' if file_name else f'{file_path}/{file.filename}'
                    blob = bucket.blob(blob_path)
                    file.file.seek(0)
                    blob.upload_from_file(file_obj=file.file, content_type=file.content_type)
                    return {
                                'file_name': file_name if file_name else file.filename, 
                                'file_path': blob_path, 
                                'file_size': await FGCSUploadValidation.convert_size(file_size), 
                                'content_type': file.content_type
                            }
                else:
                    raise FailedValidation(reason='attachment size exceeds the maximum size', message='validation failed', file_name=file.filename)
            else:
                raise FailedValidation(reason='unsupported extension', message='validation failed', file_name=file.filename)
        except Exception as e:
            raise e

    @classmethod
    async def multiple_file(cls, project_id: str, bucket_name: str, file_list: list, file_path: str, maximum_size: int, allowed_extension: list, is_custom_file_name: bool = False, is_replace: bool= True):
        try:
            storage_client = storage.Client(project_id)
            bucket = storage_client.bucket(bucket_name)
            documents = []
            for i in file_list:
                file_size = len(await i['file_object'].read())
                file_object = i['file_object']
                file_name = i['file_name']
                is_public = i['is_public']
                if await FGCSUploadValidation.extensions_validation(file_object, allowed_extension):
                    if await FGCSUploadValidation.size_validation(file_size, maximum_size):
                        blob_path = f'{file_path}/{file_name}' if is_custom_file_name else  f'{file_path}/{file_object.filename}'
                        blob = bucket.blob(blob_path)
                        file_object.file.seek(0)
                        if not is_replace and blob.exists():
                                blob = bucket.blob(f'{blob_path}_{str(uuid4())}')
                        blob.upload_from_file(file_obj=file_object.file, content_type=file_object.content_type)
                        documents.append({
                                    'file_name': file_name if is_custom_file_name else file_object.filename, 
                                    'file_path': blob_path, 
                                    'file_size': await FGCSUploadValidation.convert_size(file_size), 
                                    'content_type': file_object.content_type
                                })
                        if is_public:
                            blob.make_public()
                        return documents
                    else:
                        raise FailedValidation(reason='attachment size exceeds the maximum size', message='validation failed', file_name=file_object.filename)
                else:
                    raise FailedValidation(reason='unsupported extension', message='validation failed', file_name=file_object.filename)
        except Exception as e:
            raise e

    @classmethod
    async def multiple_encrypted_file(cls, project_id: str, bucket_name: str, file_list: list, path: str, maximum_size: int, allowed_extension: list, is_custom_file_name: bool = False, is_replace: bool= True):
        try:
            storage_client = storage.Client(project_id)
            bucket = storage_client.bucket(bucket_name)
            documents = []
            for i in file_list:
                file_size = len(await i['file_object'].read())
                file_object = i['file_object']
                file_name = i['file_name']
                if await FGCSUploadValidation.extensions_validation(file_object, allowed_extension):
                    if await FGCSUploadValidation.size_validation(file_size, maximum_size):
                        blob_path = f'{path}/{file_name}' if is_custom_file_name else  f'{path}/{file_object.filename}'
                        key = await FGCSGenerate.encryption_key()
                        b64_decode_key = base64.b64decode(key)
                        blob = bucket.blob(blob_path, encryption_key=b64_decode_key)
                        file_object.file.seek(0)
                        if not is_replace and blob.exists():
                                blob = bucket.blob(f'{blob_path}_{str(uuid4())}', encryption_key=b64_decode_key)
                        blob = bucket.blob(blob_path, encryption_key=b64_decode_key)
                        file_object.file.seek(0)
                        if not is_replace and blob.exists():
                                blob = bucket.blob(f'{blob_path}_{str(uuid4())}')
                        blob.upload_from_file(file_obj=file_object.file, content_type=file_object.content_type)
                        documents.append({
                                    'file_name': file_name if is_custom_file_name else file_object.filename, 
                                    'file_path': blob_path, 
                                    'file_size': await FGCSUploadValidation.convert_size(file_size), 
                                    'content_type': file_object.content_type
                                })
                        return documents
                    else:
                        raise FailedValidation(reason='attachment size exceeds the maximum size', message='validation failed', file_name=file_object.filename)
                else:
                    raise FailedValidation(reason='unsupported extension', message='validation failed', file_name=file_object.filename)
        except Exception as e:
            raise e