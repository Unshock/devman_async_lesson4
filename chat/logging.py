import enum
import logging

from chat.settings import LOG_LEVEL, LOG_FILE


LOG_LEVEL_MAP = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}


class LoggingInstance(enum.Enum):
    Reader = 'reader'
    Sender = 'sender'
    System = 'system'


def setup_logger(logging_instance: LoggingInstance = LoggingInstance.System):

    log_instance = logging_instance.value if logging_instance else ''
    instance_adding = f':{log_instance}:'

    logger_name = (
        'chat_logger' + ('_' + log_instance)
        if logging_instance
        else ''
    )
    logger = logging.getLogger(logger_name)

    if not logger.handlers:
        log_level = LOG_LEVEL_MAP.get(LOG_LEVEL.lower(), logging.INFO)

        log_format = f'%(asctime)s:%(levelname)s{instance_adding}%(message)s'
        formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(log_level)

        file_handler = logging.FileHandler(filename=LOG_FILE)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        logger.propagate = False
    return logger


logger = setup_logger()
sender_logger = setup_logger(LoggingInstance.Sender)
reader_logger = setup_logger(LoggingInstance.Reader)
