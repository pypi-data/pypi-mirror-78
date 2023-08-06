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

"""This module defines the Sensor class, and subclasses as well as a factory function
that created sensor instances from names.
"""

from socket import gethostname
import asyncio
import time

from fructosa.logs import setup_logging
from fructosa.constants import PROTO_SENSOR_STARTED_MSG

import psutil


def sensor_factory(name, arguments, logging):
    """This is the typical factory function that creates an instance from a
    name of a class. If the name is not a vaild Sensor name, NameError is
    raised."""
    if _is_sensor(name):
        return _make_sensor(name, arguments, logging)
    else:
        raise NameError

def _is_sensor(name):
    """This function tells if there is a Sensor (sub class) with the given name."""
    if name in _find_all_sensors():
        result = True
    else:
        result = False
    return result

def old_find_all_sensors():
    """Searches dynamically for sensors in the current module"""
    all_items_in_module = globals()
    all_sensors = {
        name: obj for name, obj in all_items_in_module.items() if issubclass(obj, Sensor)
    }
    return all_sensors

def _find_all_sensors():
    """Searches dynamically for sensors in the current module"""
    all_items_in_module = globals()
    all_sensors = {}
    for name, obj in all_items_in_module.items():
        try:
            is_sensor = issubclass(obj, Sensor)
        except TypeError:
            continue
        if is_sensor:
            all_sensors[name] = obj
    return all_sensors

def _make_sensor(name, arguments, logging):
    """This function creates an instance of the Sensor subclass specified by the given name.
    It assumes that there is a sensor with that name."""
    all_sensors = _find_all_sensors()
    return all_sensors[name](logging, **arguments)


class Sensor:
    def __init__(self, logging, time_interval):
        self.time_interval = time_interval
        self._logger = setup_logging(logger_name=self.name, rotatingfile_conf=logging)

    @property
    def host(self):
        try:
            host = self._host
        except AttributeError:
            host = gethostname().split(".")[0]
            self._host = host
        return host
        
    @property
    def name(self):
        return self.__class__.__name__
    
    def __call__(self, output_queue):
        start_msg = PROTO_SENSOR_STARTED_MSG.format(
            sensor_name=self.__class__.__name__,
            host=self.host,
            frequency=self.time_interval
        )
        self._logger.warning(start_msg)


class PeriodicSensor(Sensor):
    async def __call__(self, output_queue):
        super().__call__(output_queue)
        result = {"host": self.host, "sensor": self.name}
        while True:
            result["value"] = self.measure()
            now = time.time()
            result["time"] = now
            await output_queue.put(result)
            await asyncio.sleep(float(self.time_interval))

    def measure(self):
        pass


class CPUPercent(PeriodicSensor):
    def measure(self):
        return dict(enumerate(psutil.cpu_percent(interval=None, percpu=True)))


class VirtualMemory(PeriodicSensor):
    def measure(self):
        return dict(psutil.virtual_memory()._asdict())


class CPUTimes(PeriodicSensor):
    def measure(self):
        return dict(psutil.cpu_times()._asdict())


class CPUTimesPercent(PeriodicSensor):
    def measure(self):
        return dict(psutil.cpu_times_percent()._asdict())


class CPUCount(PeriodicSensor):
    def measure(self):
        return psutil.cpu_count()


class CPUStats(PeriodicSensor):
    def measure(self):
        return dict(psutil.cpu_stats()._asdict())


class CPUFreq(PeriodicSensor):
    def measure(self):
        return dict(psutil.cpu_freq()._asdict())


class SwapMemory(PeriodicSensor):
    def measure(self):
        return dict(psutil.swap_memory()._asdict())


class DiskPartitions(PeriodicSensor):
    def measure(self):
        return [dict(_._asdict()) for _ in psutil.disk_partitions()]


class DiskUsage(PeriodicSensor):
    def measure(self):
        return dict(psutil.disk_usage("/")._asdict())# of course the "/" is temporary


class DiskIOCounters(PeriodicSensor):
    def measure(self):
        return dict(psutil.disk_io_counters()._asdict())


class NetIOCounters(PeriodicSensor):
    def measure(self):
        return dict(psutil.net_io_counters()._asdict())


class NetConnections(PeriodicSensor):
    def measure(self):
        result = [dict(_._asdict()) for _ in psutil.net_connections()]
        for k in result:
            for repr_item in "family", "type":
                k[repr_item] = repr(k[repr_item])
            for todict_item in "laddr", "raddr":
                try:
                    k[todict_item] = dict(k[todict_item]._asdict())
                except AttributeError:
                    pass
        return result


class NetIFAddrs(PeriodicSensor):
    def measure(self):
        result = {
            k: [dict(vi._asdict()) for vi in v] for k,v in psutil.net_if_addrs().items()
        }
        for k, v in result.items():
            for d in v:
                d["family"] = repr(d["family"])
        return result


class NetIFStats(PeriodicSensor):
    def measure(self):
        result = {k: dict(v._asdict()) for k, v in psutil.net_if_stats().items()}
        for k in result.keys():
            result[k]["duplex"] = repr(result[k]["duplex"])
        return result


class SensorsTemperatures(PeriodicSensor):
    def measure(self):
        return {k: [dict(vi._asdict()) for vi in v] for k,v in psutil.sensors_temperatures().items()}


class SensorsFans(PeriodicSensor):
    def measure(self):
        return {k: [dict(vi._asdict()) for vi in v] for k,v in psutil.sensors_fans().items()}


class SensorsBattery(PeriodicSensor):
    def measure(self):
        measurement = psutil.sensors_battery()
        if measurement is None:
            result = None
        else:
            result = dict(measurement._asdict())
            if result["power_plugged"] in (True, None):
                result["secsleft"] = repr(result["secsleft"])
        return result


class BootTime(PeriodicSensor):
    def measure(self):
        return psutil.boot_time()


class Users(PeriodicSensor):
    def measure(self):
        return [dict(_._asdict()) for _ in psutil.users()]


    
