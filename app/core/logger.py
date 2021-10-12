import logging
import sys
from loguru import logger
from gunicorn.app.base import BaseApplication
from gunicorn.glogging import Logger

from app.core.config import settings


loglevel_mapping = {
    50: 'CRITICAL',
    40: 'ERROR',
    30: 'WARNING',
    20: 'INFO',
    10: 'DEBUG',
    0: 'NOTSET',
}

loglevel_reverse_mapping = {
    'CRITICAL': 50,
    'ERROR': 40,
    'WARNING': 30,
    'INFO': 20,
    'DEBUG': 10,
    'NOTSET': 0
}


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = loglevel_mapping[record.levelno]

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level, record.getMessage())


class StubbedGunicornLogger(Logger):
    def setup(self, cfg):
        handler = logging.NullHandler()
        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(handler)
        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(handler)
        self.error_logger.setLevel(settings.log_level)
        self.access_logger.setLevel(settings.log_level)


class StandaloneApplication(BaseApplication):
    """Our Gunicorn application."""

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def config_logger():
    logger.remove()
    logger.add(
        sys.stdout,
        enqueue=True,
        backtrace=True,
        level=settings.log_level.upper(),
        format="<green>{time:YYYY-MM-DD hh:mm:ss.SSS}</green> | <level>{level: <8}</level> | {name}:{line} - <level>{message}</level>",
        colorize=True,
        serialize=settings.json_logs
    )
    logger.add(
        "{path}/{name}_{time}.log".format(path=settings.log_path,
                                          name=settings.log_file, time="{time:YYYY-MM-DD}"),
        retention="5 days",
        enqueue=True,
        backtrace=True,
        level=settings.log_level.upper(),
        format="{time:YYYY-MM-DD hh:mm:ss.SSS} | {level: <8} | {name}:{line} - {message}",
        colorize=True,
        serialize=settings.json_logs
    )

    # intercept everything at the root logger
    logging.basicConfig(handlers=[InterceptHandler(
    )], level=loglevel_reverse_mapping[settings.log_level.upper()], force=True)
    logging.getLogger().setLevel(
        loglevel_reverse_mapping[settings.log_level.upper()])

    # disable handlers for specific uvicorn loggers
    # to redirect their output to the default uvicorn logger
    # works with uvicorn==0.11.6
    uvicorn_loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")
    )
    for uvicorn_logger in uvicorn_loggers:
        uvicorn_logger.handlers = []

    # change handler for default uvicorn logger
    intercept_handler = InterceptHandler()
    logging.getLogger("uvicorn").handlers = [intercept_handler]

    for _log in [*logging.root.manager.loggerDict.keys(),
                 'gunicorn',
                 'gunicorn.error',
                 'gunicorn.access',
                 'fastapi'
                 ]:
        _logger = logging.getLogger(_log)
        _logger.handlers = [InterceptHandler()]
        _logger.level = loglevel_reverse_mapping[settings.log_level.upper()]

    return logger.bind(request_id=None, method=None)
