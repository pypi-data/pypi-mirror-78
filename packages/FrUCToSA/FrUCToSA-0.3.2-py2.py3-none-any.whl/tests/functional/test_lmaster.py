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
import os
import time
import socket
import shutil
from functools import reduce

from tests.common.program import LMasterWrapper, LAgentWrapper
from tests.functional.base_start_stop import BaseStartStop
from tests.functional.test_lagent import BaseLAgent
from tests.functional.environment import (
    LOCALHOST_FT_ENVIRONMENT, DOCKER_FT_ENVIRONMENT, 
)
from fructosa.constants import (
    LMASTER_DESCRIPTION, CONF_READ_MSG, LMASTER_DEFAULT_CONFIGFILE,
    LAGENT_DEFAULT_CONFIGFILE, PROTO_SENSOR_STARTED_MSG, LMASTER_DEFAULT_CONFIGFILE,
    PROTO_MEASUREMENT_RECEIVED_MSG, PROTO_INVALID_SENSOR_MSG,
    HEARTBEAT_RECEIVE_MSG_TEMPLATE, HEARTBEAT_LISTENING_MSG_TEMPLATE,
    HEARTBEAT_PORT
)
from fructosa.lmaster import LMASTER_STARTING_MESSAGE, LMASTER_STOP_MESSAGE
from fructosa.conf import LMASTER_DEFAULT_PIDFILE, LAGENT_DEFAULT_PIDFILE

import fructosa


class LMasterFunctionalityDefaultConfTest(BaseStartStop, BaseLAgent, unittest.TestCase):
    def setUp(self):
        self.wrapper_class = LMasterWrapper
        self.program_starting_msg = LMASTER_STARTING_MESSAGE
        self.program_stop_msg = LMASTER_STOP_MESSAGE
        self.program_default_pidfile = LMASTER_DEFAULT_PIDFILE
        self.program_description = LMASTER_DESCRIPTION
        self.program_conf_read_msg = CONF_READ_MSG.format(
            config_file=LMASTER_DEFAULT_CONFIGFILE
        )
        self.program_default_configfile = LMASTER_DEFAULT_CONFIGFILE
        super().setUp()

    def test_lmaster_receives_heartbeats_from_lagent(self):
        #  Tux has wants to check that lmaster and lagent can communicate.
        # So, he prepares configurations files for lmaster and lagent:
        lagent = LAgentWrapper(pidfile=LAGENT_DEFAULT_PIDFILE)
        if self.ft_env.name == LOCALHOST_FT_ENVIRONMENT:
            lagent_config_file_name = "lagent-test.0.conf"
            lmaster_config_file_name = "lmaster.0.conf"
        elif self.ft_env.name == DOCKER_FT_ENVIRONMENT:
            lagent_config_file_name = "lagent-test.0.docker.conf"
            lmaster_config_file_name = "lmaster.0.docker.conf"
        lagent_conf = self.prepare_config_from_file(
            lagent_config_file_name,
            default_configfile=LAGENT_DEFAULT_CONFIGFILE,
            program=lagent,
        )
        #self.prepare_sensors(lagent_conf)
        lmaster_conf = self.prepare_config_from_file(lmaster_config_file_name)
        listeining_to_heartbeats = HEARTBEAT_LISTENING_MSG_TEMPLATE.format(
            master=lmaster_conf["lmaster"]["host"],
            hb_port=HEARTBEAT_PORT,
        )
        heartbeat_received = HEARTBEAT_RECEIVE_MSG_TEMPLATE.format(
            host="quaco", message_number=0,
        )[11:]#just cut the "random" initial part
        self.setup_logparser(
            target_strings=(listeining_to_heartbeats, heartbeat_received,)
        )
        old_lines = self.tmplogparser.get_new_lines()
        old_lines_summary = self.tmplogparser._line_counting_history[-1]
        #and he launches lmaster and lagent:
        self.program.args = ("start",)
        lagent.args = ("start",)
        programs = (self.program, lagent)
        with self.ft_env(*programs) as start_lmaster_lagent:
            # Immediately he sees that the first heartbeat signal has arrived 
            # and is reported in the logs:
            self.wait_for_environment(30)
            new_lines = self.tmplogparser.get_new_lines()
            new_lines_summary = self.tmplogparser._line_counting_history[-1]
            self.assertTrue(len(new_lines) > 0)
            #  He finds in the logs a message claiming that the program is listening
            # to heartbeats:
            self.assertEqual(
                old_lines_summary[1][listeining_to_heartbeats]+1,
                new_lines_summary[1][listeining_to_heartbeats]
            )
            # and also a message saying that the first heartbeat arrived!
            self.assertEqual(
                old_lines_summary[1][heartbeat_received]+1,
                new_lines_summary[1][heartbeat_received]
            )            
        # This was very satisfying!
        # He stops lagent:
    # and lmaster:

    @unittest.skip
    def test_lmaster_receives_data_from_lagent(self):
        # For version 0.3.0, this FT is removed because the data goes directly
        # from lagent to graphite.
        #  Before it used to go from lagent to lmaster and then to graphite
        #  (DPalao, 9/6/2020)
        # ---
        #  Tux has wants to check that lmaster and lagent can communicate.
        # So, he prepares configurations files for lmaster and lagent:
        lagent = LAgentWrapper(pidfile=LAGENT_DEFAULT_PIDFILE)
        if self.ft_env.name == LOCALHOST_FT_ENVIRONMENT:
            lagent_config_file_name = "lagent-test.1.conf"
            lmaster_config_file_name = "lmaster.1.conf"
        elif self.ft_env.name == DOCKER_FT_ENVIRONMENT:
            lagent_config_file_name = "lagent-test.1.docker.conf"
            lmaster_config_file_name = "lmaster.1.docker.conf"
        lagent_conf = self.prepare_config_from_file(
            lagent_config_file_name, default_configfile=LAGENT_DEFAULT_CONFIGFILE, program=lagent,
        )
        self.prepare_sensors(lagent_conf)
        lmaster_conf = self.prepare_config_from_file(lmaster_config_file_name)
        #and he launches lmaster and lagent:
        self.program.args = ("start",)
        lagent.args = ("start",)
        programs = (self.program, lagent)
        ## I need to remove some spaces and one ":" to be able to identify lines
        measurament_received = PROTO_MEASUREMENT_RECEIVED_MSG.format("", "")
        measurament_received = measurament_received.strip().strip(":").strip()
        self.setup_logparser(target_strings=(measurament_received,))
        old_lines = self.tmplogparser.get_new_lines()
        with self.ft_env(*programs) as start_lmaster_lagent:
            # Now he waits some seconds to check that the measuraments are indeed correctly
            # reported in the logs, *as received messages*:
            wait_t = 10*max([float(v["frequency"]) for k,v in self.sensors.items()])
            self.wait_for_environment(wait_t)
            new_lines = self.tmplogparser.get_new_lines()
            self.assertTrue(len(new_lines) > 0)
            for line in new_lines:
                values = [k in line for k in self.sensors]
                self.assertTrue(reduce(lambda x,y: x or y, values))
                self.assertIn("DEBUG", line)
                self.assertIn("LMaster", line)
        # This was very satisfying!
        # He stops lagent:
    # and lmaster:

    @unittest.skip
    def test_lmaster_custom_logging(self):
        #
        # This must be moved to base!!!
        #
        #  Tux wants to explore better the options that he can customize for logging.
        # He learned that he can set the values for maxBytes, backupCount and level.
        #  He creates now a config file with maxBytes and backupCount:
        lagent = LAgentWrapper(pidfile=LAGENT_DEFAULT_PIDFILE)
        if self.ft_env.name == LOCALHOST_FT_ENVIRONMENT:
            lagent_config_file_name = "lagent-test.1.conf"
            lmaster_config_file_name = "lmaster.1.conf"
        elif self.ft_env.name == DOCKER_FT_ENVIRONMENT:
            lagent_config_file_name = "lagent-test.1.docker.conf"
            lmaster_config_file_name = "lmaster.1.docker.conf"
        lagent_conf = self.prepare_config_from_file(
            lagent_config_file_name, default_configfile=LAGENT_DEFAULT_CONFIGFILE, program=lagent,
        )
        self.prepare_sensors(lagent_conf)
        lmaster_conf = self.prepare_config_from_file(lmaster_config_file_name)
        #and he launches lmaster and lagent:
        self.program.args = ("start",)
        lagent.args = ("start",)
        programs = (self.program, lagent)
        ## I need to remove some spaces and one ":" to be able to identify lines
        measurament_received = PROTO_MEASUREMENT_RECEIVED_MSG.format("", "")
        measurament_received = measurament_received.strip().strip(":").strip()
        self.setup_logparser(target_strings=(measurament_received,))
        old_lines = self.tmplogparser.get_new_lines()
        with self.ft_env(*programs) as start_lmaster_lagent:
            # Now he waits some seconds to check that the measuraments are indeed correctly
            # reported in the logs, *as received messages*:
            wait_t = 2.1*max([float(v["frequency"]) for k,v in self.sensors.items()])
            self.wait_for_environment(wait_t)
            new_lines = self.tmplogparser.get_new_lines()
            self.assertTrue(len(new_lines) > 0)
            for line in new_lines:
                values = [k in line for k in self.sensors]
                self.assertTrue(reduce(lambda x,y: x or y, values))
                self.assertIn("DEBUG", line)
                self.assertIn("LMaster", line)
