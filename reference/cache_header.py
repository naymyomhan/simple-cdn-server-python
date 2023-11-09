from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse, Response
from hashlib import md5
import os
from datetime import datetime, timedelta

app = FastAPI()

cache_directory = "image_cache"

def get_cache_key(image_path):
    return md5(image_path.encode()).hexdigest()

def get_cache_path(cache_key):
    return os.path.join(cache_directory, cache_key)

def cache_image(image_path, cache_key):
    cached_path = get_cache_path(cache_key)

    if not os.path.exists(cached_path):
        with open(image_path, 'rb') as file:
            image_data = file.read()

        os.makedirs(os.path.dirname(cached_path), exist_ok=True)

        with open(cached_path, 'wb') as cached_file:
            cached_file.write(image_data)

    return cached_path

def get_cache_headers():
    # Set cache headers for 1 day (adjust as needed)
    expiration_date = datetime.utcnow() + timedelta(days=1)
    cache_control = f"public, max-age={int((expiration_date - datetime.utcnow()).total_seconds())}"
    return {"Cache-Control": cache_control, "Expires": expiration_date.strftime("%a, %d %b %Y %H:%M:%S GMT")}

@app.get("/coderverse/{path:path}/{image_name}")
async def get_image(image_name: str, path: str):
    image_path = f"storage/{path}/{image_name}"
    cache_key = get_cache_key(image_path)

    cached_path = get_cache_path(cache_key)

    if os.path.exists(cached_path):
        return FileResponse(cached_path, headers=get_cache_headers())

    try:
        cached_path = cache_image(image_path, cache_key)
        return FileResponse(cached_path, headers=get_cache_headers())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
