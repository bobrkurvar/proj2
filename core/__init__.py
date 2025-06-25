from .config import load_config
from .logger import logger
from pathlib import Path

path = Path(r'C:\proj2\.env')
conf = load_config(path)
