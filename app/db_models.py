import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger, Date


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str]
    own_tasks: Mapped[list["Task"]] = relationship("Task", back_populates="owner")
    tasks: Mapped[list["TaskExecutors"]] = relationship(
        "TaskExecutors", back_populates="users"
    )
    requests: Mapped[list["RequestsToExecutor"]] = relationship(
        "RequestsToExecutor", back_populates="users"
    )

    def model_dump(self):
        return {"id": self.id, "username": self.username}


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    description: Mapped[str]
    date_of_creation: Mapped[datetime] = mapped_column(
        Date, default=datetime.date.today()
    )
    public: Mapped[bool]
    deadline: Mapped[datetime] = mapped_column(Date, default=None)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    owner: Mapped["User"] = relationship("User", back_populates="own_tasks")
    executors: Mapped[list["TaskExecutors"]] = relationship(
        "TaskExecutors",
        back_populates="tasks",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    requests: Mapped[list["RequestsToExecutor"]] = relationship(
        "RequestsToExecutor",
        back_populates="tasks",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def model_dump(self):
        return {
            "id": self.id,
            "content": self.description,
            "data_of_creation": self.date_of_creation,
            "deadline": self.deadline,
            "owner_id": self.owner_id,
            "public": self.public,
        }


class TaskExecutors(Base):
    __tablename__ = "task_executors"
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    tasks: Mapped["Task"] = relationship("Task", back_populates="executors")
    users: Mapped["User"] = relationship("User", back_populates="tasks")

    def model_dump(self):
        return {"task_id": self.task_id, "user_id": self.user_id}


class RequestsToExecutor(Base):
    __tablename__ = "requests"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    owner_request: Mapped[bool]
    tasks: Mapped["Task"] = relationship("Task", back_populates="requests")
    users: Mapped["User"] = relationship("User", back_populates="requests")

    def model_dump(self):
        return {
            "task_id": self.task_id,
            "user_id": self.user_id,
            "owner_request": self.owner_request,
        }
