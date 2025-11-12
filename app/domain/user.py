class User:
    def __init__(
        self,
        username: str,
        user_id: int = 0,
    ):
        self.id = user_id
        self.username = username

    def model_dump(self):
        return {"id": self.id, "username": self.username}
