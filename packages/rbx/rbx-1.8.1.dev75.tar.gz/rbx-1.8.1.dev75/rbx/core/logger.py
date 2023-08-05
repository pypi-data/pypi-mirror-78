from enum import IntEnum
from functools import partial
import logging
import logging.config
import os
import sys
import traceback

import click
from google.cloud import logging_v2

ENABLE_CLOUD_LOGGING = 'ENABLE_CLOUD_LOGGING'


def init(format='[%(asctime)s] [%(levelname)s] %(message)s'):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': format
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            '': {
                'level': os.getenv('LOG_LEVEL', 'ERROR'),
                'handlers': ['console'],
            },
            'rbx': {
                'level': os.getenv('LOG_LEVEL', 'ERROR'),
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }

    logging.config.dictConfig(LOGGING)
    logging.getLogger('urllib3').propagate = False
    logging.getLogger('google').propagate = False


class Logger:
    """Implements the default logging methods."""
    def __init__(self, format='[%(asctime)s] [%(levelname)s] %(message)s', logger=None):
        if not logger:
            logger = logging

        self.format = format
        self.logger = logger
        self.setup_logging()

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.__class__.__name__)

    def __getattr__(self, name):
        """Delegate the basic logging methods to the logger."""
        if name in ('debug', 'info', 'warning', 'error', 'critical', 'exception'):
            return getattr(self.logger, name)

        raise AttributeError(f'{self.__class__.__name__!r} object has no attribute {name!r}')

    def setup_logging(self):
        init(format=self.format)

    def done(self):
        pass

    def log(self, message):
        self.logger.debug(message)

    def progress(self):
        pass


class ConsoleLogger(Logger):
    """Logs to the console with colours."""

    def info(self, message, *args, **kwargs):
        self.logger.info(click.style(str(message), bold=True), *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self.logger.warning(click.style(str(message), fg='yellow'), *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self.logger.error(click.style(str(message), fg='bright_red'), *args, **kwargs)

    def exception(self, message, *args, **kwargs):
        self.logger.exception(click.style(str(message), fg='bright_red'), *args, **kwargs)

    def critical(self, message, *args, **kwargs):
        self.logger.critical(
            click.style(str(message), fg='bright_white', bg='red'), *args, **kwargs)

    def log(self, message):
        """Print to screen without a new line."""
        click.echo(message, nl=False)

    def progress(self):
        """Print a '.' to screens without a new line."""
        click.echo('.', nl=False)

    def done(self):
        """Print 'done' followed by a new line."""
        click.secho(' done', fg='green')


class CloudLoggingParseError(Exception):
    pass


class CloudLoggingSeverity(IntEnum):
    ALL = 0
    DEBUG = 100
    INFO = 200
    WARNING = 400
    ERROR = 500
    CRITICAL = 600


class CloudLoggingLogger(Logger):
    """Logs to Google Cloud Logging.

    This logger is built to work from within Google App Engine, which by default will print all
    logs from stdout without any severity level. This implementation will set the appropriate
    level, as well as use the 'rbx' logger in the Cloud Logging Console.
    """

    class LogWriter:
        """The LogWriter is the object that calls the Cloud Logging API."""

        def __init__(self):
            self.client = logging_v2.LoggingServiceV2Client()
            self.project = os.environ['GAE_APPLICATION'].split('~')[-1]
            self.resource = {
                'type': 'gae_app',
                'labels': {
                    'project_id': self.project,
                    'module_id': os.environ['GAE_SERVICE'],
                    'version_id': os.environ['GAE_VERSION'],
                }
            }

        def write_log(self, message, severity=CloudLoggingSeverity.ALL, tb=None):
            if tb:
                message = f'{tb}\nMessage: {message}'

            entry = logging_v2.types.LogEntry(text_payload=str(message), severity=severity)
            self.client.write_log_entries(
                [entry],
                log_name=f'projects/{self.project}/logs/rbx',
                resource=self.resource)

    def __init__(self):
        super().__init__()

        if self.cloud_logging_enabled:
            self.logger = self.LogWriter()

    @property
    def cloud_logging_enabled(self):
        return bool(os.getenv(ENABLE_CLOUD_LOGGING, False))

    def __getattr__(self, name):
        """Delegate the basic logging methods to the logger."""
        if name in ('debug', 'info', 'warning', 'error', 'critical', 'exception'):
            if self.cloud_logging_enabled:
                return partial(self.write_log, name)
            else:
                return getattr(self.logger, name)

        raise AttributeError(f'{self.__class__.__name__!r} object has no attribute {name!r}')

    def write_log(self, level, message):
        tb = None
        if level == 'exception':
            tb = ''.join(traceback.format_exception(*sys.exc_info()))
            level = 'critical'

        self.logger.write_log(message, severity=CloudLoggingSeverity[level.upper()], tb=tb)

    def log(self, message):
        if self.cloud_logging_enabled:
            self.write_log('debug', message)
        else:
            super().log(message)
