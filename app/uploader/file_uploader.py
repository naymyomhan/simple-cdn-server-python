import os
from PIL import Image
import uuid
from dotenv import load_dotenv
from response import success_response
from helper import createDirsIfNotExists

from constants import FILE_PATH, STORAGE_PATH
load_dotenv()


#Save Compressed Image (720)
def compressAndSave(original_image, compressed_image, size):
    thumbnail = Image.open(original_image)
    thumbnail.thumbnail(size)
    thumbnail.save(compressed_image)


def saveMedia(original_file,file_upload_path,file_name):
    compressed_path = os.path.join(file_upload_path,"media")
    compressed_file = os.path.join(compressed_path,file_name)
    createDirsIfNotExists(compressed_path)
    compressAndSave(original_file,compressed_file,(1200,628))


def saveThumbnail(original_file,file_upload_path,file_name):
    compressed_path = os.path.join(file_upload_path,"thumbnail")
    compressed_file = os.path.join(compressed_path,file_name)
    createDirsIfNotExists(compressed_path)
    compressAndSave(original_file,compressed_file,(300,300))


#Upload File
def uploadFile(file,file_path,file_name,file_type):
    try:
        
        current_upload_path = f"{FILE_PATH}/{file_type}"
        file_upload_path = f"{current_upload_path}/{file_path}"
        createDirsIfNotExists(STORAGE_PATH, FILE_PATH,current_upload_path,file_upload_path)



        original_path = os.path.join(file_upload_path, "source")
        createDirsIfNotExists(original_path)
        original_file = os.path.join(original_path, file_name)

        file.save(original_file)

        print(file_type)
        
        if file_type == 'Image':
            saveMedia(original_file,file_upload_path,file_name)
            saveThumbnail(original_file,file_upload_path,file_name)


        cdn_url = f"{os.environ.get('APP_URL')}/coderverse/{file_type}/{file_path}/{file_name}?ql=media"
        return {
            "url": cdn_url,
        }
    except Exception as e:
        return e