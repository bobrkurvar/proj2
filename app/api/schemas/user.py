from pydantic import BaseModel

class UserOutputForBot(BaseModel):
    first_name: str
    last_name: str

class UserInputFromBot(BaseModel):
    id: int
    activity: bool
    first_name: str
    last_name: str

class UserInput(BaseModel):
    username: str
    password: str
