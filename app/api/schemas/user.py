from pydantic import BaseModel

class UserInputFromBot(BaseModel):
    id: int
    activity: bool = True
    first_name: str
    last_name: str




