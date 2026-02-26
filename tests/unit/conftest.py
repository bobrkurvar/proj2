import pytest

from app.domain import Task, TaskExecutors, RequestsToExecutor
from tests.fakes import (FakeCRUD, FakeStorage, Table)

@pytest.fixture
def storage():
    storage = FakeStorage()
    storage.register_tables(
        [
            Table(
                name=Task,
                columns=["id", "description", "date_of_creation", "public", "deadline", "owner_id"],
                defaults={"id": 1}
            ),
            Table(
                name=TaskExecutors,
                columns=["task_id", "user_id"]
            ),
            Table(
                name=RequestsToExecutor,
                columns=["task_id", "user_id", "owner_to_user"]
            )
        ]
    )

    return storage


@pytest.fixture
def manager(storage):
    return FakeCRUD(storage)

