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
from unittest.mock import patch, MagicMock, call, mock_open
from inspect import signature, Parameter

import fructosa.fructosad
from fructosa.constants import (
    PROTO_NO_PERMISSION_PIDFILE, START_STOP_ERROR, PIDFILE_NOT_FOUND,
    PIDFILE_ACTION_CREATED, PIDFILE_ACTION_ACCESSED, INVALID_PID,
    PROCESS_DOES_NOT_EXIST, OWN_LOG_FILE_KEY, ACTION_STR, PIDFILE_STR,
    GRAPHITE_HOST_KEY, GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY,
    PROTO_MSG_TO_GRAPHITE, TO_GRAPHITE_CONNECTING_MSG,
    TO_GRAPHITE_CONNECTED_MSG, TO_GRAPHITE_RETRY_MSG,
    OWN_LOG_SECTION, 
)
from fructosa.lmessage import UnsuitableLMessage, WrongPickleMessage

from .aio_tools import asyncio_run, AsyncioMock


class InventedException(Exception):
    ...


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.main = fructosa.fructosad.main
        
    def test_is_executable(self):
        self.assertIn("__call__", dir(self.main))

    def test_takes_no_arguments(self):
        s = signature(self.main)
        parameters = s.parameters
        self.assertEqual(len(parameters), 0)

    @patch("fructosa.fructosad.generic_main")
    @patch("fructosa.fructosad.FructosaD")
    @patch("fructosa.fructosad.FructosaDConf")
    def test_calls_generic_main(self, pfructosadconf, pfructosad, pgeneric_main):
        self.main()
        pgeneric_main.assert_called_once_with(pfructosadconf, pfructosad)

        
class FructosaDTestCase(unittest.TestCase):
    def setUp(self):
        self.test_class = fructosa.fructosad.FructosaD
        self.mocked_conf = MagicMock()
        setattr(self.mocked_conf, ACTION_STR, "")
        setattr(self.mocked_conf, PIDFILE_STR, "")
        self.simple_logging = {OWN_LOG_FILE_KEY: "/dev/null"}
        setattr(self.mocked_conf, OWN_LOG_SECTION, self.simple_logging)
        #with patch("fructosa.fructosad.setup_logging") as psetup_logging:
            #self.psetup_logging = psetup_logging
        self.simple_instance = self.test_class(self.mocked_conf)
        
    def test_instance_has_conf_attribute(self):
        self.assertEqual(self.simple_instance._conf, self.mocked_conf)
        
    def test_instance_has_expected_attributes(self):
        from fructosa.fructosad import ACTION_STR, PIDFILE_STR
        action_mock = MagicMock()
        pidfile_mock = MagicMock()
        def getitem(key):
            if key == ACTION_STR:
                return action_mock
            elif key == PIDFILE_STR:
                return pidfile_mock
            else:
                raise KeyError
        conf = MagicMock()
        conf.__getitem__.side_effect = getitem
        with patch("fructosa.fructosad.setup_logging") as psetup_logging:
            instance = self.test_class(conf)
        self.assertEqual(instance.action, conf[ACTION_STR])
        self.assertEqual(instance.pidfile, conf[PIDFILE_STR])
        self.assertEqual(instance.logger, psetup_logging.return_value)

    def test_init_calls_create_queues(self):
        with patch("fructosa.fructosad.FructosaD._create_queues") as pcreate:
            instance = self.test_class(self.mocked_conf)
        pcreate.assert_called_once_with()

    def test_instance_defines_some_strings(self):
        """This test must be implemented for the subclasses. The rest is not necessary, for
        now."""
        from fructosa.fructosad import (
            FRUCTOSAD_STARTING_MESSAGE, FRUCTOSAD_STOP_MESSAGE, FRUCTOSAD_CANT_STOP_MESSAGE
        )
        inst = self.simple_instance
        self.assertEqual(inst._starting_message, FRUCTOSAD_STARTING_MESSAGE)
        self.assertEqual(inst._stopped_message, FRUCTOSAD_STOP_MESSAGE)
        self.assertEqual(inst._cant_stop_message, FRUCTOSAD_CANT_STOP_MESSAGE)
        
    def test_instance_setups_logging(self):
        with patch("fructosa.fructosad.setup_logging") as psetup_logging:
            instance = self.test_class(self.mocked_conf)
        psetup_logging.assert_called_once_with(
            logger_name=self.test_class.__name__,
            rotatingfile_conf=self.mocked_conf.logging
        )

    @patch("fructosa.fructosad.setup_logging")
    @patch("fructosa.fructosad.asyncio.get_event_loop")
    def test_init_creates_event_loop(self, pget_event_loop, psetup_logging):
        event_loop = MagicMock()
        pget_event_loop.return_value = event_loop
        conf = MagicMock()
        instance = self.test_class(conf)
        pget_event_loop.assert_called_once_with()
        self.assertEqual(instance._event_loop, event_loop)

    def test_call_uses_getattr_to_select_action(self):
        action_mock = MagicMock()
        instance = self.simple_instance
        instance.action = action_mock
        pgetattr_ret = MagicMock()
        with patch("fructosa.fructosad.getattr") as pgetattr:
            pgetattr.return_value = pgetattr_ret
            instance()
        pgetattr.assert_called_once_with(instance, action_mock)
        pgetattr_ret.assert_called_once_with()

    def test_logger_sends_message_to_logger(self):
        instance = self.test_class(self.mocked_conf)
        msg = "my dummy message"
        with self.assertLogs(fructosa.fructosad.FructosaD.__name__) as log:
            instance.logger.info(msg)
        
    @patch("fructosa.fructosad.FructosaD.run")
    @patch("fructosa.fructosad.daemonize")
    def test_start_call_sequence(self, pdaemonize, prun):
        pidfile_mock = MagicMock()
        logger = MagicMock()
        logger.warning = MagicMock()
        self.simple_instance.pidfile = pidfile_mock
        self.simple_instance.logger = logger
        manager = MagicMock()
        manager.attach_mock(pdaemonize, "daemonize")
        manager.attach_mock(logger.warning, "warning")
        manager.attach_mock(prun, "run")
        self.simple_instance.start()
        msg = self.simple_instance._starting_message
        expected_calls = [
            call.daemonize(pidfile_mock), call.warning(msg), call.run()
        ]
        manager.assert_has_calls(expected_calls)

    @patch("fructosa.fructosad.FructosaD.run")
    @patch("fructosa.fructosad.daemonize")
    def test_start_behaviour_if_daemonize_raises_RuntimeError(
            self, pdaemonize, prun):
        from fructosa.fructosad import START_STOP_ERROR
        import sys
        logger_name = self.simple_instance.__class__.__name__
        from fructosa.logs import setup_logging
        logger = setup_logging(
            logger_name=logger_name, rotatingfile_conf=self.simple_logging
        )
        self.simple_instance.logger = logger
        pidfile_mock = MagicMock()
        self.simple_instance.pidfile = pidfile_mock
        msg = "my funny error"
        log_level = "ERROR"
        error = RuntimeError(msg)
        pdaemonize.side_effect = error
        expected_log_error = "{}:{}:{}".format(
            log_level, logger_name, msg
        )
        warn_msgs = ("wanna", "be", "porquerizo")
        expected_log_warnings = [
            "{}:{}:{}".format("WARNING", logger_name, msg) for msg in warn_msgs
        ]
        error.to_warning = warn_msgs
        with self.assertRaises(SystemExit) as e:
            with self.assertLogs(fructosa.fructosad.FructosaD.__name__) as log_msg:
                self.simple_instance.start()
        self.assertEqual(e.exception.code, START_STOP_ERROR)
        self.assertIn(expected_log_error, log_msg.output)
        for warn in expected_log_warnings:
            self.assertIn(warn, log_msg.output)
        prun.assert_not_called()

    @patch("fructosa.fructosad.FructosaD.run")
    @patch("fructosa.fructosad.daemonize")
    def test_start_behaviour_if_daemonize_raises_PermissionError(self, pdaemonize, prun):
        exception_msg = "another funny error"
        error = PermissionError(exception_msg)
        error.to_error = PROTO_NO_PERMISSION_PIDFILE.format(
            pidfile=self.simple_instance.pidfile, action=PIDFILE_ACTION_CREATED)
        pdaemonize.side_effect = error
        logger_name = self.simple_instance.__class__.__name__
        from fructosa.logs import setup_logging
        logger = setup_logging(
            logger_name=logger_name, rotatingfile_conf=self.simple_logging
        )
        self.simple_instance.logger = logger
        expected_log_critical = "{}:{}:{}: {}".format(
            "WARNING", logger_name, "Exception message", exception_msg
        )
        expected_log_error = "{}:{}:{}".format(
            "ERROR", logger_name, error.to_error
        )
        with self.assertRaises(SystemExit) as e:
            with self.assertLogs(fructosa.fructosad.FructosaD.__name__) as log_msg:
                self.simple_instance.start()
        self.assertEqual(e.exception.code, START_STOP_ERROR)
        prun.assert_not_called()
        self.assertIn(expected_log_critical, log_msg.output)
        self.assertIn(expected_log_error, log_msg.output)

    @patch("fructosa.fructosad.os.kill")
    def test_stop_kills_right_process_if_pidfile_can_be_opened(self, pkill):
        import signal
        mpid = "9292929292929"
        with patch("fructosa.fructosad.open", mock_open(read_data=mpid)) as mopen:
            self.simple_instance.stop()
            pkill.assert_called_once_with(int(mpid), signal.SIGTERM)

    @patch("fructosa.fructosad.os.kill")
    def test_stop_logs_message_if_process_stops(self, pkill):
        with patch("fructosa.fructosad.setup_logging") as psetup_logging:
            instance = self.test_class(self.mocked_conf)
        with patch("fructosa.fructosad.open", mock_open(read_data=" 23 \n")) as mopen:
            instance.stop()
        instance.logger.warning.assert_called_once_with(
            instance._stopped_message
        )
        
    # @patch("fructosa.fructosad.os.path.exists")
    # @patch("fructosa.fructosad.os.kill")
    # def test_stop_doesnt_kill_if_no_pidfile(self, pkill, pexists):
    #     pexists.return_value = False
    #     self.simple_instance.stop()
    #     pkill.assert_not_called()
    @patch("fructosa.fructosad.setup_logging")
    @patch("fructosa.fructosad.os.kill")
    def test_stop_cleanup_behaviour_if_no_pidfile(self, pkill, psetup_logging):
        instance = self.test_class(self.mocked_conf)
        pidfile_mock = MagicMock()
        instance.pidfile = pidfile_mock
        with patch("fructosa.fructosad.open", mock_open()) as mopen:
            mopen.side_effect = FileNotFoundError
            with self.assertRaises(SystemExit) as system_exit:
                instance.stop()
        self.assertEqual(system_exit.exception.code, START_STOP_ERROR)
        pkill.assert_not_called()
        instance.logger.error.assert_called_once_with(
            "{}: {}".format(
                instance._cant_stop_message,
                PIDFILE_NOT_FOUND.format(pidfile=pidfile_mock))
        )

    @patch("fructosa.fructosad.setup_logging")
    @patch("fructosa.fructosad.os.kill")
    def test_stop_cleanup_behaviour_if_no_permission_to_read_pidfile(
            self, pkill, psetup_logging):
        instance = self.test_class(self.mocked_conf)
        with patch("fructosa.fructosad.open", mock_open()) as mopen:
            mopen.side_effect = PermissionError
            with self.assertRaises(SystemExit) as system_exit:
                instance.stop()
        self.assertEqual(system_exit.exception.code, START_STOP_ERROR)
        pkill.assert_not_called()
        instance.logger.error.assert_called_once_with(
            "{}: {}".format(
                instance._cant_stop_message,
                PROTO_NO_PERMISSION_PIDFILE.format(
                    pidfile=instance.pidfile, action=PIDFILE_ACTION_ACCESSED))
        )

    @patch("fructosa.fructosad.setup_logging")
    @patch("fructosa.fructosad.os.kill")
    def test_stop_cleanup_behaviour_if_invalid_pids(
            self, pkill, psetup_logging):
        instance = self.test_class(self.mocked_conf)
        for data, ex in zip(("333998294434332", "asds"), (OverflowError, ValueError)):
            pkill.side_effect = ex
            with patch("fructosa.fructosad.open", mock_open(read_data=data)) as mopen:
                with self.assertRaises(SystemExit) as system_exit:
                    instance.stop()
            self.assertEqual(system_exit.exception.code, START_STOP_ERROR)
            instance.logger.error.assert_called_once_with(
                "{}: {}".format(
                    instance._cant_stop_message,
                    INVALID_PID.format(pid=data))
            )
            instance.logger.error.reset_mock()

    @patch("fructosa.fructosad.setup_logging")
    @patch("fructosa.fructosad.os.kill")
    def test_stop_cleanup_behaviour_no_process(self, pkill, psetup_logging):
        instance = self.test_class(self.mocked_conf)
        pidfile_mock = MagicMock()
        instance.pidfile = pidfile_mock
        with patch("fructosa.fructosad.open", mock_open(read_data=" 34324")) as mopen:
            pkill.side_effect = ProcessLookupError
            with self.assertRaises(SystemExit) as system_exit:
                instance.stop()
        self.assertEqual(system_exit.exception.code, START_STOP_ERROR)
        instance.logger.error.assert_called_once_with(
            "{}: {}".format(
                instance._cant_stop_message,
                PROCESS_DOES_NOT_EXIST.format(pid="34324"))
        )
        
    @patch("fructosa.fructosad.FructosaD._clean_up")
    def test_run_loop_call_sequence(self, _clean_up):
        event_loop = MagicMock()
        run_forever = MagicMock()
        event_loop.run_forever = run_forever
        manager = MagicMock()
        manager.attach_mock(run_forever, "run_forever")
        manager.attach_mock(_clean_up, "_clean_up")
        expected_calls = [call.run_forever(), call._clean_up()]
        self.simple_instance._event_loop = event_loop
        self.simple_instance._run_loop()
        manager.assert_has_calls(expected_calls)

    @patch("fructosa.fructosad.FructosaD._clean_up")
    def test_run_loop_calls_loop_close_method_even_if_exception_raises(self, _clean_up):
        event_loop = MagicMock()
        run_forever = MagicMock()
        run_forever.side_effect = Exception()
        event_loop.run_forever = run_forever
        self.simple_instance._event_loop = event_loop
        with self.assertRaises(Exception):
            self.simple_instance._run_loop()
        _clean_up.assert_called_once_with()

    def test_clean_up_calls_event_loop_close(self):
        event_loop = MagicMock()
        self.simple_instance._event_loop = event_loop
        self.simple_instance._clean_up()
        event_loop.close.assert_called_once_with()
    
    @patch("fructosa.fructosad.FructosaD._run_loop")
    def test_run_calls_run_loop(self, prun_loop):
        self.simple_instance.run()
        prun_loop.assert_called_once_with()

    def test_submit_task_arguments(self):
        s = signature(self.simple_instance.submit_task)
        parameters = s.parameters
        param_kinds = [param.kind for param in parameters.values()]
        expected_params = [
            Parameter.POSITIONAL_OR_KEYWORD, Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD
        ]
        self.assertEqual(expected_params, param_kinds)

    def test_submit_task_calls_loop_create_task_method(self):
        event_loop = MagicMock()
        self.simple_instance._event_loop = event_loop
        task = MagicMock()
        returned_task = MagicMock()
        task.return_value = returned_task
        args = MagicMock()
        kwargs = MagicMock()
        self.simple_instance.submit_task(task, *args, **kwargs)
        task.assert_called_once_with(*args, **kwargs)
        event_loop.create_task.assert_called_once_with(returned_task)

    @patch("fructosa.fructosad.asyncio.Queue")
    def test_create_queues_method_sets_needed_attributes(self, pQueue):
        self.simple_instance._create_queues()
        pQueue.assert_called_once_with()
        self.assertEqual(
            self.simple_instance._to_graphite_queue, pQueue.return_value
        )

    def test_send_to_graphite_is_a_coroutine(self):
        from inspect import iscoroutinefunction
        self.assertTrue(iscoroutinefunction(self.test_class._send_to_graphite))

    @patch("fructosa.fructosad.LMessage")
    def test_send_to_graphite_awaits_in_queue_get(self, mock_LMessage):
        with patch(
                "fructosa.fructosad.asyncio.open_connection", new=AsyncioMock()
                ) as open_connection:
            reader = MagicMock()
            writer = MagicMock()
            open_connection.mock.return_value = (reader, writer)
            self.simple_instance._to_graphite_queue = MagicMock()
            self.simple_instance._event_loop = MagicMock()
            for num in 4,2,3:
                values = [MagicMock() for _ in range(num)] + [InventedException()]
                self.simple_instance._to_graphite_queue.get = AsyncioMock(
                    side_effect=values)
                self.simple_instance._to_graphite_queue.get.mock.side_effect = values
                expected_calls_get = [call() for value in values[:-1]]
                with self.assertRaises(InventedException):
                    asyncio_run(self.simple_instance._send_to_graphite())
                self.simple_instance._to_graphite_queue.get.mock.assert_has_calls(
                    expected_calls_get)
                self.simple_instance._to_graphite_queue.get.mock.reset_mock()

    @patch("fructosa.fructosad.LMessage")
    @patch("fructosa.fructosad.asyncio.open_connection", new=AsyncioMock())
    def test_send_to_graphite_awaits_open_connection_only_once_if_connection(self, mock_LMessage):
        from fructosa.fructosad import asyncio
        mock_open_connection = asyncio.open_connection
        reader = MagicMock()
        writer = MagicMock()
        graphite_conf = {
            GRAPHITE_HOST_KEY: "qaqa",
            GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY: 212434,
        }
        def getitem(value):
            return graphite_conf[value]
        self.mocked_conf.graphite.__getitem__.side_effect = getitem
        # The following is to avoid having problems with the event loop
        self.simple_instance._event_loop = MagicMock()
        mock_open_connection.mock.return_value = (reader, writer)
        for num in 1, 5, 2:
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            self.simple_instance._to_graphite_queue.get = AsyncioMock(
                side_effect=values)
            self.simple_instance._to_graphite_queue.get.mock.side_effect = values
            with self.assertRaises(InventedException):
                asyncio_run(self.simple_instance._send_to_graphite())
            mock_open_connection.mock.assert_called_once_with(
                "qaqa", 212434, loop=self.simple_instance._event_loop
            )
            mock_open_connection.mock.reset_mock()

    @patch("fructosa.fructosad.LMessage")
    @patch("fructosa.fructosad.asyncio.open_connection", new=AsyncioMock())
    def test_send_to_graphite_sends_raw_message_to_logger(self, mock_LMessage):
        from fructosa.fructosad import asyncio
        mock_open_connection = asyncio.open_connection
        reader = MagicMock()
        writer = MagicMock()
        # The following is to avoid having problems with the event loop
        self.simple_instance._event_loop = MagicMock()
        logger = self.simple_instance.logger
        log_level = "DEBUG"
        log_template = "{}:{}:{}".format(
            log_level, self.simple_instance.__class__.__name__, PROTO_MSG_TO_GRAPHITE,
        )
        mock_open_connection.mock.return_value = (reader, writer)
        for num in 4, 2:
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            self.simple_instance._to_graphite_queue.get = AsyncioMock(
                side_effect=values)
            #args = aquin+[LMessage.from_remote(_) for _ in values[:-1]]
            args = values[:-1]
            expected = [log_template.format(_) for _ in args]
            self.simple_instance._to_graphite_queue.get.mock.side_effect = values
            with self.assertRaises(InventedException):
                with self.assertLogs(logger, level=log_level) as log:
                    asyncio_run(self.simple_instance._send_to_graphite())
            for expected_line in expected:
                self.assertIn(expected_line, log.output)

    @patch("fructosa.fructosad.LMessage")
    @patch("fructosa.fructosad.asyncio.open_connection", new=AsyncioMock())
    def test_send_to_graphite_writes_message_to_writer(self, mock_LMessage):
        from fructosa.fructosad import asyncio
        mock_open_connection = asyncio.open_connection
        reader = MagicMock()
        writer = MagicMock()
        # The following is to avoid having problems with the event loop
        self.simple_instance._event_loop = MagicMock()
        mock_open_connection.mock.return_value = (reader, writer)
        
        for num in 1, 3:
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            self.simple_instance._to_graphite_queue.get = AsyncioMock(
                side_effect=values)
            #args = aquin+[LMessage.from_remote(_) for _ in values[:-1]]
            args = values[:-1]
            expected_calls = [call(mock_LMessage(_).to_graphite()) for _ in args]
            self.simple_instance._to_graphite_queue.get.mock.side_effect = values
            with self.assertRaises(InventedException):
                asyncio_run(self.simple_instance._send_to_graphite())
            writer.write.assert_has_calls(expected_calls)
            writer.write.reset_mock()

    @patch("fructosa.fructosad.LMessage")
    @patch("fructosa.fructosad.asyncio.open_connection", new=AsyncioMock())
    def test_send_to_graphite_behaviour_if_invalid_message(self, mock_LMessage):
        from fructosa.fructosad import asyncio
        mock_open_connection = asyncio.open_connection
        reader = MagicMock()
        writer = MagicMock()
        # The following is to avoid having problems with the event loop
        self.simple_instance._event_loop = MagicMock()
        mock_open_connection.mock.return_value = (reader, writer)
        num = 4
        unsuitable_msg = MagicMock()
        values = [MagicMock() for _ in range(num)] + [InventedException()]
        self.simple_instance._to_graphite_queue.get = AsyncioMock(
            side_effect=values)
        #args = aquin+[LMessage.from_remote(_) for _ in values[:-1]]
        err_msg_unsuit = "paripe paripa"
        err_msg_pickle = "pickle is mean"
        args = values[:-1]
        data_to_write = [MagicMock() for _ in range(num-2)]
        idata_to_write = iter(data_to_write)
        def lmessage_init(raw_value):
            if raw_value == args[1]:
                return unsuitable_msg
            elif raw_value == args[2]:
                raise WrongPickleMessage(err_msg_pickle)
            else:
                return next(idata_to_write)
        mock_LMessage.side_effect = lmessage_init
        unsuitable_msg.to_graphite.side_effect = UnsuitableLMessage(err_msg_unsuit)
        self.simple_instance._to_graphite_queue.get.mock.side_effect = values
        logger = self.simple_instance.logger
        log_level = "ERROR"
        expected_log_msg = "{}:FructosaD:{}".format(log_level, err_msg_unsuit)
        with self.assertRaises(InventedException):
            with self.assertLogs(logger, level=log_level) as log:            
                asyncio_run(self.simple_instance._send_to_graphite())
        writer.write.assert_has_calls(
            [call(_.to_graphite.return_value) for _ in data_to_write]
        )
        self.assertEqual(writer.write.call_count, 2)
        self.assertIn(expected_log_msg, log.output)
        
    @patch("fructosa.fructosad.asyncio.sleep", new=AsyncioMock())
    @patch("fructosa.fructosad.asyncio.open_connection", new=AsyncioMock())
    def test_send_to_graphite_awaits_sleep_if_ConnectionRefusedError(self):
        from fructosa.fructosad import asyncio
        mock_open_connection = asyncio.open_connection
        reader = MagicMock()
        writer = MagicMock()
        # The following is to avoid having problems with the event loop
        self.simple_instance._event_loop = MagicMock()
        values = [ConnectionRefusedError(), ConnectionRefusedError(), (reader, writer)]
        mock_open_connection.mock.side_effect = values
        self.simple_instance._to_graphite_queue.get = AsyncioMock(side_effect=InventedException())
        expected_calls = [call(1), call(1)]
        with self.assertRaises(InventedException):
            asyncio_run(self.simple_instance._send_to_graphite())
        asyncio.sleep.mock.assert_has_calls(expected_calls)

    @patch("fructosa.fructosad.asyncio.open_connection", new=AsyncioMock())
    def test_send_to_graphite_logs_if_no_connection(self):
        from fructosa.fructosad import asyncio
        mock_open_connection = asyncio.open_connection
        graphite_conf = {
            GRAPHITE_HOST_KEY: "jamacuquen",
            GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY: 21555,
        }
        def getitem(value):
            return graphite_conf[value]
        self.mocked_conf.graphite.__getitem__.side_effect = getitem        
        logger = self.simple_instance.logger
        log_level = "INFO"
        # The following is to avoid having problems with the event loop
        self.simple_instance._event_loop = MagicMock()
        mock_open_connection.mock.side_effect = InventedException()
        expected = TO_GRAPHITE_CONNECTING_MSG.format(
            host_key=GRAPHITE_HOST_KEY,
            host="jamacuquen",
            port_key=GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY,
            port=21555,
        )
        expected = "{}:{}:{}".format(
            log_level, self.simple_instance.__class__.__name__, expected
        )
        self.simple_instance._to_graphite_queue.get = AsyncioMock(
            side_effect=InventedException())
        with self.assertRaises(InventedException):
            with self.assertLogs(logger, level=log_level) as log:            
                asyncio_run(self.simple_instance._send_to_graphite())
        self.assertIn(expected, log.output)
    
    @patch("fructosa.fructosad.asyncio.open_connection", new=AsyncioMock())
    def test_send_to_graphite_logs_if_connected_and_no_refused_trials(self):
        from fructosa.fructosad import asyncio
        mock_open_connection = asyncio.open_connection
        reader = MagicMock()
        writer = MagicMock()
        graphite_conf = {
            GRAPHITE_HOST_KEY: "jamacuquen",
            GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY: 21555,
        }
        def getitem(value):
            return graphite_conf[value]
        self.mocked_conf.graphite.__getitem__.side_effect = getitem        
        logger = self.simple_instance.logger
        log_level = "INFO"
        # The following is to avoid having problems with the event loop
        self.simple_instance._event_loop = MagicMock()
        mock_open_connection.mock.return_value = (reader, writer)
        expected0 = TO_GRAPHITE_CONNECTING_MSG.format(
            host_key=GRAPHITE_HOST_KEY,
            host="jamacuquen",
            port_key=GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY,
            port=21555,
        )
        proto = [expected0, TO_GRAPHITE_CONNECTED_MSG]
        cn = self.simple_instance.__class__.__name__
        expected = ["{}:{}:{}".format(log_level, cn, _) for _ in proto]
        self.simple_instance._to_graphite_queue.get = AsyncioMock(
            side_effect=InventedException())
        with self.assertRaises(InventedException):
            with self.assertLogs(logger, level=log_level) as log:            
                asyncio_run(self.simple_instance._send_to_graphite())
        for line in expected:
            self.assertIn(line, log.output)

    @patch("fructosa.fructosad.asyncio.sleep", new=AsyncioMock())
    @patch("fructosa.fructosad.asyncio.open_connection", new=AsyncioMock())
    def test_send_to_graphite_logs_if_connected_but_refused_trials(self):
        from fructosa.fructosad import asyncio
        mock_open_connection = asyncio.open_connection
        reader = MagicMock()
        writer = MagicMock()
        graphite_conf = {
            GRAPHITE_HOST_KEY: "gul",
            GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY: 21555,
        }
        def getitem(value):
            return graphite_conf[value]
        self.mocked_conf.graphite.__getitem__.side_effect = getitem        
        logger = self.simple_instance.logger
        log_level = "INFO"
        # The following is to avoid having problems with the event loop
        self.simple_instance._event_loop = MagicMock()
        trials = [ConnectionRefusedError()]*3 + [(reader, writer)]
        #trials = [ConnectionRefusedError(), (reader, writer)]
        mock_open_connection.mock.side_effect = trials
        start = TO_GRAPHITE_CONNECTING_MSG.format(
            host_key=GRAPHITE_HOST_KEY,
            host="gul",
            port_key=GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY,
            port=21555,
        )
        retry_msg = TO_GRAPHITE_RETRY_MSG.format(host="gul")
        connected = TO_GRAPHITE_CONNECTED_MSG
        proto = [start] + [retry_msg]*3 + [connected]
        cn = self.simple_instance.__class__.__name__
        expected = ["{}:{}:{}".format(log_level, cn, _) for _ in proto]
        self.simple_instance._to_graphite_queue.get = AsyncioMock(
            side_effect=InventedException())
        with self.assertRaises(InventedException):
            with self.assertLogs(logger, level=log_level) as log:            
                asyncio_run(self.simple_instance._send_to_graphite())
        self.assertEqual(expected, log.output)


    # @patch("fructosa.fructosad.convert_pickled_dict_to_graphite_format")
    # def test_send_to_graphite_calls_writer_write_with_correct_arg(
    #         self, mock_convert_pickled_dict_to_graphite_format):
    #     with patch(
    #             "fructosa.fructosad.asyncio.open_connection", new=AsyncioMock()
    #             ) as open_connection:
    #         reader = MagicMock()
    #         writer = MagicMock()
    #         open_connection.mock.return_value = (reader, writer)
    #         self.simple_instance._to_graphite_queue = MagicMock()
    #         for num in 1,2,5:
    #             values = [MagicMock() for _ in range(num)] + [InventedException()]
    #             self.simple_instance._to_graphite_queue.get = AsyncioMock(side_effect=values)
    #             expected_calls = [call(value) for value in values[:-1]]
    #             with self.assertRaises(InventedException):
    #                 asyncio_run(self.simple_instance.send_to_graphite())
    #             writer.write.assert_has_calls(expected_calls)
    #             writer.write.reset_mock()


        
if __name__ == "__main__":
    unittest.main()
