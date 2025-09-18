from .crud import Crud
from core import conf

def get_db_manager():
    db_url = str(conf.db_url)
    manager = Crud(db_url)
    return manager

