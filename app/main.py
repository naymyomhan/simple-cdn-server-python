

import io
import base64
import os
import time
import re
import uuid
import json
from fastapi import Body, FastAPI, HTTPException,Depends
from pydantic import BaseModel
from PIL import Image
from datetime import datetime,timedelta
from fastapi.responses import FileResponse
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
from helper import check_file_type
from request.image_upload_request import ImageUploadRequest
from request.presign_request import PresignRequest
from constants import ALLOWED_EXTENSIONS,AUDIO_EXTENSIONS,IMAGE_EXTENSIONS,VIDEO_EXTENSIONS
from image_upload import generate_random_filename, upload_and_save_image


from presign import get_file_name_by_presign_key, is_valid_presign_key,insert_presign
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
    if api_key == os.environ.get('API_KEY'):
        return True
    else:
        raise HTTPException(status_code=403, detail="API key is invalid")




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
            filename =generate_random_filename(datetime.now(),file_extension)
            path = request.path
            file_type = check_file_type(file_extension)

            # Insert presign
            response = insert_presign(cursor, connection, presign_key, filename, path, file_type)

            connection.commit()
            return response
        finally:
            close_connection(cursor,connection)

    except Exception as e:
        close_connection(cursor,connection)
        raise HTTPException(status_code=500, detail=str(e))






@app.post("/api/image/upload")
async def upload_image(request: ImageUploadRequest,verified: bool = Depends(verify_api_key)):
    connection = establish_connection()

    try:
        image_data = base64.b64decode(request.base64_data)
        presign_key = request.presign_key

        cursor = connection.cursor()

        # Check presign key
        if not is_valid_presign_key(cursor, presign_key):
            return fail_response("Invalid presign key", 400)
        
        #Get file name using presign key
        file_name=get_file_name_by_presign_key(cursor, presign_key)
        if(file_name == None or file_name==""):
            return fail_response("Invalid presign key",400)

        response_data = upload_and_save_image(image_data, file_name)
        return success_response("Upload successful",response_data)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error {str(e)}")
    finally:
        close_connection(cursor, connection)




#protected template
@app.get("/protected-resource")
async def get_protected_resource(verified: bool = Depends(verify_api_key)):
    return {"message": "This is a protected resource"}







#view image
@app.get("/images/{image_name}")
async def get_image(image_name: str, verified: bool = Depends(verify_api_key)):
    image_dir = "upload/original"

    image_path = f"{image_dir}/{image_name}"

    return FileResponse(image_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
