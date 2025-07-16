from .crud import Crud
from core import *


db_url = str(conf.db_url)
manager = Crud(db_url)
