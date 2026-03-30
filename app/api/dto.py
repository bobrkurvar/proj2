from datetime import datetime
from pydantic import BaseModel


class TaskInput(BaseModel):
    description: str
    owner_id: int
    deadline: datetime | None = None
    public: bool = False
    executors: list[int] = None


class TaskUpdate(BaseModel):
    ident: str = "id"
    ident_val: int
    name: str | None = None
    content: str | None = None
    deadline: datetime | None = None
    is_delete: bool = False


class UserInput(BaseModel):
    id: int
    username: str


class UserDelete(BaseModel):
    #activity: bool | None = None
    username: str | None = None


class UserOutput(BaseModel):
    id: int
    username: str
