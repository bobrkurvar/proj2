from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.endpoints import main_router
from app.err_handlers import (
    data_base_exception_handler,
    entity_already_exists_in_db_exceptions_handler,
    foreign_key_violation_exceptions_handler,
    global_exception_handler,
    not_found_in_db_exceptions_handler,
)
from app.repo import get_db_manager
from app.repo.exceptions import (
    AlreadyExistsError,
    CustomForeignKeyViolationError,
    DatabaseError,
    NotFoundError,
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    manager = get_db_manager()
    manager.close_and_dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(main_router)


app.add_exception_handler(NotFoundError, not_found_in_db_exceptions_handler)
app.add_exception_handler(
    AlreadyExistsError, entity_already_exists_in_db_exceptions_handler
)
app.add_exception_handler(
    CustomForeignKeyViolationError, foreign_key_violation_exceptions_handler
)
app.add_exception_handler(DatabaseError, data_base_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
