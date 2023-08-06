#!/bin/env python

#######################################################################
#
# Copyright (C) 2020 David Palao
#
# This file is part of FrUCToSA.
#
#  FrUCToSA is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  FrUCToSA is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with FrUCToSA.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################

import logging
from logging import getLogger, Formatter, StreamHandler
import inspect
from logging.handlers import SysLogHandler, RotatingFileHandler

from fructosa.error_handling import CannotLog
from fructosa.constants import (
    LOGGER_LEVEL, FILE_LOGGING_FORMAT, CANNOT_USE_LOG_HANDLER, 
)


def setup_logging(logger_name=None, stream_conf={}, syslog_conf={}, rotatingfile_conf={}):
    """If no logger_name is provided, then the name is decided based on 
    the module that calls this function.
    """
    logger = _create_logger(logger_name)
    _add_handlers(logger, stream_conf, syslog_conf, rotatingfile_conf)
    return logger

def _add_handlers(logger, stream_conf, syslog_conf, rotatingfile_conf):
    file_formater = Formatter(FILE_LOGGING_FORMAT)
    _add_sysloghandler(logger, file_formater, syslog_conf)
    try:
        _add_rotatingfilehandler(logger, file_formater, rotatingfile_conf)
    except PermissionError as e:
        new_msg = "{}\n... {}".format(CANNOT_USE_LOG_HANDLER, str(e))
        raise CannotLog(new_msg)
    _add_streamhandler(logger, stream_conf)
    
def _add_streamhandler(logger, conf):
    stream = StreamHandler()
    level = conf.get("level", logging.ERROR)
    stream.setLevel(level)
    logger.addHandler(stream)

def _add_sysloghandler(logger, formatter, conf):
    syslog_handler = SysLogHandler("/dev/log")
    level = conf.get("level", logging.WARNING)
    syslog_handler.setLevel(level)
    syslog_handler.setFormatter(formatter)
    logger.addHandler(syslog_handler)

def _add_rotatingfilehandler(logger, formatter, conf):
    valid_keys = ["filename", "backupCount", "maxBytes"]
    rotating_handler = RotatingFileHandler(
        **{_:conf[_] for _ in conf if _ in valid_keys}
    )
    try:
        level = conf["level"]
    except KeyError:
        pass
    else:
        rotating_handler.setLevel(level)
    rotating_handler.setFormatter(formatter)
    logger.addHandler(rotating_handler)

def _create_logger(proto_logger_name):
    logger_name = _get_logger_name(proto_logger_name)
    logger = getLogger(logger_name)
    logger.setLevel(LOGGER_LEVEL)
    return logger
    
def _get_logger_name(proto_logger_name):
    logger_name = proto_logger_name
    if logger_name is None:
        logger_name = _get_default_logger_name()
    return logger_name

def _get_default_logger_name():
    """It looks like an artificial level of abstraction, but I think it is
    not: what if I want to determine the default logger name in a different
    way?"""
    name = _get_caller_module_name()
    return name

def _get_caller_module_name():
    stack = inspect.stack()
    first_frame_record = stack[0]
    first_module_name = _get_module_name_from_frame_record(first_frame_record)
    module_name = _get_next_module_name_in_stack(stack, first_module_name)
    return module_name

def _get_next_module_name_in_stack(stack, reference_module_name):
    for current_frame_record in stack:
        current_module_name = _get_module_name_from_frame_record(
            current_frame_record
        )
        if current_module_name != reference_module_name:
            module_name = current_module_name
            break
    else:
        module_name = reference_module_name
    return module_name
    
def _get_module_name_from_frame_record(frame_record):
    frame = frame_record[0]
    mod = inspect.getmodule(frame)
    module_name = mod.__name__
    return module_name

