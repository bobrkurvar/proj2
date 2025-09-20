from pydantic import BaseModel
from datetime import date

class TodoInput(BaseModel):
    id: int | None = None
    name: str
    content: str
    doer_id: int | None = None
    deadline: date | None = None

class TodoOutput(BaseModel):
    id: int
    name: str
    content: str
    doer_id: int
    deadline: date

class TodoUpdate(BaseModel):
    ident: str = 'id'
    ident_val: int
    name: str | None = None
    content: str | None = None
    deadline: date | None = None
    is_delete: bool = False

