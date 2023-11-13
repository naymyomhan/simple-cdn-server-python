import os
import uuid
from constants import AUDIO_EXTENSIONS, IMAGE_EXTENSIONS, VIDEO_EXTENSIONS


def checkFileType(extension):
    if extension in IMAGE_EXTENSIONS:
        return 'image'
    elif extension in VIDEO_EXTENSIONS:
        return 'video'
    elif extension in AUDIO_EXTENSIONS:
        return 'audio'
    else:
        return 'unknow'
    

#Create Folders 
def createDirsIfNotExists(*dirs):
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)



#Generate random name for new file
def ramdomFilename(created_date,file_extension):
    random_string = str(uuid.uuid4())
    filename = f"ludu_network_{random_string}_{created_date.strftime('%d_%m_%Y')}.{file_extension}"
    return filename