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
from unittest.mock import patch, MagicMock, call, mock_open, PropertyMock
from inspect import signature, Parameter

from fructosa.constants import (
    OWN_LOG_FILE_KEY, OWN_LOG_LEVEL_KEY,
)

from .aio_tools import asyncio_run, AsyncioMock

class InventedException(Exception):
    pass


class sensor_factoryTestCase(unittest.TestCase):
    def setUp(self):
        from fructosa.sensors import sensor_factory
        self.test_func = sensor_factory
    
    def test_init_parameters(self):
        s = signature(self.test_func)
        parameters = s.parameters
        self.assertEqual(len(parameters), 3)

    @patch("fructosa.sensors._make_sensor")
    @patch("fructosa.sensors._is_sensor")
    def test_calls_is_sensor(self, pis_sensor, pmake_sensor):
        name = MagicMock()
        opts = MagicMock()
        logging = MagicMock()
        self.test_func(name, opts, logging)
        pis_sensor.assert_called_once_with(name)

    @patch("fructosa.sensors._make_sensor")
    @patch("fructosa.sensors._is_sensor")
    def test_raises_NameError_if_not_valid_sensor_name(self, pis_sensor, pmake_sensor):
        name = MagicMock()
        opts = MagicMock()
        logging = MagicMock()
        pis_sensor.return_value = False
        with self.assertRaises(NameError):
            result = self.test_func(name, opts, logging)

    @patch("fructosa.sensors._make_sensor")
    @patch("fructosa.sensors._is_sensor")
    def test_returns_result_of_make_sensor_if_valid_sensor_name(
            self, pis_sensor, pmake_sensor):
        name = MagicMock()
        opts = MagicMock()
        sensor = MagicMock()
        logging = MagicMock()
        pmake_sensor.return_value = sensor
        pis_sensor.return_value = True
        result = self.test_func(name, opts, logging)
        self.assertEqual(result, sensor)
        pmake_sensor.assert_called_once_with(name, opts, logging)

        
class is_sensorTestCase(unittest.TestCase):
    def setUp(self):
        from fructosa.sensors import _is_sensor
        self.test_func = _is_sensor
        
    @patch("fructosa.sensors._find_all_sensors")
    def test_calls_find_all_sensors(self, pfind_all_sensors):
        name = MagicMock()
        self.test_func(name)
        pfind_all_sensors.assert_called_once_with()

    @patch("fructosa.sensors._find_all_sensors")
    def test_return_True_if_valid_sensor(self, pfind_all_sensors):
        all_sensors = MagicMock()
        all_sensors.__contains__.return_value = True
        pfind_all_sensors.return_value = all_sensors
        name = MagicMock()
        result = self.test_func(name)
        self.assertTrue(result)
        
                
class find_all_sensorsTestCase(unittest.TestCase):
    def setUp(self):
        from fructosa.sensors import _find_all_sensors
        self.test_func = _find_all_sensors
        a_sensor = MagicMock()
        self.globals_all_sensors_collection = []
        self.globals_not_sensors_collection = []
        self.globals_mixed_collection = []
        for i in range(5):
            sensors = {"sensor{}".format(_): a_sensor for _ in range(i)}
            not_sensors = {}
            for _ in range(i):
                not_sensor = MagicMock()
                if _ == 1:
                    not_sensor.issubclass_raises = True
                not_sensors["whatever{}".format(_)] = not_sensor
            self.globals_all_sensors_collection.append(sensors)
            self.globals_not_sensors_collection.append(not_sensors)
            for j in range(5):
                mixed = {"whatever{}".format(_): MagicMock() for _ in range(j)}
                mixed.update(sensors)
                self.globals_mixed_collection.append(mixed)
        def mocked_issubclass(cls, other_cls):
            if cls.issubclass_raises == True:
                raise TypeError()
            elif cls == a_sensor:
                return True
            else:
                return False
        self.mocked_issubclass = mocked_issubclass
    
    @patch("fructosa.sensors.globals")
    def test_calls_globals_builtin(self, pglobals):
        self.test_func()
        pglobals.assert_called_once_with()

    @patch("fructosa.sensors.issubclass")
    @patch("fructosa.sensors.globals")
    def test_return_value_if_globals_are_all_sensors(self, pglobals, pissubclass):
        pissubclass.side_effect = self.mocked_issubclass
        for my_globals in self.globals_all_sensors_collection:
            pglobals.return_value = my_globals
            result = self.test_func()
            self.assertEqual(result, my_globals)
        
    @patch("fructosa.sensors.issubclass")
    @patch("fructosa.sensors.globals")
    def test_return_value_if_globals_are_not_sensors(self, pglobals, pissubclass):
        pissubclass.side_effect = self.mocked_issubclass
        for my_globals in self.globals_not_sensors_collection:
            pglobals.return_value = my_globals
            result = self.test_func()
            self.assertEqual(result, {})

    @patch("fructosa.sensors.issubclass")
    @patch("fructosa.sensors.globals")
    def test_return_value_if_globals_have_sensors_and_others(self, pglobals, pissubclass):
        pissubclass.side_effect = self.mocked_issubclass
        for my_globals in self.globals_all_sensors_collection:
            pglobals.return_value = my_globals
            expected = {k: v for k, v in my_globals.items() if k.startswith("sensor")}
            result = self.test_func()
            self.assertEqual(result, expected)
        

class make_sensorTestCase(unittest.TestCase):
    def setUp(self):
        from fructosa.sensors import _make_sensor
        self.test_func = _make_sensor
        
    @patch("fructosa.sensors._find_all_sensors")
    def test_calls_find_all_sensors(self, pfind_all_sensors):
        name = MagicMock()
        opts = MagicMock()
        logging = MagicMock()
        self.test_func(name, opts, logging)
        pfind_all_sensors.assert_called_once_with()

    @patch("fructosa.sensors._find_all_sensors")
    def test_return_value(self, pfind_all_sensors):
        opts = MagicMock()
        logging = MagicMock()
        all_sensors = MagicMock()
        my_sensor = MagicMock()
        my_sensor_instance = MagicMock()
        def my_side_effect(logging, **par):
            if par == dict(opts):
                return my_sensor_instance
            else:
                return MagicMock() 
        my_sensor.side_effect = my_side_effect
        def getitem(key):
            if key == "my_sensor":
                return my_sensor
            else:
                return MagicMock()
        all_sensors.__getitem__.side_effect = getitem
        pfind_all_sensors.return_value = all_sensors
        result = self.test_func("my_sensor", opts, logging)
        self.assertEqual(result, my_sensor_instance)
        

class SensorTestCaseBase(unittest.TestCase):
    def setUp(self):
        self.mocked_time_interval = MagicMock()
        self.some_logging = {OWN_LOG_FILE_KEY: "/dev/null", OWN_LOG_LEVEL_KEY: 17}
        self.mocked_logging = MagicMock()
        self.host = "ma.cha.cant.es"
        self.class_name = self.test_class.__name__
        mocked_name = PropertyMock(return_value=self.class_name)
        self.mocked_name = mocked_name
        self.real_log_instance = self.test_class(self.some_logging, self.mocked_time_interval)
        self.real_log_instance._host = self.host
        type(self.real_log_instance).name = mocked_name
        with patch("fructosa.sensors.setup_logging") as self.psetup_logging:
            self.instance = self.test_class(self.mocked_logging, self.mocked_time_interval)
            type(self.instance).name = mocked_name
        self.instance._host = self.host
                        
class SensorTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import Sensor
        self.test_class = Sensor
        super().setUp()
        
    def test_init_parameters(self):
        s = signature(self.test_class)
        parameters = s.parameters
        self.assertEqual(len(parameters), 2)

    def test_instance_has_needed_attributes(self):
        self.assertEqual(self.instance.time_interval, self.mocked_time_interval)
        self.assertEqual(self.instance._logger, self.psetup_logging.return_value)
        self.assertEqual(self.instance.host, self.host)

    def test_setup_logger_called_correctly(self):
        self.psetup_logging.assert_called_once_with(
            logger_name=self.instance.name, rotatingfile_conf=self.mocked_logging
        )

    def test_instance_can_be_called(self):
        self.instance(MagicMock())

    def test_calling_instance_logs_message(self):
        import logging
        from fructosa.constants import PROTO_SENSOR_STARTED_MSG
        expected = PROTO_SENSOR_STARTED_MSG.format(
            sensor_name=self.real_log_instance.name,
            host=self.host,
            frequency=self.mocked_time_interval
        )
        with self.assertLogs(self.class_name, logging.WARNING) as cm:
            self.real_log_instance(MagicMock())
        self.assertIn(expected, cm.output[0])

    def test_name_is_property(self):
        self.mocked_name.reset_mock()
        self.instance.name
        self.mocked_name.assert_called_once_with()

    def test_host_cutoffs_hostname_after_first_dot(self):
        del self.instance._host
        with patch("fructosa.sensors.gethostname") as pgethostname:
            pgethostname.return_value = self.host
            self.assertEqual(self.instance.host, self.host.split(".")[0])


class PeriodicSensorTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import PeriodicSensor
        self.test_class = PeriodicSensor
        super().setUp()
        
    def test_is_subclass_of_Sensor(self):
        from fructosa.sensors import Sensor
        self.assertTrue(issubclass(self.test_class, Sensor))

    def test_call_is_a_coroutine(self):
        from inspect import iscoroutinefunction
        self.assertTrue(iscoroutinefunction(self.test_class.__call__))

    def test_instance_has_a_measure_method(self):
        self.instance.measure()

    @patch("fructosa.sensors.asyncio.sleep", new=AsyncioMock())
    @patch("fructosa.sensors.PeriodicSensor.measure")
    @patch("fructosa.sensors.Sensor.__call__")
    def test_measure_called(self, sensor_call, measure):
        queue = MagicMock()
        queue.put = AsyncioMock()
        for num in 3,6,2:
            measurements = [MagicMock() for _ in range(num)] + [InventedException()]
            measure.side_effect = measurements
            with self.assertRaises(InventedException):
                asyncio_run(self.instance(queue))
            expected_calls = [call() for _ in measurements[:-1]]
            measure.assert_has_calls(expected_calls)
            measure.reset_mock()
            
    @patch("fructosa.sensors.asyncio.sleep", new=AsyncioMock())
    @patch("fructosa.sensors.PeriodicSensor.measure")
    @patch("fructosa.sensors.Sensor.__call__")
    def test_call_calls_Sensor_call(self, sensorcall, measure):
        measure.side_effect = [MagicMock(), InventedException()]
        queue = MagicMock()
        queue.put = AsyncioMock()
        with self.assertRaises(InventedException):
            asyncio_run(self.instance(queue))
        sensorcall.assert_called_once_with(queue)

    @patch("fructosa.sensors.asyncio.sleep", new=AsyncioMock())
    @patch("fructosa.sensors.time.time")
    @patch("fructosa.sensors.PeriodicSensor.measure")
    @patch("fructosa.sensors.Sensor.__call__")
    def test_call_method_calls_queue_put_with_result(self, sensor_call, measure, ptime):
        queue = MagicMock()
        queue.put = AsyncioMock()
        value = MagicMock()
        time_value = MagicMock()
        ptime.return_value = time_value
        measure.side_effect = [value, InventedException()]
        expected = {
            "sensor": self.instance.name,
            "host": self.instance.host,
            "time": time_value,
            "value": value
        }
        with self.assertRaises(InventedException):
            asyncio_run(self.instance(queue))
        queue.put.mock.assert_called_once_with(expected)

    @patch("fructosa.sensors.float")
    @patch("fructosa.sensors.asyncio.sleep", new=AsyncioMock())
    @patch("fructosa.sensors.PeriodicSensor.measure")
    @patch("fructosa.sensors.Sensor.__call__")
    def test_call_method_calls_asyncio_sleep_called(self, sensor_call, measure, pfloat):
        measure.side_effect = [MagicMock(), InventedException()]
        queue = MagicMock()
        queue.put = AsyncioMock()
        result = MagicMock()
        def float_result(v):
            if v == self.instance.time_interval:
                return result
            else:
                return MagicMock()
        pfloat.side_effect = float_result
        with self.assertRaises(InventedException):
            asyncio_run(self.instance(queue))
        from fructosa.sensors import asyncio
        asyncio.sleep.mock.assert_called_once_with(result)


class CPUPercentTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import CPUPercent
        self.test_class = CPUPercent
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.dict")
    @patch("fructosa.sensors.enumerate")
    @patch("fructosa.sensors.psutil.cpu_percent")
    def test_measure_calls_psutil_cpu_percent(self, pcpupercent, penumerate, pdict):
        result = MagicMock()
        enumerate_result = MagicMock()
        dict_result = MagicMock()
        pdict.return_value = dict_result
        penumerate.return_value = enumerate_result
        pcpupercent.return_value = result
        self.assertEqual(self.instance.measure(), dict_result)
        pcpupercent.assert_called_once_with(interval=None, percpu=True)
        penumerate.assert_called_once_with(result)
        pdict.assert_called_once_with(enumerate_result)
        

class VirtualMemoryTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import VirtualMemory
        self.test_class = VirtualMemory
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.psutil.virtual_memory")
    def test_measure_calls_psutil_virtual_memory(self, pvirtual_memory):
        result = MagicMock()
        pvirtual_memory.return_value = result
        self.assertEqual(self.instance.measure(), dict(result._asdict()))
        pvirtual_memory.assert_called_once_with()
        

class CPUTimesTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import CPUTimes
        self.test_class = CPUTimes
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.psutil.cpu_times")
    def test_measure_calls_psutil_cpu_times(self, patchedmethod):
        result = MagicMock()
        patchedmethod.return_value = result
        self.assertEqual(self.instance.measure(), dict(result._asdict()))
        patchedmethod.assert_called_once_with()
        

class CPUTimesPercentTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import CPUTimesPercent
        self.test_class = CPUTimesPercent
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.psutil.cpu_times_percent")
    def test_measure_calls_psutil_cpu_times_percent(self, patchedmethod):
        result = MagicMock()
        patchedmethod.return_value = result
        self.assertEqual(self.instance.measure(), dict(result._asdict()))
        patchedmethod.assert_called_once_with()
        

class CPUCountTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import CPUCount
        self.test_class = CPUCount
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.psutil.cpu_count")
    def test_measure_calls_psutil_cpu_count(self, patchedmethod):
        result = MagicMock()
        patchedmethod.return_value = result
        self.assertEqual(self.instance.measure(), result)
        patchedmethod.assert_called_once_with()
        

class CPUStatsTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import CPUStats
        self.test_class = CPUStats
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.psutil.cpu_stats")
    def test_measure_calls_psutil_cpu_stats(self, patchedmethod):
        result = MagicMock()
        patchedmethod.return_value = result
        self.assertEqual(self.instance.measure(), dict(result._asdict()))
        patchedmethod.assert_called_once_with()
        

class CPUFreqTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import CPUFreq
        self.test_class = CPUFreq
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.psutil.cpu_freq")
    def test_measure_calls_psutil_cpu_freq(self, patchedmethod):
        result = MagicMock()
        patchedmethod.return_value = result
        self.assertEqual(self.instance.measure(), dict(result._asdict()))
        patchedmethod.assert_called_once_with()
        

class SwapMemoryTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import SwapMemory
        self.test_class = SwapMemory
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.psutil.swap_memory")
    def test_measure_calls_psutil_swap_memory(self, patchedmethod):
        result = MagicMock()
        patchedmethod.return_value = result
        self.assertEqual(self.instance.measure(), dict(result._asdict()))
        patchedmethod.assert_called_once_with()
        

class DiskPartitionsTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import DiskPartitions
        self.test_class = DiskPartitions
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.psutil.disk_partitions")
    def test_measure_calls_psutil_disk_partitions(self, patchedmethod):
        result = [MagicMock() for _ in range(4)]
        patchedmethod.return_value = result
        self.assertEqual(self.instance.measure(), [dict(_._asdict()) for _ in result])
        patchedmethod.assert_called_once_with()
        

class DiskUsageTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import DiskUsage
        self.test_class = DiskUsage
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.psutil.disk_usage")
    def test_measure_calls_psutil_disk_usage(self, patchedmethod):
        result = MagicMock()
        patchedmethod.return_value = result
        self.assertEqual(self.instance.measure(), dict(result._asdict()))
        patchedmethod.assert_called_once_with("/")
        

class DiskIOCountersTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import DiskIOCounters
        self.test_class = DiskIOCounters
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.psutil.disk_io_counters")
    def test_measure_calls_psutil_disk_io_counters(self, patchedmethod):
        result = MagicMock()
        patchedmethod.return_value = result
        self.assertEqual(self.instance.measure(), dict(result._asdict()))
        patchedmethod.assert_called_once_with()
        

class NetIOCountersTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import NetIOCounters
        self.test_class = NetIOCounters
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.psutil.net_io_counters")
    def test_measure_calls_psutil_net_io_counters(self, patchedmethod):
        result = MagicMock()
        patchedmethod.return_value = result
        self.assertEqual(self.instance.measure(), dict(result._asdict()))
        patchedmethod.assert_called_once_with()
        

class NetConnectionsTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import NetConnections
        self.test_class = NetConnections
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    # @patch("fructosa.sensors.psutil.net_connections")
    # def test_measure_calls_psutil_net_connections(self, patchedmethod):
    #     for num in 3, 5, 1:
    #         result = [MagicMock() for _ in range(num)]
    #         patchedmethod.return_value = result
    #         self.assertEqual(
    #             self.instance.measure(), [dict(r._asdict()) for r in result]
    #         )
    #         patchedmethod.assert_called_once_with()
    #         patchedmethod.reset_mock()

    @patch("fructosa.sensors.psutil.net_connections")
    def test_measure_calls_psutil_net_connections(self, mock_net_connections):
        from psutil._common import sconn, addr
        from socket import AddressFamily, SocketKind
        conn1 = {
            "fd": 34,
            "family": AddressFamily(7),
            "type": SocketKind(2),
            "laddr": addr(ip='192.168.0.11', port=55878),
            "raddr": (),
            "status": "ESTABLISHED",
            "pid": 345,
        }
        conn2 = {
            "fd": 5,
            "family": AddressFamily(4),
            "type": SocketKind(1),
            "laddr": addr(ip='192.168.0.40', port=5802),
            "raddr": addr(ip='127.0.0.2', port=3123),
            "status": "NONE",
            "pid": 3336,
        }
        out_conn1 = conn1.copy()
        out_conn2 = conn2.copy()
        for out_conn in out_conn1, out_conn2:
            out_conn["family"] = repr(out_conn["family"])
            out_conn["type"] = repr(out_conn["type"])
            out_conn["laddr"] = dict(out_conn["laddr"]._asdict())
            try:
                out_conn["raddr"] = dict(out_conn["raddr"]._asdict())
            except AttributeError:
                pass
            
        conns = [sconn(**conn1), sconn(**conn2)]
        mock_net_connections.return_value = conns
        expected = [out_conn1, out_conn2]
        
        result = self.instance.measure()
        
        mock_net_connections.assert_called_once_with()
        self.assertEqual(result, expected)
        

class NetIFAddrsTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import NetIFAddrs
        self.test_class = NetIFAddrs
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    # @patch("fructosa.sensors.psutil.net_if_addrs")
    # def test_measure_calls_psutil_net_if_addrs(self, patchedmethod):
    #     for numk, numi in (2,2) ,(5,1):
    #         result = {
    #             MagicMock(): [MagicMock() for i in range(numi)] for k in range(numk)
    #         }
    #         patchedmethod.return_value = result
    #         expected = {k: [dict(vi._asdict()) for vi in v] for k,v in result.items()}
    #         self.assertEqual(self.instance.measure(), expected)
    #         patchedmethod.assert_called_once_with()
    #         patchedmethod.reset_mock()
        
    @patch("fructosa.sensors.psutil.net_if_addrs")
    def test_measure_returns_result_from_net_if_addrs(self, mock_net_if_addrs):
        try:
            from psutil._common import snic
        except ImportError:
            from psutil._common import snicaddr as snic
        from socket import AddressFamily
        addr_dicts = [
            {"family": AddressFamily(3),
             "address": "127.20.79.72",
             "netmask": "255.255.255.0",
             "broadcast": "172.20.127.255",
             "ptp": None,
            },
            {"family": AddressFamily(2),
             "address": "192.2.145.11",
             "netmask": "255.255.255.0",
             "broadcast": "192.2.145.255",
             "ptp": None,
            },
            {"family": AddressFamily(10),
             "address": '2001:41b8:83c:fb01::1007',
             "netmask": 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff',
             "broadcast": None,
             "ptp": None,
            },            
        ]
        addrs = [snic(**d) for d in addr_dicts]
        sensor_result = {"lo": addrs[:1], "eth0": addrs[1:]}
        mock_net_if_addrs.return_value = sensor_result
        pre_expected = [d.copy() for d in addr_dicts]
        for d in pre_expected:
            d["family"] = repr(d["family"])
        expected = {"lo": pre_expected[:1], "eth0": pre_expected[1:]}
        result = self.instance.measure()
        self.assertEqual(result, expected)
    
        
class NetIFStatsTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import NetIFStats
        self.test_class = NetIFStats
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    # @patch("fructosa.sensors.psutil.dict")
    # @patch("fructosa.sensors.psutil.net_if_stats")
    # def test_measure_calls_psutil_net_if_stats(self, patchedmethod, mock_dict):
    #     for num in 2,7,1:
    #         result = {MagicMock(): MagicMock() for i in range(num)}
    #         for value in result.values():
    #             value._asdict.__getitem__.return_value = MagicMock()
    #             #res_value = MagicMock()
    #             #res_value.__getitem__.return_value = MagicMock()
    #         mock_dict.__getitem__.return_value = MagicMock()
    #         patchedmethod.items.return_value = result
    #         expected = {k: dict(v._asdict()) for k,v in result.items()}
    #         self.assertEqual(self.instance.measure(), expected)
    #         patchedmethod.assert_called_once_with()
    #         patchedmethod.reset_mock()

    @patch("fructosa.sensors.psutil.net_if_stats")
    def test_sensor_result_duplex_key_is_string(self, mock_net_if_stats):
        import psutil
        net_if_stats_as_dict = {
            'docker0': {
                'isup': True,
                'duplex': psutil._common.NicDuplex(0),
                'speed': 0,
                'mtu': 1500
            },
            'wlan0': {
                'isup': False,
                'duplex': psutil._common.NicDuplex(1),
                'speed': 0,
                'mtu': 1500
            },
            'eth0': {
                'isup': True,
                'duplex': psutil._common.NicDuplex(2),
                'speed': 65535,
                'mtu': 1500
            },
        }
        from collections import namedtuple
        snicstats = namedtuple("snicstats", net_if_stats_as_dict["eth0"].keys())
        net_if_stats_result = {k: snicstats(**v) for k, v in net_if_stats_as_dict.items()}

        mock_net_if_stats.return_value = net_if_stats_result
        
        expected = {k: v.copy() for k, v in net_if_stats_as_dict.items()}
        for k in expected.keys():
            expected[k]["duplex"] = repr(expected[k]["duplex"])
        mock_net_if_stats.return_value = net_if_stats_result

        result = self.instance.measure()
        
        mock_net_if_stats.assert_called_once_with()
        self.assertEqual(result, expected)
                
            
class SensorsTemperaturesTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import SensorsTemperatures
        self.test_class = SensorsTemperatures
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.psutil.sensors_temperatures")
    def test_measure_calls_psutil_sensors_temperatures(self, patchedmethod):
        for numk, numi in (2,1) ,(2,2):
            result = {
                MagicMock(): [MagicMock() for i in range(numi)] for k in range(numk)
            }
            patchedmethod.return_value = result
            expected = {k: [dict(vi._asdict()) for vi in v] for k,v in result.items()}
            self.assertEqual(self.instance.measure(), expected)
            patchedmethod.assert_called_once_with()
            patchedmethod.reset_mock()
                

class SensorsFansTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import SensorsFans
        self.test_class = SensorsFans
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.psutil.sensors_fans")
    def test_measure_calls_psutil_sensors_fans(self, patchedmethod):
        for numk, numi in (3,1) ,(2,2):
            result = {MagicMock(): [MagicMock() for i in range(numi)] for k in range(numk)}
            patchedmethod.return_value = result
            expected = {k: [dict(vi._asdict()) for vi in v] for k,v in result.items()}
            self.assertEqual(self.instance.measure(), expected)
            patchedmethod.assert_called_once_with()
            patchedmethod.reset_mock()


class SensorsBatteryTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import SensorsBattery
        self.test_class = SensorsBattery
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.dict")
    @patch("fructosa.sensors.psutil.sensors_battery")
    def test_measure_calls_psutil_sensors_battery(self, mock_sensors_battery, mock_dict):
        sensor_result = MagicMock()
        mock_sensors_battery.return_value = sensor_result
        result = MagicMock()
        def dict_side_effect(arg):
            if arg == sensor_result._asdict():
                return result
        result.__getitem__.return_value = MagicMock()
        #mock_dict.return_value = result
        mock_dict.side_effect = dict_side_effect
        self.assertEqual(self.instance.measure(), result)
        #patchedmethod.return_value = result
        #self.assertEqual(self.instance.measure(), dict(result._asdict()))
        mock_sensors_battery.assert_called_once_with()
        
    @patch("fructosa.sensors.psutil.sensors_battery")
    def test_secsleft_in_result_is_string_if_battery_not_unplugged(
            self, mock_sensors_battery):
        from psutil._common import sbattery
        from psutil import POWER_TIME_UNLIMITED, POWER_TIME_UNKNOWN
        for in_secsleft, out_secsleft in (
                (POWER_TIME_UNLIMITED, repr(POWER_TIME_UNLIMITED)),
                (POWER_TIME_UNKNOWN, repr(POWER_TIME_UNKNOWN))):
            sensor_dict = {
                'percent': 81.89123528312464,
                'secsleft': in_secsleft,
                'power_plugged': True,
            }
            sensor_result = sbattery(**sensor_dict)
            expected = sensor_dict.copy()
            expected["secsleft"] = out_secsleft
            mock_sensors_battery.return_value = sensor_result
            
            self.assertEqual(self.instance.measure(), expected)
        
    @patch("fructosa.sensors.psutil.sensors_battery")
    def test_result_is_None_if_no_battery(
            self, mock_sensors_battery):
        expected = None
        mock_sensors_battery.return_value = expected
        measurement = self.instance.measure()
        self.assertEqual(expected, measurement)

        
class BootTimeTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import BootTime
        self.test_class = BootTime
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.psutil.boot_time")
    def test_measure_calls_psutil_boot_time(self, patchedmethod):
        result = MagicMock()
        patchedmethod.return_value = result
        self.assertEqual(self.instance.measure(), result)
        patchedmethod.assert_called_once_with()
        

class UsersTestCase(SensorTestCaseBase):
    def setUp(self):
        from fructosa.sensors import Users
        self.test_class = Users
        super().setUp()
        
    def test_is_subclass_of_PeriodicSensor(self):
        from fructosa.sensors import PeriodicSensor
        self.assertTrue(issubclass(self.test_class, PeriodicSensor))

    @patch("fructosa.sensors.psutil.users")
    def test_measure_calls_psutil_users(self, patchedmethod):
        for num in 6, 2, 3:
            result = [MagicMock() for _ in range(num)]
            patchedmethod.return_value = result
            self.assertEqual(self.instance.measure(), [dict(r._asdict()) for r in result])
            patchedmethod.assert_called_once_with()
            patchedmethod.reset_mock()
        

if __name__ == "__main__":
    unittest.main()
