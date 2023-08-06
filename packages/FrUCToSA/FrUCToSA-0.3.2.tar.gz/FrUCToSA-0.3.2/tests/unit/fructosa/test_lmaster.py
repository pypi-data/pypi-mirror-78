#!/bin/env python3

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
import logging

from unittest.mock import patch, MagicMock, call, mock_open, PropertyMock
from inspect import signature, Parameter, iscoroutinefunction

from .aio_tools import asyncio_run, AsyncioMock

import fructosa.lmaster
from fructosa.constants import (
    LAGENT_TO_LMASTER_DATA_PORT_KEY, LMASTER_HOST_KEY,
    ACTION_STR, PIDFILE_STR, OWN_LOG_SECTION, OWN_LOG_FILE_KEY,
    HEARTBEAT_LISTENING_MSG_TEMPLATE, HEARTBEAT_PORT,
)


class InventedException(Exception):
    pass


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.main = fructosa.lmaster.main
        
    def test_is_executable(self):
        self.assertIn("__call__", dir(self.main))

    def test_takes_no_arguments(self):
        s = signature(self.main)
        parameters = s.parameters
        self.assertEqual(len(parameters), 0)

    @patch("fructosa.lmaster.generic_main")
    @patch("fructosa.lmaster.LMaster")
    @patch("fructosa.lmaster.LMasterConf")
    def test_calls_generic_main(self, pmasterconf, pmaster, pgeneric_main):
        self.main()
        pgeneric_main.assert_called_once_with(pmasterconf, pmaster)

        
class LMasterBase:
    def setUp(self):
        self.test_class = fructosa.lmaster.LMaster
        self.mocked_conf = MagicMock()
        setattr(self.mocked_conf, ACTION_STR, "")
        setattr(self.mocked_conf, PIDFILE_STR, "")
        self.simple_logging = {OWN_LOG_FILE_KEY: "/dev/null"}
        setattr(self.mocked_conf, OWN_LOG_SECTION, self.simple_logging)
        self.simple_instance = self.test_class(self.mocked_conf)


class LMasterTestCase(LMasterBase, unittest.TestCase):
    def test_LMaster_is_subclass_of_FructosaD(self):
        from fructosa.fructosad import FructosaD
        self.assertTrue(issubclass(self.test_class, FructosaD))

    def test_instance_defines_some_strings(self):
        from fructosa.lmaster import (
            LMASTER_STARTING_MESSAGE, LMASTER_STOP_MESSAGE, LMASTER_CANT_STOP_MESSAGE
        )
        inst = self.simple_instance
        self.assertEqual(inst._starting_message, LMASTER_STARTING_MESSAGE)
        self.assertEqual(inst._stopped_message, LMASTER_STOP_MESSAGE)
        self.assertEqual(inst._cant_stop_message, LMASTER_CANT_STOP_MESSAGE)
        
    @patch("fructosa.lmaster.FructosaD.run")
    @patch("fructosa.lmaster.LMaster.submit_task")
    @patch("fructosa.lmaster.LMaster._run_server")
    @patch("fructosa.lmaster.LMaster._create_server")
    def test_run_call_sequence(self, _create_server, _run_server, submit_task, run):
        manager = MagicMock()
        server = MagicMock()
        _create_server.return_value = server
        manager.attach_mock(_create_server, "_create_server")
        manager.attach_mock(_run_server, "_run_server")
        manager.attach_mock(submit_task, "submit_task")
        manager.attach_mock(run, "run")
        expected_calls = [
            call._create_server(),
            call._run_server(server),
            call.submit_task(self.simple_instance.heartbeats_sink),
            #call.submit_task(self.simple_instance._send_to_graphite),
            call.run(),
        ]
        self.simple_instance.run()
        manager.assert_has_calls(expected_calls)
        
    @patch("fructosa.lmaster.asyncio.start_server")
    def test_create_server_calls_to_and_returns_from_start_server(self, start_server):
        server = MagicMock()
        mock_conf = MagicMock()
        self.simple_instance._conf = mock_conf
        host = "ayeleole"
        port = 8686844
        def getitem(value):
            return {LMASTER_HOST_KEY: host, LAGENT_TO_LMASTER_DATA_PORT_KEY: port}[value]
        mock_conf.lmaster.__getitem__.side_effect = getitem
        start_server.return_value = server
        result = self.simple_instance._create_server()
        start_server.assert_called_once_with(
            self.simple_instance._handle_connection, host, port,
            loop=self.simple_instance._event_loop
        )
        self.assertEqual(result, server)

    def test_run_server_sends_coroutine_to_event_loop(self):
        server_coroutine = MagicMock()
        server = MagicMock()
        self.simple_instance._event_loop = MagicMock()
        self.simple_instance._event_loop.run_until_complete.return_value = server
        run_until_complete = self.simple_instance._event_loop.run_until_complete
        self.simple_instance._run_server(server_coroutine)
        run_until_complete.assert_called_once_with(server_coroutine)
        self.assertEqual(server, self.simple_instance.server)

    def test_run_server_sends_message_to_logger(self):
        from fructosa.constants import SERVING_PROTO_MESSAGE
        logger = MagicMock()
        server = MagicMock()
        self.simple_instance._event_loop = MagicMock()
        run_until_complete = MagicMock()
        run_until_complete.return_value = server
        self.simple_instance._event_loop.run_until_complete = run_until_complete
        self.simple_instance.logger = logger
        self.simple_instance._run_server(MagicMock())
        message = SERVING_PROTO_MESSAGE.format(server.sockets[0].getsockname())
        logger.info.assert_called_once_with(message)

    @patch("fructosa.lmaster.FructosaD._clean_up")
    def test_clean_up_call_sequence(self, fructosad_clean_up):
        manager = MagicMock()
        close = MagicMock()
        run_until_complete = MagicMock()
        server = MagicMock()
        wait_closed = MagicMock()
        server.wait_closed.return_value = wait_closed
        self.simple_instance.server = server
        event_loop = MagicMock()
        self.simple_instance._event_loop = event_loop
        manager.attach_mock(server, "server")
        manager.attach_mock(event_loop, "_event_loop")
        manager.attach_mock(fructosad_clean_up, "_clean_up")
        expected_calls = [
            call.server.close(),
            call.server.wait_closed(),
            call._event_loop.run_until_complete(wait_closed),
            call._clean_up()
        ]
        self.simple_instance._clean_up()
        manager.assert_has_calls(expected_calls)

    def test_handle_connection_is_a_coroutine(self):
        from inspect import iscoroutinefunction
        self.assertTrue(iscoroutinefunction(self.test_class._handle_connection))

    def test_handle_connection_takes_two_parameters(self):
        s = signature(self.simple_instance._handle_connection)
        parameters = s.parameters
        self.assertEqual(len(parameters), 2)

    @patch("fructosa.lmaster.pickle.loads")
    def test_handle_connection_awaits_reader_read(self, loads):    
        from fructosa.constants import INITIAL_LMASTER_SERVER_PACKET_SIZE
        reader = MagicMock()
        writer = MagicMock()
        for num in 4,1,2:
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            reader.read = AsyncioMock(side_effect=values)
            expected_calls_get = [
                call(INITIAL_LMASTER_SERVER_PACKET_SIZE) for value in values[:-1]
            ]
            with self.assertRaises(InventedException):
                asyncio_run(self.simple_instance._handle_connection(reader, writer))
            reader.read.mock.assert_has_calls(expected_calls_get)

    @patch("fructosa.lmaster.pickle.loads")
    def test_handle_connection_awaits_to_graphite_queue_put(self, loads):    
        from fructosa.constants import INITIAL_LMASTER_SERVER_PACKET_SIZE
        reader = MagicMock()
        writer = MagicMock()
        self.simple_instance._to_graphite_queue = MagicMock()
        for num in 3,2,5:
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            reader.read = AsyncioMock(side_effect=values)
            self.simple_instance._to_graphite_queue.put = AsyncioMock()
            expected_calls_put = [call(value) for value in values[:-1]]
            with self.assertRaises(InventedException):
                asyncio_run(self.simple_instance._handle_connection(reader, writer))
            self.simple_instance._to_graphite_queue.put.mock.assert_has_calls(
                expected_calls_put
            )
            self.simple_instance._to_graphite_queue.put.mock.reset_mock()

    @patch("fructosa.lmaster.pickle.loads")
    def test_handle_connection_calls_once_to_writer_get_extra_info(self, loads):    
        reader = MagicMock()
        writer = MagicMock()
        extra_info = MagicMock()
        writer.get_extra_info = extra_info
        for num in 6,2,4:
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            reader.read = AsyncioMock(side_effect=values)
            with self.assertRaises(InventedException):
                asyncio_run(self.simple_instance._handle_connection(reader, writer))
            extra_info.assert_called_once_with("peername")
            extra_info.reset_mock()

    @patch("fructosa.lmaster.pickle.loads")
    def test_handle_connection_sends_wished_message_to_logger(self, loads):
        from fructosa.constants import PROTO_MEASUREMENT_RECEIVED_MSG
        import pickle
        reader = MagicMock()
        writer = MagicMock()
        addr = MagicMock()
        writer.get_extra_info.return_value = addr
        for num in 3,5,1:
            logger = MagicMock()
            self.simple_instance.logger = logger
            values = [MagicMock() for _ in range(num)] + [InventedException()]
            loads_values = [MagicMock() for _ in range(num)]
            loads.side_effect = loads_values
            reader.read = AsyncioMock(side_effect=values)
            log_msgs = [
                PROTO_MEASUREMENT_RECEIVED_MSG.format(addr, msg) for msg in loads_values
            ]
            expected_calls_logger_debug = [call(msg) for msg in log_msgs]
            expected_calls_loads = [call(value) for value in values[:-1]]
            with self.assertRaises(InventedException):
                asyncio_run(self.simple_instance._handle_connection(reader, writer))
            logger.debug.assert_has_calls(expected_calls_logger_debug)
            loads.assert_has_calls(expected_calls_loads)
            loads.reset_mock()
    
                
class LMasterHeartbeatTestCase(LMasterBase, unittest.TestCase):
    def test_heartbeats_sink_is_a_coroutine(self):
        self.assertTrue(
            iscoroutinefunction(self.test_class.heartbeats_sink)
        )

    def test_heartbeats_sink_logs_start_message(self):
        mock_conf = MagicMock()
        self.simple_instance._conf = mock_conf
        host = "aylasole"
        def getitem(value):
            return {LMASTER_HOST_KEY: host}[value]
        mock_conf.lmaster.__getitem__.side_effect = getitem
        msg = HEARTBEAT_LISTENING_MSG_TEMPLATE.format(
            master=host, hb_port=HEARTBEAT_PORT
        )
        logger = self.simple_instance.__class__.__name__
        with self.assertLogs(logger, level=logging.INFO) as log:
            with patch("fructosa.lmaster.HeartbeatSink") as hb_snk:
                hb_snk.return_value = AsyncioMock(side_effect=InventedException())
                with self.assertRaises(InventedException):
                    asyncio_run(self.simple_instance.heartbeats_sink())
        self.assertIn(msg, log.output[0])

    def test_heartbeats_sink_creates_heartbeatsource_instance(self):
        mock_conf = MagicMock()
        self.simple_instance._conf = mock_conf
        host = "bls"
        mock_conf.lmaster.__getitem__.return_value = host
        with patch("fructosa.lmaster.HeartbeatSink") as hb_snk:
            hb_snk.return_value = AsyncioMock(side_effect=InventedException())
            with self.assertRaises(InventedException):
                asyncio_run(self.simple_instance.heartbeats_sink())
        hb_snk.assert_called_once_with(
            host=host, port=HEARTBEAT_PORT,
            logging_conf=self.simple_instance._conf.logging
        )
        
    def test_heartbeats_sink_awaits_for_heartbeatsink(self):
        ahb = AsyncioMock()
        with patch("fructosa.lmaster.HeartbeatSink") as hb_snk:
            hb_snk.return_value = ahb
            asyncio_run(self.simple_instance.heartbeats_sink())
        ahb.mock.assert_called_once_with()

        
if __name__ == "__main__":
    unittest.main()

