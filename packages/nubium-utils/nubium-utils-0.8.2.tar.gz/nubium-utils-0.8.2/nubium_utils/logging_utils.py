import sys
import logging
import os
import threading


def _init_handler():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(_get_loglevel())

    handler.setFormatter(
        logging.Formatter(
            "{process} - {filename:15} - {asctime} - {name} - {levelname} - {message}",
            style="{"
        )
    )
    return handler


def _get_loglevel():
    return os.environ.get('LOGLEVEL', 'CRITICAL')


def init_logger(name='nubium-utils'):
    logger = logging.getLogger(name)
    logger.setLevel(_get_loglevel())
    logger.addHandler(_init_handler())
    logger.propagate = False
    return logger


def init_error_counter_loggers(name):
    logging.setLoggerClass(LogCounter)
    logger = logging.getLogger(name)
    return logger


class LogCounter(logging.Logger):
    """ Overrides logging.Logger to increment a counter when an error or a warning with any of the
    specified strings are logged. """
    def __init__(self, name, level=logging.NOTSET):
        self._count = 0
        self._countLock = threading.Lock()

        return super(LogCounter, self).__init__(name, level)

    @property
    def error_count(self):
        return self._count

    def kill_if_necessary(self):
        if self.name in os.environ['LOGGERS_TO_WATCH'].split(','):
            self._countLock.acquire()
            if self._count >= 1:
                os._exit(1)
            self._countLock.release()

    def warning(self, msg, *args, **kwargs):
        if any(error_string in msg for error_string in os.environ['ERROR_STRINGS'].split(',')):
            self._countLock.acquire()
            self._count += 1
            self._countLock.release()
            self.kill_if_necessary()

        return super(LogCounter, self).warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if any(error_string in msg for error_string in os.environ['ERROR_STRINGS'].split(',')):
            self._countLock.acquire()
            self._count += 1
            self._countLock.release()
            self.kill_if_necessary()

        return super(LogCounter, self).error(msg, *args, **kwargs)
