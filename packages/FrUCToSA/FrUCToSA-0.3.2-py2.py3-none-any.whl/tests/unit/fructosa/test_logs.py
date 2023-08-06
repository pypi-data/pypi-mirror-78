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

import unittest
from unittest.mock import patch, MagicMock
from inspect import signature, Parameter

import logging

import fructosa.logs as logs
from fructosa.constants import CANNOT_USE_LOG_HANDLER
from fructosa.error_handling import CannotLog


class BaseLogging:
    def check_number_of_arguments(self, number_of_arguments):
        s = signature(self.test_func)
        parameters = s.parameters
        self.assertEqual(len(parameters), number_of_arguments)

        
class setup_logging_TestCase(BaseLogging, unittest.TestCase):
    def setUp(self):
        self.test_func = logs.setup_logging
    
    def test_has_one_argument(self):
        self.check_number_of_arguments(4)
             
    def test_argument_of_correct_type(self):
        s = signature(self.test_func)
        for parameter in s.parameters.values():
            self.assertEqual(parameter.kind, Parameter.POSITIONAL_OR_KEYWORD)

    def test_the_argument_defaults_to_None(self):
        s = signature(self.test_func)
        for parameter in s.parameters.values():
            self.assertFalse(parameter.default)

    @patch("fructosa.logs._add_handlers")
    @patch("fructosa.logs._create_logger")
    def test_create_logger_called_with_name(
            self, pcreate_logger, padd_handlers):
        logger_name = "stupid logger name"
        self.test_func(logger_name)
        pcreate_logger.assert_called_once_with(logger_name)

    @patch("fructosa.logs._add_handlers")
    @patch("fructosa.logs._create_logger")
    def test_returns_created_logger(self, pcreate_logger, padd_handlers):
        logger_name = "stupid logger name"
        mock_logger = MagicMock()
        pcreate_logger.return_value = mock_logger
        expected = mock_logger
        actual = self.test_func(logger_name)
        self.assertIs(expected, actual)

    @patch("fructosa.logs._add_handlers")
    @patch("fructosa.logs._create_logger")
    def test_add_handlers_called(
            self, pcreate_logger, 
            padd_handlers):
        args = [MagicMock() for _ in range(4)]
        mock_logger = MagicMock()
        pcreate_logger.return_value = mock_logger
        self.test_func(*args)
        padd_handlers.assert_called_once_with(mock_logger, *args[1:])


class create_logger_TestCase(BaseLogging, unittest.TestCase):
    def setUp(self):
        self.test_func = logs._create_logger
        
    def test_has_one_argument(self):
        self.check_number_of_arguments(1)

    @patch("fructosa.logs._get_logger_name")
    @patch("fructosa.logs.getLogger")
    def test_calls_get_logger_name(self, pgetLogger, pget_logger_name):
        create_logger_arg = "name"
        self.test_func(create_logger_arg)
        pget_logger_name.assert_called_once_with(create_logger_arg)

    @patch("fructosa.logs._get_logger_name")
    @patch("fructosa.logs.getLogger")
    def test_calls_getLogger(self, pgetLogger, pget_logger_name):
        create_logger_arg = "name"
        logger_name = MagicMock()
        pget_logger_name.return_value = logger_name
        self.test_func(create_logger_arg)
        pgetLogger.assert_called_once_with(logger_name)

    @patch("fructosa.logs._get_logger_name")
    @patch("fructosa.logs.getLogger")
    def test_sets_logger_level(self, pgetLogger, pget_logger_name):
        from fructosa.constants import LOGGER_LEVEL
        logger = MagicMock()
        pgetLogger.return_value = logger
        self.test_func("fake name")
        logger.setLevel.assert_called_once_with(LOGGER_LEVEL)

    @patch("fructosa.logs._get_logger_name")
    @patch("fructosa.logs.getLogger")
    def test_returns_logger(self, pgetLogger, pget_logger_name):
        mock_logger = MagicMock()
        pgetLogger.return_value = mock_logger
        actual_result = self.test_func("fake name")
        self.assertIs(actual_result, mock_logger)


class get_logger_name_TestCase(BaseLogging, unittest.TestCase):
    def setUp(self):
        self.test_func = logs._get_logger_name
        
    def test_has_one_argument(self):
        self.check_number_of_arguments(1)

    def test_input_proper_argument_returns_the_same(self):
        given = "funny_name"
        result = self.test_func(given)
        self.assertEqual(given, result)

    @patch("fructosa.logs._get_default_logger_name")
    def test_input_None_returns_default(self, pget_name_mock):
        expected = "tests"
        pget_name_mock.return_value = expected
        given = None
        result = self.test_func(given)
        self.assertEqual(expected, result)


class get_default_logger_name_TestCase(BaseLogging, unittest.TestCase):
    def setUp(self):
        self.test_func = logs._get_default_logger_name
        
    def test_has_zero_arguments(self):
        s = signature(self.test_func)
        parameters = s.parameters
        self.assertEqual(len(parameters), 0)

    @patch("fructosa.logs._get_caller_module_name")
    def test_calls_get_caller_module_name(self, pget_caller_name):
        self.test_func()
        pget_caller_name.assert_called_once_with()

    @patch("fructosa.logs._get_caller_module_name")
    def test_returns_what_get_caller_module_name(self, pget_caller_name):
        fake_module_name = MagicMock()
        pget_caller_name.return_value = fake_module_name
        result = self.test_func()
        expected = fake_module_name
        self.assertEqual(result, expected)


class get_caller_module_name_TestCase(BaseLogging, unittest.TestCase):
    def setUp(self):
        self.test_func = logs._get_caller_module_name
        
    def test_has_zero_arguments(self):
        self.check_number_of_arguments(0)

    @patch("fructosa.logs._get_next_module_name_in_stack")
    @patch("fructosa.logs._get_module_name_from_frame_record")
    @patch("fructosa.logs.inspect.stack")
    def test_gets_the_stack_from_inspect(
            self, pstack, pget_module_name_from_frame_record, 
            pget_next_module_name_in_stack):
        self.test_func()
        pstack.assert_called_once_with()
        
    @patch("fructosa.logs._get_next_module_name_in_stack")
    @patch("fructosa.logs._get_module_name_from_frame_record")
    @patch("fructosa.logs.inspect.stack")
    def test_first_frame_in_stack_taken_as_reference(
            self, pstack, pget_module_name_from_frame_record, 
            pget_next_module_name_in_stack):
        test_stack = MagicMock()
        test_stack.__getitem__ = MagicMock()
        pstack.return_value = test_stack
        self.test_func()
        test_stack.__getitem__.assert_called_once_with(0)
        
    @patch("fructosa.logs._get_next_module_name_in_stack")
    @patch("fructosa.logs._get_module_name_from_frame_record")
    @patch("fructosa.logs.inspect.stack")
    def test_get_module_name_from_frame_record_called_with_first_frame_in_stack(
            self, pstack, pget_module_name_from_frame_record, 
            pget_next_module_name_in_stack):
        test_stack = MagicMock()
        target_frame_record = MagicMock()
        def getitem(index):
            if index == 0:
                return target_frame_record
            else:
                return MagicMock()
        test_stack.__getitem__ = MagicMock(side_effect=getitem)
        pstack.return_value = test_stack
        self.test_func()
        pget_module_name_from_frame_record.assert_called_with(
            target_frame_record
        )

    @patch("fructosa.logs._get_next_module_name_in_stack")
    @patch("fructosa.logs._get_module_name_from_frame_record")
    @patch("fructosa.logs.inspect.stack")
    def test_get_next_module_name_in_stack_called(
            self, pstack, pget_module_name_from_frame_record,
            pget_next_module_name_in_stack):
        mock_stack = MagicMock()
        pstack.return_value = mock_stack
        mock_frame_record = MagicMock()
        pget_module_name_from_frame_record.return_value = mock_frame_record
        self.test_func()
        pget_next_module_name_in_stack.assert_called_once_with(
            mock_stack, mock_frame_record
        )

    @patch("fructosa.logs._get_next_module_name_in_stack")
    @patch("fructosa.logs._get_module_name_from_frame_record")
    @patch("fructosa.logs.inspect.stack")
    def test_result_of_get_next_module_name_in_stack_returned(
            self, pstack, pget_module_name_from_frame_record,
            pget_next_module_name_in_stack):
        mock_result = MagicMock()
        pget_next_module_name_in_stack.return_value = mock_result
        result = self.test_func()
        self.assertEqual(result, mock_result)
    

class get_next_module_name_in_stack_TestCase(BaseLogging, unittest.TestCase):
    def setUp(self):
        self.test_func = logs._get_next_module_name_in_stack
        self.prepare_test_stacks()

    def prepare_test_stacks(self):
        frames = [MagicMock() for _ in range(4)]
        for iframe, frame in enumerate(frames):
            frame.module_name = "mod{0}".format(iframe)
        stack0 = frames
        stack1 = [
            frames[0], frames[0], frames[0], frames[1], frames[2], frames[3]
        ]
        stack2 = [frames[0], frames[0], frames[0]]
        self.interesting_stacks = [stack0, stack1, stack2]
        self.module_names_of_interesting_stacks = ["mod1", "mod1", "mod0"]

    def test_has_two_arguments(self):
        self.check_number_of_arguments(2)

    @patch("fructosa.logs._get_module_name_from_frame_record")
    @patch("fructosa.logs.inspect.stack")
    def test_returns_next_to_given_frame_modules_name(
            self, pstack, pget_module_name_from_frame_record):
        def fake_module_getter(thing):
            return thing.module_name
        pget_module_name_from_frame_record.side_effect = fake_module_getter
        stacks = self.interesting_stacks
        expected_names = self.module_names_of_interesting_stacks
        for stack, expected_name in zip(stacks, expected_names):
            pstack.return_value = stack
            ref_module_name = stack[0].module_name
            module_name = self.test_func(stack, ref_module_name)
            self.assertEqual(module_name, expected_name)


class get_module_name_from_frame_record_TestCase(
        BaseLogging, unittest.TestCase):
    def setUp(self):
        self.test_func = logs._get_module_name_from_frame_record

    def test_has_one_argument(self):
        self.check_number_of_arguments(1)

    @patch("fructosa.logs.inspect.getmodule")
    def test_returns_next_to_given_frame_modules_name(
            self, pgetmodule):
        mock_frame = MagicMock()
        mock_frame_record = MagicMock()
        def getitem(index):
            if index == 0:
                return mock_frame
            else:
                return None
        mock_frame_record.__getitem__ = MagicMock(side_effect=getitem)
        mock_name = MagicMock()
        mock_module = MagicMock()
        mock_module.__name__ = mock_name
        pgetmodule.return_value = mock_module
        result = self.test_func(mock_frame_record)
        self.assertEqual(result, mock_name)

        
@patch("fructosa.logs.Formatter")
@patch("fructosa.logs._add_streamhandler")
@patch("fructosa.logs._add_rotatingfilehandler")
@patch("fructosa.logs._add_sysloghandler")
class add_handlers_TestCase(BaseLogging, unittest.TestCase):
    def setUp(self):
        self.test_func = logs._add_handlers
        self.mlogger = MagicMock()

    def test_has_one_argument(self, *patches):
        self.check_number_of_arguments(4)

    def test_Formatter_instance_properly_created(
            self, p_add_sysloghandler, p_add_rotatingfilehandler,
            p_add_streamhandler, pFormatter):
        from fructosa.constants import FILE_LOGGING_FORMAT
        self.test_func(self.mlogger, {}, {}, {})
        pFormatter.assert_called_once_with(FILE_LOGGING_FORMAT)

    def test_add_sysloghandler_called(
            self, p_add_sysloghandler, p_add_rotatingfilehandler,
            p_add_streamhandler, pFormatter):
        formatter_instance = MagicMock()
        pFormatter.return_value = formatter_instance
        conf = {}
        self.test_func(self.mlogger, {}, conf, {})
        p_add_sysloghandler.assert_called_once_with(self.mlogger, formatter_instance, conf)

    def test_add_rotatingfilehandler_called(
            self, p_add_sysloghandler, p_add_rotatingfilehandler,
            p_add_streamhandler, pFormatter):
        formatter_instance = MagicMock()
        pFormatter.return_value = formatter_instance
        conf = {}
        self.test_func(self.mlogger, {}, {}, conf)
        p_add_rotatingfilehandler.assert_called_once_with(
            self.mlogger, formatter_instance, conf
        )

    def test_add_streamhandler_called(
            self, p_add_sysloghandler, p_add_rotatingfilehandler,
            p_add_streamhandler, pFormatter):
        pFormatter.return_value = MagicMock()
        conf = {}
        self.test_func(self.mlogger, conf, {}, {})
        p_add_streamhandler.assert_called_once_with(self.mlogger, conf)

    def test_raises_CannotLog_if_rotatingfilehandler_raises_PermissionError(
            self, p_add_sysloghandler, p_add_rotatingfilehandler,
            p_add_streamhandler, pFormatter):
        original_msg = "xxxhhh"
        msg = "{}\n... {}".format(CANNOT_USE_LOG_HANDLER, original_msg)
        p_add_rotatingfilehandler.side_effect = PermissionError(original_msg)
        with self.assertRaises(CannotLog) as e:
            self.test_func(self.mlogger, {}, {}, {})
        self.assertEqual(str(e.exception), msg)


@patch("fructosa.logs.StreamHandler")
class add_streamhandler_TestCase(unittest.TestCase):
    def setUp(self):
        self.test_func = logs._add_streamhandler

    def test_creates_StreamHandler_instance(self, pStramHandler):
        self.test_func(MagicMock(), {})
        pStramHandler.assert_called_once_with()
        
    def test_sets_default_logging_level(self, pStramHandler):
        handler = MagicMock()
        pStramHandler.return_value = handler
        self.test_func(MagicMock(), {})
        handler.setLevel.assert_called_once_with(logging.ERROR)

    def test_sets_non_default_logging_level(self, pStramHandler):
        handler = MagicMock()
        pStramHandler.return_value = handler
        conf = {"level": logging.INFO}
        self.test_func(MagicMock(), conf)
        handler.setLevel.assert_called_once_with(logging.INFO)

    def test_handler_added_to_logger(self, pStramHandler):
        logger = MagicMock()
        self.test_func(logger, {})
        logger.addHandler.assert_called_once_with(pStramHandler.return_value)

        
class add_sysloghandler_TestCase(BaseLogging, unittest.TestCase):
    def setUp(self):
        self.test_func = logs._add_sysloghandler

    @patch("fructosa.logs.SysLogHandler")
    def test_SysLogHandler_instance_properly_created(self, pSysLogHandler):
        self.test_func(MagicMock(), MagicMock(), {})
        pSysLogHandler.assert_called_once_with("/dev/log")

    @patch("fructosa.logs.SysLogHandler")
    def test_setting_formatter_for_SysLogHandler(self, pSysLogHandler):
        set_formatter = MagicMock()
        sysloghandler_instance = MagicMock()
        formatter_instance = MagicMock()
        sysloghandler_instance.setFormatter = set_formatter
        pSysLogHandler.return_value = sysloghandler_instance
        self.test_func(MagicMock(), formatter_instance, {})
        set_formatter.assert_called_once_with(formatter_instance)

    @patch("fructosa.logs.SysLogHandler")
    def test_sets_default_logging_level(self, pSysLogHandler):
        set_level = MagicMock()
        sysloghandler_instance = MagicMock()
        sysloghandler_instance.setLevel = set_level
        pSysLogHandler.return_value = sysloghandler_instance
        self.test_func(MagicMock(), MagicMock(), {})
        set_level.assert_called_once_with(logging.WARNING)

    @patch("fructosa.logs.SysLogHandler")
    def test_sets_non_default_logging_level(self, pSysLogHandler):
        set_level = MagicMock()
        sysloghandler_instance = MagicMock()
        sysloghandler_instance.setLevel = set_level
        conf = {"level": logging.INFO}
        pSysLogHandler.return_value = sysloghandler_instance
        self.test_func(MagicMock(), MagicMock(), conf)
        set_level.assert_called_once_with(logging.INFO)

    @patch("fructosa.logs.SysLogHandler")
    def test_SysLogHandler_added_to_logger(self, pSysLogHandler):
        logger = MagicMock()
        add_handler = MagicMock()
        syslog_handler = MagicMock()
        pSysLogHandler.return_value = syslog_handler
        logger.addHandler = add_handler
        self.test_func(logger, MagicMock(), {})
        add_handler.assert_called_once_with(syslog_handler)

        
class add_rotatingfilehandler_TestCase(BaseLogging, unittest.TestCase):
    def setUp(self):
        self.test_func = logs._add_rotatingfilehandler

    @patch("fructosa.logs.RotatingFileHandler")
    def test_instance_with_correct_keys_properly_created(
            self, pRotatingFileHandler):
        conf = {
            "filename": "/dev/null",
            "maxBytes": 234,
            "backupCount": 9,
        }
        self.test_func(MagicMock(), MagicMock(), conf)
        pRotatingFileHandler.assert_called_once_with(
            filename="/dev/null", maxBytes=234, backupCount=9
        )

    @patch("fructosa.logs.RotatingFileHandler")
    def test_instance_with_some_invalid_keys_properly_created(
            self, pRotatingFileHandler):
        conf = {
            "filename": "/dev/null",
            "maxBytes": 234,
            "backu": 9,
        }
        self.test_func(MagicMock(), MagicMock(), conf)
        pRotatingFileHandler.assert_called_once_with(
            filename="/dev/null", maxBytes=234, 
        )

    @patch("fructosa.logs.RotatingFileHandler")
    def test_sets_logging_level_if_given(
            self, pRotatingFileHandler):
        set_level = MagicMock()
        loghandler_instance = MagicMock()
        loghandler_instance.setLevel = set_level
        pRotatingFileHandler.return_value = loghandler_instance
        self.test_func(MagicMock(), MagicMock(), {"level": 12})
        set_level.assert_called_once_with(12)

    @patch("fructosa.logs.RotatingFileHandler")
    def test_set_level_not_called_if_level_not_given(
            self, pRotatingFileHandler):
        set_level = MagicMock()
        loghandler_instance = MagicMock()
        loghandler_instance.setLevel = set_level
        pRotatingFileHandler.return_value = loghandler_instance
        self.test_func(MagicMock(), MagicMock(), {})
        set_level.assert_not_called()

    @patch("fructosa.logs.RotatingFileHandler")
    def test_setting_formatter_for_RotatingFileHandler(
            self, pRotatingFileHandler):
        set_formatter = MagicMock()
        loghandler_instance = MagicMock()
        formatter_instance = MagicMock()
        loghandler_instance.setFormatter = set_formatter
        pRotatingFileHandler.return_value = loghandler_instance
        self.test_func(MagicMock(), formatter_instance, {})
        set_formatter.assert_called_once_with(formatter_instance)

    @patch("fructosa.logs.RotatingFileHandler")
    def test_RotatingFileHandler_added_to_logger(self, pRotatingFileHandler):
        logger = MagicMock()
        add_handler = MagicMock()
        log_handler = MagicMock()
        pRotatingFileHandler.return_value = log_handler
        logger.addHandler = add_handler
        self.test_func(logger, MagicMock(), {})
        add_handler.assert_called_once_with(log_handler)


if __name__ == "__main__":
    unittest.main()
