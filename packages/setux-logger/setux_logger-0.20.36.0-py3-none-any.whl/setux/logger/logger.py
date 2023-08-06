from logging import getLogger, FileHandler
from logging.config import dictConfig
from enum import Enum
from contextlib import contextmanager

from pybrary.func import caller

from .config import config

dictConfig(config)

_logger_ = getLogger('setux')


class Verbosity(Enum):
    quiet = 0
    normal = 1
    verbose = 2


class Logger:
    def __init__(self, verbosity=None):
        self.verbosity = verbosity or Verbosity.normal

    @contextmanager
    def quiet(self):
        back = self.verbosity
        self.verbosity = Verbosity.quiet
        try:
            yield
        finally:
            self.verbosity = back

    def debug(self, *a):
        if len(a)>1:
            _logger_.debug(*a)
        else:
            _logger_.debug(f'{caller()} -> {a[0]}')

    def info(self, *a):
        if self.verbosity.value < Verbosity.normal.value:
            self.debug(*a)
        else:
            _logger_.info(*a)

    def error(self, *a):
        _logger_.error(*a)

    def exception(self, *a):
        _logger_.exception(*a)

    def logs(self, level='info'):
        for h in _logger_.handlers:
            if isinstance(h, FileHandler):
                if h.get_name()==level:
                    return h.baseFilename


logger = Logger()

debug = logger.debug
info = logger.info
error = logger.error
exception = logger.exception

