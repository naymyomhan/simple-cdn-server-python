from pydantic import BaseModel


class PresignRequest(BaseModel):
    file_name: str
    file_path:str