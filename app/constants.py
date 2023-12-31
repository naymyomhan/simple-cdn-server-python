import os
from dotenv import load_dotenv
load_dotenv()


ALLOWED_EXTENSIONS = {'png', 'jpg','gif','bmp','webp','tiff','mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'mpeg','mp3', 'wav', 'flac', 'aac','ogg','wma','aiff'}
IMAGE_EXTENSIONS = {'png', 'jpg','gif','bmp','webp','tiff'}
VIDEO_EXTENSIONS = {'mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'mpeg'}
AUDIO_EXTENSIONS = {'mp3', 'wav', 'flac', 'aac','ogg','wma','aiff'}

APP_URL = os.environ.get('APP_URL')
STORAGE_PATH = os.environ.get('STORAGE_PATH')
IMAGE_PATH = f"{STORAGE_PATH}/image"
AUDIO_PATH = f"{STORAGE_PATH}/audio"
FILE_PATH = f"{STORAGE_PATH}"
