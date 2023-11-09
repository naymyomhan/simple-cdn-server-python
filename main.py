
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
from fastapi.responses import FileResponse
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv


from presign import is_valid_presign_key,insert_presign
from response import success_response,fail_response
from database import establish_connection, init_db, close_connection


app = FastAPI()
load_dotenv()




#Secure
api_key = APIKeyHeader(name="X-API-KEY")
def verify_api_key(api_key: str = Depends(api_key)):
    if api_key == os.environ.get('API_KEY'):
        return True
    else:
        raise HTTPException(status_code=403, detail="API key is invalid")







class PresignRequest(BaseModel):
    file_name: str

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@app.post("/presign")
async def presign(request: PresignRequest,verified: bool = Depends(verify_api_key)):
    try:
        if not request.file_name.lower().split('.')[-1] in ALLOWED_EXTENSIONS:
            return fail_response("Don't allowed file extensions",400)
            
        connection = establish_connection()
        
        try:
            cursor = connection.cursor()

            presign_key = str(uuid.uuid4())
            filename =  request.file_name
            filename = filename.strip()

            # Insert presign
            response = insert_presign(cursor, connection, presign_key, filename)

            connection.commit()
            return response
        finally:
            close_connection(cursor,connection)

    except Exception as e:
        close_connection(cursor,connection)
        raise HTTPException(status_code=500, detail=str(e))









class ImageUploadRequest(BaseModel):
    base64_data: str
    presign_key: str

#upload image
@app.post("/api/image/upload")
async def upload_image(request: ImageUploadRequest):

    connection = establish_connection()
    try:    
        image_data = base64.b64decode(request.base64_data)
        presign_key = request.presign_key
        cursor = connection.cursor()
        print(presign_key)

        #check presign key
        if(is_valid_presign_key(cursor,presign_key)==False):
            return fail_response("Invalid presign key",400)
        
        file_name = "generated.png"

        upload_dir = "upload"
        original_dir = f"{upload_dir}/original"
        thumbnail_dir = f"{upload_dir}/thumbnail"

        if not os.path.exists(original_dir):
            os.makedirs(original_dir)

        if not os.path.exists(thumbnail_dir):
            os.makedirs(thumbnail_dir)

        file_path = os.path.join(original_dir, file_name)

        with open(file_path, "wb") as file:
            file.write(image_data)
            
        thumbnail = Image.open(file_path)
        thumbnail.thumbnail((720, 720))#(width, height)

        thumbnail_path = os.path.join(thumbnail_dir, file_name)
        thumbnail.save(thumbnail_path)

        cdn_url = f"http://127.0.0.1:8000/images/{file_name}"
        thumbnail_cdn_url = f"http://127.0.0.1:8000/images/{file_name}"

        return {
            "message": f"Uploaded image '{file_name}' and saved in {file_path}",
            "original": cdn_url,
            "thumbnail": thumbnail_cdn_url
        }
        

    except Exception as e:
        raise HTTPException(status_code=400, detail="Error "+e)

    










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
