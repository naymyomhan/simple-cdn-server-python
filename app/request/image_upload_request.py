from pydantic import BaseModel


class ImageUploadRequest(BaseModel):
    base64_data: str
    presign_key: str