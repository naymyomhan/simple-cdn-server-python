from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from hashlib import md5
from cachetools import TTLCache

app = FastAPI()

# Set the maximum number of items in the cache and the time-to-live (TTL) in seconds
CACHE_MAX_SIZE = 1000
CACHE_TTL = 3600  # 1 hour

image_cache = TTLCache(maxsize=CACHE_MAX_SIZE, ttl=CACHE_TTL)

def get_cache_key(image_path):
    return md5(image_path.encode()).hexdigest()

@app.get("/coderverse/{path:path}/{image_name}")
async def get_image(image_name: str, path: str):
    image_path = f"storage/{path}/{image_name}"
    cache_key = get_cache_key(image_path)

    cached_image = image_cache.get(cache_key)
    if cached_image:
        return FileResponse(cached_image)

    try:
        with open(image_path, 'rb') as file:
            image_data = file.read()

        image_cache[cache_key] = image_data

        return FileResponse(image_data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
