import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)
stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)