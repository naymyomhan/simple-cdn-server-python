import os
import uuid
from PIL import Image
from dotenv import load_dotenv

from constants import IMAGE_PATH, STORAGE_PATH
load_dotenv()




#Create Folders 
def create_dirs_if_not_exists(*dirs):
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

#Save Original Image
def save_image(file_path, image_data):
    with open(file_path, "wb") as file:
        file.write(image_data)

#Save Compressed Image (720)
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
def upload_and_save_image(image_data,file_path,file_name):
    current_upload_path = f"{IMAGE_PATH}/{file_path}"
    original_upload_path = f"{current_upload_path}/Original"
    compressed_upload_path = f"{current_upload_path}/Compressed"
    thumbnail_upload_path = f"{current_upload_path}/Thumbnail"

    create_dirs_if_not_exists(STORAGE_PATH, IMAGE_PATH,current_upload_path,original_upload_path,compressed_upload_path,thumbnail_upload_path)

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
        "message": f"Uploaded image '{file_name}' and saved in {original_path}",
        "original": original_cdn_url,
        "compressed":compressed_cdn_url,
        "thumbnail": thumbnail_cdn_url
    }

#Generate random name for new file
def generate_random_filename(created_date,file_extension):
    random_string = str(uuid.uuid4())
    filename = f"ludu_network_{random_string}_{created_date.strftime('%d_%m_%Y')}.{file_extension}"
    return filename