import os
from PIL import Image
from dotenv import load_dotenv
from helper import createDirsIfNotExists

from constants import IMAGE_PATH, STORAGE_PATH
load_dotenv()



#Save Original Image
def save_image(file_path, image_data):
    with open(file_path, "wb") as file:
        file.write(image_data)

#Save Compressed Image (1200)
def save_compress_image(original_path, compressed_path, size=(1200,628)):
    thumbnail = Image.open(original_path)
    thumbnail.thumbnail(size)
    thumbnail.save(compressed_path)

#Save Thumbnail Size Image
def save_thumbnail_image(original_path, thumbnail_path, size=(300, 300)):
    thumbnail = Image.open(original_path)
    thumbnail.thumbnail(size)
    thumbnail.save(thumbnail_path)



#Upload and Save Images
def uploadImage(image_data,file_path,file_name):
    current_upload_path = f"{IMAGE_PATH}/{file_path}"
    original_upload_path = f"{current_upload_path}/Original"
    compressed_upload_path = f"{current_upload_path}/Compressed"
    thumbnail_upload_path = f"{current_upload_path}/Thumbnail"

    createDirsIfNotExists(STORAGE_PATH, IMAGE_PATH,current_upload_path,original_upload_path,compressed_upload_path,thumbnail_upload_path)

    original_path = os.path.join(original_upload_path, file_name)
    compressed_path = os.path.join(compressed_upload_path, file_name)
    thumbnail_path = os.path.join(thumbnail_upload_path, file_name)

    save_image(original_path, image_data)
    save_compress_image(original_path, compressed_path)
    save_thumbnail_image(original_path, thumbnail_path)

    original_cdn_url = f"{os.environ.get('APP_URL')}/coderverse/Image/{file_path}/Original/{file_name}"
    compressed_cdn_url = f"{os.environ.get('APP_URL')}/coderverse/Image/{file_path}/Compressed/{file_name}"
    thumbnail_cdn_url = f"{os.environ.get('APP_URL')}/coderverse/Image/{file_path}/Compressed/{file_name}"

    return {
        "original": original_cdn_url,
        "compressed":compressed_cdn_url,
        "thumbnail": thumbnail_cdn_url
    }