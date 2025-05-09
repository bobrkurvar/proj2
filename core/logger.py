import logging
import sys

logging.basicConfig()
logger = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)