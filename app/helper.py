from constants import AUDIO_EXTENSIONS, IMAGE_EXTENSIONS, VIDEO_EXTENSIONS


def check_file_type(extension):
    if extension in IMAGE_EXTENSIONS:
        return 'Image'
    elif extension in VIDEO_EXTENSIONS:
        return 'Video'
    elif extension in AUDIO_EXTENSIONS:
        return 'Audio'
    else:
        return 'Unknown'