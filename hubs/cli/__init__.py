import logging

logger = logging.getLogger('hubs.cli')
logger.setLevel(logging.ERROR)
console = logging.StreamHandler()
console.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(console)
