import logging
import os
from dotenv import load_dotenv
from logging import config as logging_config
logger = logging.getLogger()


def init_app():
    global logger
    if not load_dotenv(override=False):
        logger.error('Could not find any .env file. The module will depend on system env only')

    # if application handlers , do nothing , else add just stdout handler
    if not logger.hasHandlers():
        app_logging_config = {
            'version': 1,
            'loggers': {
                '': {  # root logger
                    'level': os.getenv('LOG_LEVEL', 'INFO'),
                    'handlers': ['console'],
                },
            },
            'handlers': {
                'console': {
                    'level': os.getenv('LOG_LEVEL', 'INFO'),
                    'formatter': 'info',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',
                },
            },
            'formatters': {
                'info': {
                    'format': '%(asctime)s-%(module)s-%(lineno)s::%(levelname)s:: %(message)s'
                }
            },
        }

        logging_config.dictConfig(app_logging_config)
    logger.debug('sqlconnection library initiated')


if __name__ == 'sqlconnection':
    init_app()
