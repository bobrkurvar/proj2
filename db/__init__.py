
from .crud import Crud
from core import *
from .models import User

db_url = str(conf.DATABASE_URL)
User = User

manager = Crud(db_url)

__all__ = ['manager', 'User']