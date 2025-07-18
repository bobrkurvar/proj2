from .crud import Crud
from core import conf

def get_db_manager() -> Crud:
    db_url = str(conf.db_url)
    return Crud(db_url)
