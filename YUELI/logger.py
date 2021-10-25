# coding=utf8

import os
import sys
import time
import socket
import random
import datetime
import logging
import logging.config
import ujson as json

from collections import OrderedDict

def _datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    return x

def produce_settings():
    return dict(
        version=1,
        disable_existing_loggers=False,
        loggers={
            "access.logger": {
                "level": "INFO",
                "handlers": ["access_console"],
                "propagate": False,
            },
            "info.logger": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
            "error.logger": {
                "level": "ERROR",
                "handlers": ["error_console"],
                "propagate": False,
            },
            "debug.logger": {
                "level": "DEBUG",
                "handlers": ["console"],
                "propagate": False,
            },
        },
        handlers={
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": sys.stdout,
            },
            "error_console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": sys.stderr,
            },
            "access_console": {
                "class": "logging.StreamHandler",
                "formatter": "access",
                "stream": sys.stdout,
            },
            "file": {
                "class": "logging.NullHandler",
            },
        },
        formatters={
            "access": {
                "class": "YUELI.logger.JSONReqFormatter",
            },
            "generic": {
                "class": "YUELI.logger.JSONFormatter",
            },
        },
    )


class JSONFormatter(logging.Formatter):

    def __init__(self, *a, **kw):
        super(JSONFormatter, self).__init__(*a, **kw)
        self._pid = os.getpid()
        self._host = socket.getfqdn(socket.gethostname())

    def format(self, record, serialize=True):
        try:
            msg = record.msg % record.args
        except TypeError:
            msg = record.msg

        message = OrderedDict((
            ('log_timestamp', record.created),
            ('log_time', datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')),
            ('log_host', self._host),
            ('log_module', record.module),
            ('log_level', record.levelname),
            ('log_worker', self._pid)
        ))
        if isinstance(msg, dict):
            message.update(msg)
        else:
            message.update({'message': msg})

        return json.dumps(message,ensure_ascii=False)


class JSONReqFormatter(JSONFormatter):

    def format(self, record, serialize=True):
        # Create message dict
        try:
            host = record.request.host
        except:  # noqa: E722
            # Got a few errors with curl :/
            host = None

        # Extract real ip if in AWS (or compatible)
        ip = record.request.headers.get('X-Forwarded-For', record.request.ip)
        port = record.request.headers.get('X-Forwarded-Port', record.request.port)

        message = OrderedDict((
            ('log_timestamp', record.created),
            ('log_time', datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')),
            ('log_host', socket.getfqdn(socket.gethostname())),
            ('log_level', record.levelname),
            ('log_method', record.request.method),
            ('log_type', 'access'),
            ('log_path', record.request.path),
            ('log_remote', '{0}:{1}'.format(ip, port)),
            ('log_user_agent', record.request.headers.get('user-agent')),
            ('log_host', host),
            ('log_response_time', round(record.time, 2)),
            ('log_req_id', record.req_id),
            ('log_worker', self._pid)
        ))

        if record.response is not None:  # not Websocket
            message['status_code'] = record.response.status
            if hasattr(record.response, 'body'):
                message['length'] = len(record.response.body)
            else:
                message['length'] = -1

            message['type'] = 'access'
        else:
            message['type'] = 'ws_access'

        # Can't remember why I added this
        if 'error_message' in record.request:
            try:
                message['request_info']['error_message'] = record.request['error_message']
            except KeyError:
                message['request_info'] = {'error_message': record.request['error_message']}

        return json.dumps(message,ensure_ascii=False)


class BaseLogger(object):

    class LoggingLevelError(Exception):
        pass

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    ERROR = logging.ERROR

    def __init__(self, service_name, debug=False, log_path=None):
        self.service_name = service_name
        self._debug = debug
        _logging_config_defaults = produce_settings()
        if log_path:
            # replace null stream handler with filehandler
            for k, v in _logging_config_defaults['loggers'].items():
                v['handlers'] = ['file']
                _logging_config_defaults['loggers'][k] = v

            _logging_config_defaults['handlers']['file'] = {
                            "class": "logging.handlers.TimedRotatingFileHandler",
                            "formatter": "generic",
                            'when': 'midnight',
                            'backupCount': 10,
                            'filename': log_path,
                        }

        logging.config.dictConfig(_logging_config_defaults)

        self._debug_logger = logging.getLogger('debug.logger')
        self._info_logger = logging.getLogger('info.logger')
        self._error_logger = logging.getLogger('error.logger')


    def access(self, context):
        raise NotImplementedError

    def debug(self, context, sampling=100):
        self._do_log(self.DEBUG,
                     self._debug_logger,
                     context,
                     sampling=sampling)

    def info(self, context, sampling=100):
        self._do_log(self.INFO,
                     self._info_logger,
                     context,
                     sampling=sampling)

    def error(self, context, sampling=100):
        self._do_log(self.ERROR,
                     self._error_logger,
                     context,
                     sampling=sampling)

    def _do_log(self, level, logger, context, sampling=100):
        if sampling > 100:
            sampling = 100

        if sampling < 100 and not random.randrange(100) in range(sampling):
            return

        if not isinstance(context, dict):
            raise TypeError('Log body requires dict')

        context.update({'service_name': self.service_name})
        logger.log(level, context)


class YULI_LOG(BaseLogger):

    def __init__(self, service_name, *a, **kw):
        super(YULI_LOG, self).__init__(service_name, *a, **kw)



