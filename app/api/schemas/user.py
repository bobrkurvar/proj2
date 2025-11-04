from pydantic import BaseModel


class UserInput(BaseModel):
    id: int
    username: str

class UserDelete(BaseModel):
    activity: bool | None = None
    username: str | None = None

class UserOutput(BaseModel):
    id: int
    username: str

