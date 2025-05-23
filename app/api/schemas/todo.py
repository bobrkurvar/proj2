from pydantic import BaseModel
#from datetime import date

class TodoInput(BaseModel):
    name: str
    content: str
    doer_id: int | None = None
    deadline: dict[str, int] | None = None

class TodoUpdate(BaseModel):
    ident: tuple
    name: str | None = None
    content: str | None = None
    is_delete: bool = False