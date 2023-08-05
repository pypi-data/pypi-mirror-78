import os

from .general_utils import generate_guid, parse_headers, log_and_raise_error
from .metrics import MetricsPusher, MetricsManager
from .logging_utils import init_logger, init_error_counter_loggers

init_logger(__name__)

if 'DO_ERROR_COUNTING' in os.environ:
    for logger in os.environ['LOGGERS_TO_WATCH'].split(','):
        init_error_counter_loggers(logger)
