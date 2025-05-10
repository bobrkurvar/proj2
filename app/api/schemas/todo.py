from pydantic import BaseModel
#import datetime

class TodoInput(BaseModel):
    name: str
    content: str
    doer_id: int | None = None

class TodoUpdate(BaseModel):
    ident: tuple
    name: str | None = None
    content: str | None = None
    is_delete: bool = False