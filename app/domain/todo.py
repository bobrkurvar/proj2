from datetime import date


class Todo:
    def __init__(
        self,
        name: str,
        content: str,
        date_of_creation: date = date.today(),
        deadline: date | None = None,
        todo_id: int = 0,
    ):
        self.id = todo_id
        self.name = name
        self.content = content
        self.date_of_creation = date_of_creation
        self.deadline = deadline

    def model_dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "date_of_creation": self.date_of_creation,
            "deadline": self.deadline,
        }
