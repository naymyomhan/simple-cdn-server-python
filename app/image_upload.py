import os
import uuid
from PIL import Image
from dotenv import load_dotenv
load_dotenv()


UPLOAD_DIR = os.environ.get('UPLOAD_DIR')
ORIGINAL_DIR = f"{UPLOAD_DIR}/{os.environ.get('ORIGINAL_DIR')}"
COMPRESSED_DIR = f"{UPLOAD_DIR}/{os.environ.get('COMPRESSED_DIR')}"
THUMBNAIL_DIR = f"{UPLOAD_DIR}/{os.environ.get('THUMBNAIL_DIR')}"

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
def save_compress_image(original_path, compressed_path, size=(720, 720)):
    thumbnail = Image.open(original_path)
    thumbnail.thumbnail(size)
    thumbnail.save(compressed_path)

#Save Thumbnail Size Image
def save_thumbnail_image(original_path, thumbnail_path, size=(720, 720)):
    thumbnail = Image.open(original_path)
    thumbnail.thumbnail(size)
    thumbnail.save(thumbnail_path)

#Create CDN Url
def get_cdn_url(file_name):
    return f"{os.environ.get('UPLOAD_DIR')}/images/{file_name}"

#Upload and Save Images
def upload_and_save_image(image_data,file_name):
    create_dirs_if_not_exists(ORIGINAL_DIR, COMPRESSED_DIR,THUMBNAIL_DIR)

    original_path = os.path.join(ORIGINAL_DIR, file_name)
    compressed_path = os.path.join(COMPRESSED_DIR, file_name)
    thumbnail_path = os.path.join(THUMBNAIL_DIR, file_name)

    save_image(original_path, image_data)
    save_compress_image(original_path, compressed_path)
    save_thumbnail_image(original_path, thumbnail_path)

    original_cdn_url = get_cdn_url(file_name)
    thumbnail_cdn_url = get_cdn_url(file_name)

    return {
        "message": f"Uploaded image '{file_name}' and saved in {original_path}",
        "original": original_cdn_url,
        "thumbnail": thumbnail_cdn_url
    }

#Generate random name for new file
def generate_random_filename(created_date,file_extension):
    random_string = str(uuid.uuid4())
    filename = f"ludu_network_{random_string}_{created_date.strftime('%d_%m_%Y')}.{file_extension}"
    return filename