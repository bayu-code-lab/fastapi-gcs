## Requirements

Python 3.7+

## Installation

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

## Example

### Create it

* Create a file `main.py` with:

```Python
from fastapi_gcs import FGCSUpload, FGCSGenerate, FGCSDelete
from fastapi import FastAPI, File, UploadFile

app = FastAPI()


#Upload File
@app.post("/upload-file/")
async def create_upload_file(file: UploadFile):
    return await FGCSUpload.file(
    	project_id={google_project_id}, 
        bucket_name={google_bucket_name}, 
        file=file, 
        file_path='my_data/test', 
        maximum_size=2_097_152, 
        allowed_extension= ['png', 'jpg'],
        #file_name='my_file.png' #optional custom file name
    )
    
#Upload File Response
# {
#     'file_name': 'my_file.png', 
#     'file_path': 'my_data/test/my_file.png', 
#     'file_size': '200 KB', 
#     'content_type': 'image/png'
# }


#Upload Encrypted File
@app.post("/upload-ecrypted-file/")
async def create_upload_file(file: UploadFile):
    return await FGCSUpload.encrypted_file(
    	project_id={google_project_id}, 
        bucket_name={google_bucket_name}, 
        file=file, 
        file_path='my_data/test', 
        maximum_size=2_097_152, 
        allowed_extension= ['png', 'jpg'],
        #file_name='my_file.png' #optional custom file name
    )
    
#Upload Encrypted File Response
# {
#     'file_name': 'my_file.png', 
#     'file_path': 'my_data/test/my_file.png', 
#     'file_size': '200 KB', 
#     'content_type': 'image/png',
#     'encryption_key': 'xxxxxxxxxxxxxxxxxx'
# }
  
  
#Generate Signed Url
@app.post("/generate-signed-url/")
async def create_upload_file(file_path: str):
    return await FGCSGenerate.signed_url(
    	project_id={google_project_id}, 
        bucket_name={google_bucket_name},  
        file_path=file_path #'my_data/test/my_file.png', 
        expiration_hour=1
    )
    
#Response Generate Signed Url
#https://storage.googleapis.com/example-bucket/cat.jpeg?X-Goog-Algorithm=
#GOOG4-RSA-SHA256&X-Goog-Credential=example%40example-project.iam.gserviceaccount
#.com%2F20181026%2Fus-central1%2Fstorage%2Fgoog4_request&X-Goog-Date=20181026T18
#1309Z&X-Goog-Expires=900&X-Goog-SignedHeaders=host&X-Goog-Signature=247a2aa45f16
#9edf4d187d54e7cc46e4731b1e6273242c4f4c39a1d2507a0e58706e25e3a85a7dbb891d62afa849
#6def8e260c1db863d9ace85ff0a184b894b117fe46d1225c82f2aa19efd52cf21d3e2022b3b868dc
#c1aca2741951ed5bf3bb25a34f5e9316a2841e8ff4c530b22ceaa1c5ce09c7cbb5732631510c2058
#0e61723f5594de3aea497f195456a2ff2bdd0d13bad47289d8611b6f9cfeef0c46c91a455b94e90a
#66924f722292d21e24d31dcfb38ce0c0f353ffa5a9756fc2a9f2b40bc2113206a81e324fc4fd6823
#a29163fa845c8ae7eca1fcf6e5bb48b3200983c56c5ca81fffb151cca7402beddfc4a76b13344703
#2ea7abedc098d2eb14a7
        
#Delete File
@app.post("/delete_file/")
async def create_upload_file(file_path: str):
    await FGCSDelete.file(
    	project_id={google_project_id}, 
        bucket_name={google_bucket_name},  
        file_path=file_path #'my_data/test/my_file.png'
    )
```
