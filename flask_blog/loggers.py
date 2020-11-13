import os
import logging


INFO_LOG_FILE_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '../log/info.log')
ERROR_LOG_FILE_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '../log/error.log')


def get_main_logger():
    '''Return file logger for info and errors'''
    log_formatter = logging.Formatter(
        "%(asctime)s — %(name)s — %(levelname)s — %(message)s")
    error_formatter = logging.Formatter(
        "%(asctime)s — %(name)s — %(message)s")

    info_handler = logging.FileHandler(INFO_LOG_FILE_LOCATION)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(log_formatter)

    error_handler = logging.FileHandler(ERROR_LOG_FILE_LOCATION)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(error_formatter)

    main_logger = logging.getLogger(__name__)
    main_logger.addHandler(info_handler)
    main_logger.addHandler(error_handler)

    return main_logger
