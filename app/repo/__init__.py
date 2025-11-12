from core import conf

from .crud import Crud


def get_db_manager():
    from app.db.models import Todo, User
    from app.domain import user
    from app.domain import todo

    db_url = str(conf.db_url)
    manager = Crud(db_url)

    manager.register(user.User, User)
    manager.register(todo.Todo, Todo)

    return manager
