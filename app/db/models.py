import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger, Date, Integer


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "bot_user"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str]
    task: Mapped[list["Todo"]] = relationship("Todo", back_populates="user")

    def __str__(self):
        text = f"id: {self.id}, username: {self.username}"
        return text

    def __repr__(self):
        text = f"id: {self.id}, username: {self.username}"
        return text

    def model_dump(self):
        return {"id": self.id, "username": self.username}


class Todo(Base):
    __tablename__ = "todo"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]
    content: Mapped[str]
    date_of_creation: Mapped[datetime.date] = mapped_column(
        Date, default=datetime.date.today()
    )
    deadline: Mapped[datetime.date | None] = mapped_column(Date, default=None)
    doer_id: Mapped[int] = mapped_column(ForeignKey("bot_user.id"), index=True)
    user: Mapped[User] = relationship("User", back_populates="task")

    def __str__(self):
        text = f"task: {self.name}, content: {self.content}"
        return text

    def __repr__(self):
        text = f"task: {self.name}, content: {self.content}"
        return text

    def model_dump(self):
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "data_of_creation": self.date_of_creation,
            "deadline": self.deadline,
            "doer_id": self.doer_id,
        }
