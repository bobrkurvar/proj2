from pydantic import BaseModel

# class UserInput(BaseModel):
#     id: int
#     activity: bool = True
#     first_name: str
#     last_name: str | None

class UserInput(BaseModel):
    id: int
    username: str

class UserOutput(BaseModel):
    id: int
    username: str



