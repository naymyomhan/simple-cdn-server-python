

import io
import base64
import os
import secrets
import time
import re
import uuid
import json
from fastapi import Body, FastAPI, HTTPException,Depends, File, UploadFile, Header
from pydantic import BaseModel
from PIL import Image
from datetime import datetime,timedelta
from fastapi.responses import FileResponse
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
from helper import checkFileType, ramdomFilename
from request.image_upload_request import ImageUploadRequest
from request.presign_request import PresignRequest
from constants import ALLOWED_EXTENSIONS, STORAGE_PATH
from uploader.image_uploader import uploadImage


from presign import get_file_info_by_presign_key, is_valid_presign_key,insert_presign
from response import success_response,fail_response
from database import establish_connection, init_db, close_connection


app = FastAPI()
load_dotenv()

# connection = establish_connection()
# cursor = connection.cursor()
# init_db(cursor)
# close_connection(cursor,connection)


#Secure
api_key = APIKeyHeader(name="X-API-KEY")
def verify_api_key(api_key: str = Depends(api_key)):
    stored_api_key = os.environ.get('API_KEY')
    if secrets.compare_digest(api_key, stored_api_key):
        return True
    else:
        raise HTTPException(status_code=403, detail="unauthorized")





@app.post("/presign")
async def presign(request: PresignRequest,verified: bool = Depends(verify_api_key)):
    try:
        file_extension = request.file_name.strip().lower().split('.')[-1]
        
        if not file_extension in ALLOWED_EXTENSIONS:
            return fail_response("Don't allowed file extensions",400)
            
        connection = establish_connection()
        
        try:
            cursor = connection.cursor()

            presign_key = str(uuid.uuid4())
            filename =ramdomFilename(datetime.now(),file_extension)
            file_path = request.file_path
            file_type = checkFileType(file_extension)

            # Insert presign
            response = insert_presign(cursor, connection, presign_key, filename, file_path, file_type)

            connection.commit()
            return response
        finally:
            close_connection(cursor,connection)

    except Exception as e:
        close_connection(cursor,connection)
        raise HTTPException(status_code=500, detail=str(e))





@app.post("/api/upload")
async def upload_file(request: ImageUploadRequest,verified: bool = Depends(verify_api_key)):
    connection = establish_connection()

    try:
        file_data = base64.b64decode(request.base64_data)
        presign_key = request.presign_key

        cursor = connection.cursor()

        # Check presign key
        if not is_valid_presign_key(cursor, presign_key):
            return fail_response("Invalid presign key", 400)
        
        #Get file name using presign key
        file_info=get_file_info_by_presign_key(cursor, presign_key)
        if not file_info:
            return fail_response("Invalid presign info",400)

        file_name = file_info['file_name']
        file_path = file_info['file_path']
        file_type = file_info['file_type']

        if file_type == 'Image':
            response_data = uploadImage(file_data, file_path, file_name)
        elif file_type == 'Video':
            response_data={}
        elif file_type == 'Audio':
            response_data={}
        else:
            return fail_response("Something went wrong")

        
        return success_response("Upload successful",response_data)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error {str(e)}")
    finally:
        close_connection(cursor, connection)







#view image
@app.get("/coderverse/{path:path}/{image_name}")
async def get_image(image_name: str,path:str,verified: bool = Depends(verify_api_key)):
    print(path)
    image_path = f"{STORAGE_PATH}/{path}/{image_name}"

    if not os.path.exists(image_path):
        return fail_response("File not found",404)

    return FileResponse(image_path)





if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
