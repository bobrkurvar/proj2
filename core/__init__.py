from .config import load_config

conf = load_config('.env')

__all__ = ['conf']