import logging
from logging.handlers import TimedRotatingFileHandler


# Logging configuration
def configurate_logger(log_file: str, log_to_file: bool, log_to_console: bool, log_level: str):
    # Set level for aiosqlite to WARNING or higher to ignore DEBUG and INFO logs
    logging.getLogger('aiosqlite').setLevel(logging.WARNING)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)s | %(message)s')

    # Create handlers
    log_handlers = []

    if log_to_file:
        file_handler = TimedRotatingFileHandler(log_file, backupCount=100, when="d", interval=1)
        file_handler.setFormatter(formatter)
        log_handlers.append(file_handler)

    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        log_handlers.append(console_handler)

    logging.basicConfig(level=log_level,
                        format='%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)s | %(message)s',
                        # datefmt='%d.%m.%Y %H:%M:%S',
                        handlers=log_handlers)

    logger = logging.getLogger(__name__)
    logger.debug(f"Logger configured with : log_file: {log_file}, log_to_file: {log_file}, "
                 f"log_to_console: {log_to_console}, log_level: {log_level}")
