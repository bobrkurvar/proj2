from datetime import datetime

from pydantic import BaseModel


class TaskInput(BaseModel):
    description: str
    owner_id: int | None = None
    deadline: datetime | None = None
    public: bool = False


class TaskUpdate(BaseModel):
    ident: str = "id"
    ident_val: int
    name: str | None = None
    content: str | None = None
    deadline: datetime | None = None
    is_delete: bool = False
