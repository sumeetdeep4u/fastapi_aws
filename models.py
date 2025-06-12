from pydantic import BaseModel

class User(BaseModel):
    user_id: str
    name: str
    email: str
    file_url: str = ""
