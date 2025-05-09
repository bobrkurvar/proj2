from pydantic import BaseModel
#import datetime

class TodoInput(BaseModel):
    name: str
    content: str
    doer_id: int | None = None