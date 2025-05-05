from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'bot_user'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    activity: Mapped[bool] = mapped_column(default=True)
    tasks = relationship()

    def __str__(self):
        text = f"id: {self.id}, first_name: {self.first_name}, last_name: {self.last_name}, activity: {self.activity}"
        return text

    def __repr__(self):
        text = f"id: {self.id}, first_name: {self.first_name}, last_name: {self.last_name}, activity: {self.activity}"
        return text

class Todo(Base):
    __tablename__ = 'todo'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    content: Mapped[str]

