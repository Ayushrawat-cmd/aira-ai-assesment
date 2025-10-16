import logging
import sys
import os
from logging.handlers import RotatingFileHandler

class Logger():
    CONFIG_KEY = 'log'
    LOG_DIRECTORY = 'logs'
    LOG_FILE_SIZE = 1 * 1024 * 1024  # 1MB in bytes
    LOG_FILE_LEVEL = logging.INFO
    LOG_STREAM_LVL = logging.DEBUG
    LOG_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
    LOG_FILE_NAME = "./logs.log"
    LOG_FORMAT = "%(asctime)s.%(msecs)03d %(levelname)5s %(name)s - %(message)s"  # Single % for format fields

    _logger_instance = None  # Single instance of the logger

    @staticmethod
    def get_filename():
        log_filename = Logger.LOG_FILE_NAME
        
        if not os.path.exists(Logger.LOG_DIRECTORY):
            os.makedirs(Logger.LOG_DIRECTORY)

        return os.path.join(Logger.LOG_DIRECTORY, log_filename)

    @staticmethod
    def get_environment():
        return os.environ.get('ENV', 'dev')  # Default to 'dev' if ENV is not set

    @staticmethod
    def get_logger(name):
        # if Logger._logger_instance is not None:
        #     return Logger._logger_instance
        
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt=Logger.LOG_FORMAT,
            datefmt=Logger.LOG_DATE_FORMAT
        )

        # Add a stream handler to print logs to console
        stream_hdlr = logging.StreamHandler(sys.stdout)
        stream_hdlr.setLevel(Logger.LOG_STREAM_LVL)
        stream_hdlr.setFormatter(formatter)
        logger.addHandler(hdlr=stream_hdlr)

        # Add a rotating file handler to save logs to a file and rotate based on file size
        file_hdlr = RotatingFileHandler(
            filename=Logger.get_filename(),
            maxBytes=Logger.LOG_FILE_SIZE,
            backupCount=5  # Number of backup files to keep
        )
        file_hdlr.setLevel(Logger.LOG_FILE_LEVEL if Logger.get_environment() != 'dev' else Logger.LOG_STREAM_LVL)  # Use LOG_STREAM_LVL in dev environment
        file_hdlr.setFormatter(formatter)
        logger.addHandler(hdlr=file_hdlr)
        # Store the logger instance for reuse
        Logger._logger_instance = logger
        return logger
