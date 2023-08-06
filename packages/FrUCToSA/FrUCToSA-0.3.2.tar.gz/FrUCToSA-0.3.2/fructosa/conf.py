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

import os
import argparse
import configparser

from .logs import setup_logging
from .sensors import sensor_factory
from .ui.cl import CLConf

from .constants import (
    DEFAULT_PID_DIR, DEFAULT_PROTO_PIDFILE, ACTION_STR, ACTION_HELP, ACTION_CHOICES,
    PIDFILE_OPTION_ALIASES, PIDFILE_HELP, PIDFILE_STR,
    FRUCTOSAD_PROGRAM, FRUCTOSAD_DESCRIPTION, FRUCTOSAD_DEFAULT_CONFIGFILE, 
    LAGENT_PROGRAM, LAGENT_DESCRIPTION, LAGENT_DEFAULT_CONFIGFILE,
    CONFIGFILE_STR, CONF_READ_MSG, PROTO_INVALID_SENSOR_MSG,
    LMASTER_PROGRAM, LMASTER_DESCRIPTION, LMASTER_DEFAULT_CONFIGFILE,
    LMASTER_HOST, LMASTER_HOST_KEY,
    LAGENT_TO_LMASTER_DATA_PORT, LAGENT_TO_LMASTER_DATA_PORT_KEY,
    GRAPHITE_HOST, GRAPHITE_HOST_KEY, GRAPHITE_CARBON_RECEIVER_PICKLE_PORT,
    GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY, GRAPHITE_SECTION,
    OWN_LOG_FILE_KEY, DEFAULT_OWN_FILE_LOGGING_PATH,
    OWN_LOG_LEVEL_KEY, DEFAULT_OWN_FILE_LOGGER_LEVEL,
    OWN_LOG_MAXBYTES_KEY, OWN_LOG_SECTION, OWN_LOG_BACKUPCOUNT_KEY,
    OWN_LOG_MAXBYTES_TYPE, OWN_LOG_BACKUPCOUNT_TYPE, 
    CONFIGFILE_STR, CONFIGFILE_OPTION_ALIASES, CONFIGFILE_HELP,
)


FRUCTOSAD_DEFAULT_PIDFILE = os.path.join(
    DEFAULT_PID_DIR, DEFAULT_PROTO_PIDFILE.format(program=FRUCTOSAD_PROGRAM)
)
LAGENT_DEFAULT_PIDFILE = os.path.join(
    DEFAULT_PID_DIR, DEFAULT_PROTO_PIDFILE.format(program=LAGENT_PROGRAM)
)
LMASTER_DEFAULT_PIDFILE = os.path.join(
    DEFAULT_PID_DIR, DEFAULT_PROTO_PIDFILE.format(program=LMASTER_PROGRAM)
)

ACTION_ARGUMENT = (
    ACTION_STR,
    ((ACTION_STR,), dict(help=ACTION_HELP, choices=ACTION_CHOICES)),
)
PIDFILE_ARGUMENT = (
    PIDFILE_STR,
    (PIDFILE_OPTION_ALIASES, dict(help=PIDFILE_HELP, dest=PIDFILE_STR))
)
CONFIGFILE_ARGUMENT = (
    CONFIGFILE_STR,
    (CONFIGFILE_OPTION_ALIASES, dict(help=CONFIGFILE_HELP, dest=CONFIGFILE_STR))
)


class FructosaDConf:
    description = FRUCTOSAD_DESCRIPTION
    default_values = {
        PIDFILE_STR: FRUCTOSAD_DEFAULT_PIDFILE,
        CONFIGFILE_STR: FRUCTOSAD_DEFAULT_CONFIGFILE
    }
    arguments = (ACTION_ARGUMENT, PIDFILE_ARGUMENT, CONFIGFILE_ARGUMENT)
    
    def __init__(self, argv=None):
        self._get_conf_from_command_line()
        self._set_config_file()
        self._get_conf_from_config_file()
        self._prepare_logging()
        self._post_process_configuration()

    def _get_conf_from_command_line(self):
        self._command_line_conf = CLConf(
            description=self.description,
            arguments=self.arguments,
            defaults=self.default_values,
        )

    def _set_config_file(self):
        self._config_file = self[CONFIGFILE_STR]#self.default_values[CONFIGFILE_STR]
    
    def _get_conf_from_config_file(self):
        self._create_config_parser()
        self._parse_config_file()

    def _prepare_logging(self):
        self._logging_from_config_file()
        self.logger = setup_logging(
            logger_name=self.__class__.__name__,
            rotatingfile_conf=self.logging
        )
    
    def _create_config_parser(self):
        self._config_file_conf = configparser.ConfigParser()

    def _parse_config_file(self):
        self._config_file_conf.read(self._config_file)

    def _post_process_configuration(self):
        """To be extended:
        Once the logging facilities are setup other parts of the configuration can be
        processed."""
        # To extend it, see "LAgentConf._post_process_configuration"
        self.logger.info(CONF_READ_MSG.format(config_file=self._config_file))
        try:
            with open(self._config_file) as conf_contents:
                for config_line in conf_contents.readlines():
                    self.logger.info(" ... {}".format(config_line.rstrip("\n")))
        except OSError:#if there is no file, I don't need to report its contents
            pass
        self._lmaster_from_config_file()

    def _lmaster_from_config_file(self):
        self.lmaster = {
            LMASTER_HOST_KEY: LMASTER_HOST,
            LAGENT_TO_LMASTER_DATA_PORT_KEY: LAGENT_TO_LMASTER_DATA_PORT,
        }
        try:
            self.lmaster.update(self._config_file_conf[LMASTER_PROGRAM])
        except KeyError:
            pass

    def _logging_from_config_file(self):
        valid_keys = (
            OWN_LOG_FILE_KEY, OWN_LOG_LEVEL_KEY,
            OWN_LOG_MAXBYTES_KEY, OWN_LOG_BACKUPCOUNT_KEY
        )
        self.logging = {
            OWN_LOG_FILE_KEY: DEFAULT_OWN_FILE_LOGGING_PATH,
            OWN_LOG_LEVEL_KEY: DEFAULT_OWN_FILE_LOGGER_LEVEL,
        }
        for key in valid_keys:
            try:
                value = self._config_file_conf[OWN_LOG_SECTION][key]
            except KeyError:
                pass
            else:
                if key == OWN_LOG_MAXBYTES_KEY:
                    value = OWN_LOG_MAXBYTES_TYPE(value)
                elif key == OWN_LOG_BACKUPCOUNT_KEY:
                    value = OWN_LOG_BACKUPCOUNT_TYPE(value)
                self.logging[key] = value

    def __getitem__(self, key):
        return self._command_line_conf[key]


class LAgentConf(FructosaDConf):
    description = LAGENT_DESCRIPTION
    default_values = {
        PIDFILE_STR: LAGENT_DEFAULT_PIDFILE,
        CONFIGFILE_STR: LAGENT_DEFAULT_CONFIGFILE
    }
    
    def _post_process_configuration(self):
        super()._post_process_configuration()
        self._sensors_from_config_file_sections()
        self._graphite_from_config_file()
        
    def _graphite_from_config_file(self):
        self.graphite = {
            GRAPHITE_HOST_KEY: GRAPHITE_HOST,
            GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY: GRAPHITE_CARBON_RECEIVER_PICKLE_PORT,
        }
        try:
            self.graphite.update(self._config_file_conf[GRAPHITE_SECTION])
        except KeyError:
            pass

    def _sensors_from_config_file_sections(self):
        # In the future, sensors should be a property, maybe dynamically generated
        self.sensors = []
        sections = self._config_file_conf.sections()
        for section in sections:
            sensor = self._make_sensor_from_section(section)
            if sensor:
                self.sensors.append(sensor)

    def _make_sensor_from_section(self, section):
        splitted_section = section.partition(":")
        sensor = None
        if splitted_section[0] == "sensor":
            sensor_name = splitted_section[2]
            options = self._config_file_conf[section]
            try:
                sensor = sensor_factory(sensor_name, options, self.logging)
            except NameError:
                self.logger.error(PROTO_INVALID_SENSOR_MSG.format(sensor_name=sensor_name))
        return sensor

        
class LMasterConf(FructosaDConf):
    description = LMASTER_DESCRIPTION
    default_values = {
        PIDFILE_STR: LMASTER_DEFAULT_PIDFILE,
        CONFIGFILE_STR: LMASTER_DEFAULT_CONFIGFILE
    }

    def _post_process_configuration(self):
        super()._post_process_configuration()
    
