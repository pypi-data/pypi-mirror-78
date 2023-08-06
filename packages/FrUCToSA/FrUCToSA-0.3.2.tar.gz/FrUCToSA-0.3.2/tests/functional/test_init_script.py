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
import psutil
import time
import os

from tests.common.logs import LogParser
#from tests.common.constants import FRUCTOSAD_PROCESS_NAME#, FRUCTOSAD_LOCK_FILE_NAME


class StartStopTest(unittest.TestCase):
    def setUp(self):
        cwd = os.path.dirname(__file__)
        conf_file = os.path.join(cwd, "..", "data", "fructosa.conf")
        conf_file = os.path.normpath(conf_file)
        self.read_fructosa_conf(conf_file)
        from tests.common.init import InitScript
        self.fructosa_init_script = InitScript(non_default_conf_file=conf_file)
        self.syslog_parser = LogParser(
            "/var/log/syslog",
            id_strings=(FRUCTOSAD_PROCESS_NAME,))
        # self.initial_syslog_lines = self.syslog_parser.get_lines(
        #     FRUCTOSAD_PROCESS_NAME
        # )

    def read_fructosa_conf(self, conf_file):
        from configparser import ConfigParser
        cfg = ConfigParser()
        section_header = ["[fructosad]\n"]
        with open(conf_file) as conff:
            conf_contents = conff.readlines()
        conf_str = ''.join(section_header + conf_contents)
        cfg.read_string(conf_str)
        self.fructosa_config = cfg
        
    def find_fructosad(self):
        fructosad_process = None
        for process in psutil.process_iter():
            if process.name() == FRUCTOSAD_PROCESS_NAME:
                fructosad_process = process
                break
        return fructosad_process

    def find_fructosad_PID_from_lock_file(self):
        #lock_file_name = FRUCTOSAD_LOCK_FILE_NAME
        from fructosa.global_conf import FRUCTOSAD_PIDFILE_VAR
        lock_file_name = self.fructosa_config.get("fructosad", FRUCTOSAD_PIDFILE_VAR)
        if os.path.exists(lock_file_name):
            with open(lock_file_name) as lock_file:
                pid_full = lock_file.read().strip()
            pid = int(pid_full)
        else:
            pid = None
        return pid

    
@unittest.skip
class BasicFructosadFunctionalityTest(StartStopTest):
    def test_fructosa_start_stop(self):
        #  Tux is one of our system administrators. He is testing the new
        # cluster perfromance tool written by one of the local hpc-support 
        # fellows.
        #  Tux likes the Unix philosophy. Well, "likes" is not very precise. 
        # He *loves* Unix. Of course, he assumes that this new tool 
        # fulfils his expectations for daemons. To start with, he checks 
        # that the fructosad daemon is not running before launching it:
        fructosad_process = self.find_fructosad()
        if fructosad_process:
            self.fail("'fructosad' process found before starting! Stop it and "\
                      "come back to test.")
        #  Fine, now he can start testing this new promising tool!
        # For that, he launches the "fructosa" init script:
        self.fructosa_init_script.start()
        # and as a consequence, he expects to find a running process 
        # named properly:
        time.sleep(0.5)#need a bit of sleep to catch the process
        fructosad_process = self.find_fructosad()
        if not fructosad_process:
            self.fail("No 'fructosad' process found!")
        # He also expects the creation of a lock file with the PID in it:
        found_pid = self.find_fructosad_PID_from_lock_file()
        # which agrees with the PID of the process:
        self.assertEqual(found_pid, fructosad_process.pid)
        #  At this point, he wants to check what happens with the logs. 
        # And he checks with satisfaction that the start event is 
        # registered in the system log. First a line informing that the 
        # daemon is starting is found. Second, he also finds a line 
        # claiming that the daemon started (he understands, it means that
        # the process of starting the daemon concluded):
        new_log_entries = self.syslog_parser.get_new_lines()
        string_marks_msg = "'{0}' and '{1}' not found in the same log file line"
        string_marks_list = [
            (FRUCTOSAD_PROCESS_NAME, "starting"),
            (FRUCTOSAD_PROCESS_NAME, "started"),
        ]
        for string_marks in string_marks_list:
            for log_line in new_log_entries:
                if string_marks[0] in log_line and string_marks[1] in log_line:
                    break
            else:
                self.fail(string_marks_msg.format(*string_marks))
        #  Of course, at the same time he checks that there is no message 
        # in the log file informing that the daemon stopped
        string_marks_msg = "'{0}' and '{1}' found in the same log file line!"
        string_marks_list = [
            (FRUCTOSAD_PROCESS_NAME, "stopped"),
        ]
        for string_marks in string_marks_list:
            for log_line in new_log_entries:
                if string_marks[0] in log_line and string_marks[1] in log_line:
                    self.fail(string_marks_msg.format(*string_marks))
        # To conclude this first tour, only one thing is missing, namely that
        # issuing the "stop" command:
        self.fructosa_init_script.stop(wait=6)
        # effectively kills "fructosad"
        fructosad_process = self.find_fructosad()
        self.assertIs(fructosad_process, None)
        # ...and the software registers that event in the system log:
        new_log_entries = self.syslog_parser.get_new()
        string_marks_msg = "'{0}' and '{1}' not found in the same log file line"
        string_marks_list = [
            (FRUCTOSAD_PROCESS_NAME, "stopping"),
            (FRUCTOSAD_PROCESS_NAME, "stopped"),
        ]
        for string_marks in string_marks_list:
            for log_line in new_log_entries:
                if string_marks[0] in log_line and string_marks[1] in log_line:
                    break
            else:
                self.fail(string_marks_msg.format(*string_marks))
        # that concludes the first test he makes to the functionality of the 
        # new monitoring program.
        
    def test_right_fructosa_config_is_read_when_init_script_starts(self):
        #  When the fructosa script starts, it is reported what options are found 
        # in the configuration file 
        self.fail("implement it! (WIP): fructosa.conf")
        # check for FRUCTOSAD_CONF, FRUCTOSAD_PIDFILE, ...
        
    def test_fructosa_does_not_start_if_host_mismatch(self):
        fail_message = "Move it to the fructosad test: The 'host' read in "\
          "the conf file must agree with hostname"
        self.fail(fail_message)
