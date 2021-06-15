import os
import logging

from flask_blog.services import init_logs


INFO_LOG_FILE_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '../log/app/info.log')
ERROR_LOG_FILE_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '../log/app/error.log')


def get_main_logger():
    '''
    If app deployment is based on heroku then 
    LOG_TO_STDOUT should be specified, 
    so returns stdout logger.
    Else returns file logger.
    '''
    main_logger = logging.getLogger(__name__)

    if os.getenv('LOG_TO_STDOUT'):
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.ERROR)
        log_formatter = logging.Formatter(
            "%(asctime)s — %(name)s — %(levelname)s — %(message)s")
        stream_handler.setFormatter(log_formatter)
        main_logger.addHandler(stream_handler)

    else:
        if not os.path.exists(ERROR_LOG_FILE_LOCATION) \
                or not os.path.exists(INFO_LOG_FILE_LOCATION):
            init_logs(ERROR_LOG_FILE_LOCATION, INFO_LOG_FILE_LOCATION)

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

        main_logger.addHandler(info_handler)
        main_logger.addHandler(error_handler)

    return main_logger
