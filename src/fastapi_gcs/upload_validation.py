from fastapi import UploadFile

class UploadValidation:
    @classmethod
    async def convert_size(cls, size_bytes):
        try:
            import math
            if size_bytes == 0:
                return "0B"
            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
            i = int(math.floor(math.log(size_bytes, 1024)))
            p = math.pow(1024, i)
            s = round(size_bytes / p, 2)
            return "%s %s" % (s, size_name[i])
        except Exception as e:
            raise e

    @classmethod
    async def extensions_validation(cls, file: UploadFile,  allowed_ext: list):
        try:
            extension = file.content_type.split('/')[-1]
            if extension in allowed_ext:
                return True
            return False
        except Exception as e:
            raise e

    @classmethod
    async def size_validation(self, file_size: int, max_size: int):
        try: 
            if file_size > max_size:
                return False
            return True
        except Exception as e:
            raise e
