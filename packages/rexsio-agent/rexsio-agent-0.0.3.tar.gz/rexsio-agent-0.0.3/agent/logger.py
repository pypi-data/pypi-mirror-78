import logging

from twisted.python import log

LOGGER_ROOT = 'agent'


def setup_logger():
    observer = log.PythonLoggingObserver(LOGGER_ROOT)
    observer.start()

    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(LOGGER_ROOT)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger


def get_logger(name):
    return logging.getLogger('.'.join([LOGGER_ROOT, name]))
