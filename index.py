from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel
import io
import base64
import os
from PIL import Image
from fastapi.responses import FileResponse
from fastapi.security import APIKeyHeader
import time

app = FastAPI()

# Step 2: Define the API key security scheme
api_key = APIKeyHeader(name="api_key")

def verify_api_key(api_key: str = Depends(api_key)):
    if api_key == "your_api_key":
        return True
    else:
        raise HTTPException(status_code=403, detail="API key is invalid")

class ImageUploadRequest(BaseModel):
    name: str
    base64_data: str

@app.post("/api/upload")
async def upload_image(request: ImageUploadRequest):
    try:
        image_data = base64.b64decode(request.base64_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid base64 data")

    upload_dir = "upload"
    original_dir = f"{upload_dir}/original"
    thumbnail_dir = f"{upload_dir}/thumbnail"

    if not os.path.exists(original_dir):
        os.makedirs(original_dir)

    if not os.path.exists(thumbnail_dir):
        os.makedirs(thumbnail_dir)

    file_path = os.path.join(original_dir, request.name)

    with open(file_path, "wb") as file:
        file.write(image_data)

    start_time = time.time()

    thumbnail = Image.open(file_path)
    thumbnail.thumbnail((720, 720))#(width, height)

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Image resizing took {execution_time} seconds")

    thumbnail_path = os.path.join(thumbnail_dir, request.name)
    thumbnail.save(thumbnail_path)

    cdn_url = f"http://127.0.0.1:8000/upload/original/{request.name}"
    thumbnail_cdn_url = f"http://127.0.0.1:8000/upload/thumbnail/{request.name}"

    return {
        "message": f"Uploaded image '{request.name}' and saved in {file_path}",
        "original": cdn_url,
        "thumbnail": thumbnail_cdn_url
    }

@app.get("/protected-resource")
async def get_protected_resource(verified: bool = Depends(verify_api_key)):
    return {"message": "This is a protected resource"}


@app.get("/images/{image_name}")
async def get_image(image_name: str, verified: bool = Depends(verify_api_key)):
    image_dir = "upload/original"

    image_path = f"{image_dir}/{image_name}"

    return FileResponse(image_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
