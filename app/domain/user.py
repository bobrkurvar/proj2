class User:
    def __init__(self, username: str, user_id: int):
        self.id = user_id
        self.username = username


class TaskExecutors:
    def __init__(self, task_id: int, user_id: int):
        self.id = user_id
        self.username = task_id
