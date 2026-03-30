from pathlib import Path

from .config import load_config
from .logger import setup_logging, setup_test_logging

# path = Path(r'C:\proj2\.env')
conf = load_config()
