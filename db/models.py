from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.types import Date, BigInteger
from sqlalchemy import ForeignKey
import datetime

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'bot_user'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    activity: Mapped[bool] = mapped_column(default=True)
    task: Mapped[list["Todo"]] = relationship("Todo", back_populates="user")

    def __str__(self):
        text = f"id: {self.id}, first_name: {self.first_name}, last_name: {self.last_name}, activity: {self.activity}"
        return text

    def __repr__(self):
        text = f"id: {self.id}, first_name: {self.first_name}, last_name: {self.last_name}, activity: {self.activity}"
        return text

    def to_dict(self):
        return {'id': self.id, "first_name": self.first_name, "last_name": self.last_name, "activity": self.activity}

class Todo(Base):
    __tablename__ = 'todo'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    data_of_creation: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today())
    data_of_change: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today())
    doer_id: Mapped[int] = mapped_column(ForeignKey("bot_user.id"), index=True)
    user: Mapped[User] = relationship("User", back_populates="task")

    def __str__(self):
        text = f"task: {self.name}, content: {self.content}"
        return text

    def to_dict(self):
        return {'id': self.id, "name": self.name, "content": self.content,
                "data_of_creation": self.data_of_creation,
                "data_of_change": self.data_of_change, "doer_id": self.doer_id}