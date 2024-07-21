import logging
from logging.handlers import TimedRotatingFileHandler


# Logging configuration
def configurate_logger(log_file: str, log_to_file: bool, log_to_condole: bool, log_level: str):
    log_handlers = []
    if log_to_file:
        log_handlers.append(TimedRotatingFileHandler(log_file, backupCount=100, when="d", interval=1))
    if log_to_condole:
        log_handlers.append(logging.StreamHandler())

    logging.basicConfig(level=log_level,
                        format='%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)s | %(message)s',
                        # datefmt='%d.%m.%Y %H:%M:%S',
                        handlers=log_handlers)
