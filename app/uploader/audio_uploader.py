import os
import uuid
from dotenv import load_dotenv
from fastapi import HTTPException
from helper import createDirsIfNotExists

from constants import AUDIO_PATH, STORAGE_PATH
load_dotenv()



#Save Original Audio
def saveAudio(file_path, audio_data):
    with open(file_path, "wb") as file:
        file.write(audio_data)


#Upload Audio
def uploadAudio(audio_data,file_path,file_name):
    try:
        current_upload_path = f"{AUDIO_PATH}/{file_path}"
        original_upload_path = f"{current_upload_path}/Original"

        createDirsIfNotExists(STORAGE_PATH, AUDIO_PATH,current_upload_path,original_upload_path)

        original_path = os.path.join(original_upload_path, file_name)

        saveAudio(original_path, audio_data)

        original_cdn_url = f"{os.environ.get('APP_URL')}/coderverse/Audio/{file_path}/Original/{file_name}"

        return {
            "original": original_cdn_url,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))