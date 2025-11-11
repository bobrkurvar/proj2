from pydantic import BaseModel, field_serializer
from datetime import date

class TodoInput(BaseModel):
    name: str
    content: str
    doer_id: int | None = None
    deadline: dict | None = None

class TodoOutput(BaseModel):
    id: int
    name: str
    content: str
    doer_id: int
    deadline: date

    @field_serializer("deadline")
    def serialize_deadline(self, v: date):
        return {"year": v.year, "month": v.month, "day": v.day}

class TodoUpdate(BaseModel):
    ident: str = 'id'
    ident_val: int
    name: str | None = None
    content: str | None = None
    deadline: date | None = None
    is_delete: bool = False

