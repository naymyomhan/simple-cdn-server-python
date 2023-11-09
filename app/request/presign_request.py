from pydantic import BaseModel


class PresignRequest(BaseModel):
    file_name: str
    path:str