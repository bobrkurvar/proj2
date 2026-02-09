from datetime import datetime


class Task:
    def __init__(
        self,
        name: str,
        content: str,
        todo_id: int,
        deadline: datetime | None = None,
    ):
        self.id = todo_id
        self.name = name
        self.content = content
        self.date_of_creation = datetime.today()
        self.deadline = deadline

class RequestsToExecutor:
    def __init__(self, task_id: int, user_id: int):
        self.task_id = task_id
        self.user_id = user_id



