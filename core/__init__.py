from .config import load_config
from pathlib import Path

__all__ = ["conf"]

path = Path(r'C:\proj2\.env')
conf = load_config(path)