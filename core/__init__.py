from .config import load_config
from pathlib import Path
from .logger import logger

__all__ = ["conf", "logger"]

path = Path(r'C:\proj2\.env')
conf = load_config(path)
