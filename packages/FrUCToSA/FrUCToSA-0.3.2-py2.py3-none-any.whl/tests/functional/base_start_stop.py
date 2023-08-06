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

import time
import os
import shutil
import configparser
import unittest
import tempfile
import logging
import itertools

from tests.common.logs import LogParser
from tests.functional.environment import (
    FTEnvironment, DOCKER_FT_ENVIRONMENT, LOCALHOST_FT_ENVIRONMENT,
    FRUCTOSA_FT_ENVIRONMENT_VAR, DEFAULT_FRUCTOSA_FT_ENVIRONMENT,
)

from fructosa.constants import (
    DEFAULT_OWN_FILE_LOGGING_PATH, DEFAULT_PID_DIR, PROTO_NO_PERMISSION_PIDFILE,
    PIDFILE_EXISTS, PROCESS_DOES_NOT_EXIST, NO_PID_FOUND, PROTO_CANT_STOP_MSG,
    NOT_RUNNING_MESSAGE, PIDFILE_ACTION_CREATED, INVALID_PID, PIDFILE_NOT_FOUND,
    ALREADY_RUNNING_MSG, RUNNING_PROCESS_FOUND, CANNOT_USE_LOG_HANDLER,
    OWN_LOG_SECTION, OWN_LOG_FILE_KEY, CONF_READ_MSG, 
    OWN_LOG_MAXBYTES_KEY, OWN_LOG_BACKUPCOUNT_KEY, OWN_LOG_LEVEL_KEY, 
)


def get_unused_pid():
    with open("/proc/sys/kernel/pid_max") as f:
        max_pid = int(f.read().strip())
    pids = []
    for proc_element in os.listdir("/proc"):
        try:
            pid = int(proc_element)
        except ValueError:
            continue
        pids.append(pid)
    candidate = max(pids)+23
    while True:
        candidate = candidate % max_pid
        if candidate not in pids:
            return candidate
        candidate += 17

def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ...
    (taken from the docs)."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


class BaseStartStop:
    _SINGLE_PROGRAM = True
    _WITH_GRAPHITE = False
    
    def setUp(self):
        if self._SINGLE_PROGRAM:
            self.single_program_setUp()
        self.setUp_ft_env()
        # ...O, he almost forgets that he has to make a backup of any preexisting
        # config file:
        self.backup_configs = {}
        if self.ft_env.name == LOCALHOST_FT_ENVIRONMENT:
            self.backup_preexisting_config_files()

    def single_program_setUp(self):
        self.program = self.wrapper_class(pidfile=self.program_default_pidfile)
        self.program.configfile = self.program_default_configfile
        
    def backup_preexisting_config_files(self):
        self.backup_preexisting_config_file()

    def backup_preexisting_config_file(self, config_file_name=None):
        if config_file_name is None:
            config_file_name = self.program_default_configfile
        if os.path.exists(config_file_name):
            backup_name = config_file_name+".back"
            shutil.move(config_file_name, backup_name)
            self.backup_configs[config_file_name] = backup_name

    def setUp_ft_env(self):
        ftenv_type = os.getenv(FRUCTOSA_FT_ENVIRONMENT_VAR, default=DEFAULT_FRUCTOSA_FT_ENVIRONMENT)
        self.ft_env = FTEnvironment(
            ftenv_type, DEFAULT_OWN_FILE_LOGGING_PATH, DEFAULT_PID_DIR,
            with_graphite=self._WITH_GRAPHITE
        )
        
    def tearDown(self):
        #self.tearDown_ft_env()#needed?
        # before leaving, he restores the original --if any-- config files:
        if self.ft_env.name == LOCALHOST_FT_ENVIRONMENT:
            self.restore_preexisting_config_files()

    def restore_preexisting_config_files(self):
        for original_name, backup_name in self.backup_configs.items():
            if os.path.exists(original_name):
                os.remove(original_name)
            if os.path.exists(backup_name):
                shutil.move(backup_name, original_name)

    def setup_logparser(self, target_strings=None, additional_logs=0):
        if not target_strings:
            target_strings = (
                self.program_starting_msg,
                self.program_stop_msg,
                self.program_conf_read_msg
            )
        # This is only done once, not per program, because each FT tests --for now-- from
        # the point of view of one program:
        self.tmplogparser = LogParser(self.ft_env.log_file_name, id_strings=target_strings)
        # For rotating logs, the next attribute can be used as a temporary hack:
        self.all_logparsers = [self.tmplogparser]
        for idx in range(additional_logs):
            self.all_logparsers.append(
                LogParser(self.ft_env.log_file_name+f".{idx+1}", id_strings=target_strings)
            )
        
    def check_program_running(self, program):
        program_process = program.find_process_instance_in_environment(self.ft_env.name)
        if program_process:
            msg = ("'{program}' process found before starting! Stop it and come back "
                   "to test.")
            msg = msg.format(program=program.default_exe)
            self.fail(msg)

    def _make_test_conf_file_name(self, config_file_name):
        """This stupid method is a two lines op that was factorized out from its former
        location (prepare_config_from_file) to make it usable from other places"""
        cwd = os.path.dirname(__file__)
        return os.path.join(cwd, "data", config_file_name)
        

    def prepare_config_from_file(self, config_file_name, default_configfile=None, program=None):
        """Helper method to be used by subclasses.
        
        It takes a config file from the data dir (config_file_name) and uses it
        as the program's config file.

        *Don't need to do backup* of the configuration: the setUp method should do it!
        """
        if program is None:
            program = self.program
        test_conf_file_name = self._make_test_conf_file_name(config_file_name)
        if default_configfile is None:
            program.standard_conf = self.program_default_configfile
        else:
            program.standard_conf = default_configfile
        # The following happens now inside the environment:
        #shutil.copyfile(test_conf_file_name, self.standard_conf_file_name)
        # ...if I do:
        program.test_conf = test_conf_file_name
        conf = configparser.ConfigParser()
        conf.read(test_conf_file_name)
        return conf

    def wait_for_environment(self, delta=0):
        if self.ft_env.name == DOCKER_FT_ENVIRONMENT:
            wait_t = 5
        else:
            wait_t = 0.2
        time.sleep(wait_t+delta)
        
    def test_program_starts_and_stops(self):
        #  Tux is one of our system administrators. He is testing the new
        # cluster perfromance tool written by one of the local hpc-support 
        # fellows.
        #  Tux likes the Unix philosophy. Well, "likes" is not very precise. 
        # He *loves* Unix. Of course, he assumes that this new tool 
        # fulfils his expectations for services. To start with, he checks 
        # that ``{program}`` is not running before launching it:
        if self.ft_env.name == LOCALHOST_FT_ENVIRONMENT:
            #  I check only in a so-called local environment because inside a new
            # container we don't need to check if the program runs: 
            self.check_program_running(self.program)
            #ft_env.check_program_running(program_name)#new
            
        #  Fine, now he can start testing this new promising tool!
        # Of course, it is mandatory to read the help message:
        #help_msg = program.help()
        programs = (self.program,)
        self.program.args = ("--help",)
        with self.ft_env(*programs) as help_command:#new
            self.wait_for_environment()
            help_msg = help_command.output
            # and he checks that a description message is displayed:
            self.assertIn(
                self.program_description.replace("\n", " "),
                str(help_msg.replace("\n", " "))
            )
        
        # Now he is ready to play around with the program.
        self.setup_logparser()
        #  1) inside containers, there must be a shared volume
        #  2) in a local environment, I have to simple define the right attribute inside the env
        old_lines_summary = self.tmplogparser._line_counting_history[-1]
        # For that, he launches the "{program}" program with "{program} start":
        #program.start()
        self.program.args = ("start",)
        with self.ft_env(*programs) as start_command:
            # and as a consequence, he expects to find a running process 
            # named properly:
            self.wait_for_environment()#need a bit of sleep to catch the process
            program_process = self.program.find_process_instance_in_environment(self.ft_env.name)
            if not program_process:
                self.fail("No '{program}' process found!".format(program=self.program.name))
            # He also expects to find a PID file with the correct PID in it:
            pid1 = program_process.NSpid
            pid2 = int(open(self.program.pidfile).read().strip())
            self.assertEqual(pid1, pid2)
            # Now, he checks the logs:
            # there must be a message announcing that {program} has started in the logs:
            new_lines = self.tmplogparser.get_new_lines()
            new_lines_summary = self.tmplogparser._line_counting_history[-1]
            self.assertEqual(
                old_lines_summary[1][self.program_starting_msg]+1,
                new_lines_summary[1][self.program_starting_msg]
            )
            # The logs also report about the configuration that has been read.
            # The first thing is a message announcing that the conf has been read:
            self.assertEqual(
                old_lines_summary[1][self.program_conf_read_msg]+1,
                new_lines_summary[1][self.program_conf_read_msg]
            )
            # To conclude this first tour, only one thing is missing, namely that
            # issuing the "stop" command ("{program} stop"):
            #  (done implicitly by environment.FTEnvironment.__exit__)
            ## ft_env.stop()
            # effectively kills "{program}"
        program_process = self.program.find_process_instance_in_environment(self.ft_env.name)
        self.assertIs(program_process, None)
        # and it is correctly reported in the logs:
        new_lines = self.tmplogparser.get_new_lines()
        new_lines_summary = self.tmplogparser._line_counting_history[-1]
        self.assertEqual(
            old_lines_summary[1][self.program_stop_msg]+1,
            new_lines_summary[1][self.program_stop_msg]
        )
        # that concludes the first test he makes to the functionality of the 
        # new monitoring program.


    def check_output_and_log_simple_cmd(
            self, programs, log_msgs=None, screen_msgs=None, old_lines_summary=None,
            wait_t=0, inside_environment=None,
            pre_inside_environment=lambda:None):
        with self.ft_env(*programs) as command:
            self.wait_for_environment(wait_t)
            if inside_environment:
                pre_inside_environment()
                self.ft_env.run_in_container(*inside_environment)
            if screen_msgs:
                error_msg = command.output
                # For instance, he finds a nice and descriptive error message
                for err_msg in screen_msgs:
                    self.assertIn(err_msg, str(error_msg))
            if log_msgs:
                # the logs also report a proper message:
                new_lines = self.tmplogparser.get_new_lines()
                new_lines_summary = self.tmplogparser._line_counting_history[-1]
                for err_msg in log_msgs:
                    try:
                        old_ntimes = old_lines_summary[1][err_msg]
                    except KeyError:
                        old_ntimes = 0
                    try:
                        new_ntimes = new_lines_summary[1][err_msg]
                    except KeyError:
                        new_ntimes = 0
                    self.assertEqual(old_ntimes+1,new_ntimes)
                    
    def test_error_behaviour_of_pidfile_functionality(self):
        ##############################################################
        #
        #  In this test, a bit more of cleaning wouldn't hurt... ;-)
        #
        ##############################################################
        #
        #  Tux wants to check the behaviour of the program with regard to the pidfile.
        # He assumes that if if starts the program twice, there must be an error
        # if both instances want to use the same pidfile:
        programs = (self.program,)
        self.program.args = ("start",)
        screen_msgs =[ALREADY_RUNNING_MSG]
        log_msgs = screen_msgs + [
            PIDFILE_EXISTS.format(pidfile=self.program_default_pidfile),
        ]
        another_program = self.wrapper_class(pidfile=self.program_default_pidfile)
        another_program.configfile = self.program_default_configfile
        another_program.args = ("start",)
        def pre_inside_environment():
            another_program.pidfile = self.program.pidfile
            pid = open(another_program.pidfile).read().strip()
            new_log_line = RUNNING_PROCESS_FOUND.format(pid=pid)
            log_msgs.append(new_log_line)
            self.tmplogparser._id_strings.append(new_log_line)
            #self.tmplogparser.count_lines()
        inside_environment = (another_program, self.program.name)                        
        self.setup_logparser(target_strings=log_msgs)
        old_lines_summary = self.tmplogparser._line_counting_history[-1]
        self.check_output_and_log_simple_cmd(
            programs, log_msgs, screen_msgs, old_lines_summary,
            inside_environment=inside_environment,
            pre_inside_environment=pre_inside_environment,
            #wait_t=10,
        )
        #  Moreover, what he considers extremely important is the exit code of the program,
        # which he expects to be different from zero:
        exit_code = another_program.exit_code
        self.assertNotEqual(exit_code, 0)

        # So far so good.
        #  But, there is a caveat. Something Tux wants to pay attention to: what
        # happens if the pidfile cannot be created? An error should be printed
        # out otherwise the user would not know it!

        # So he wants to test this. First, he wants to check that an error
        # is displayed if there is no permission to write on the chosen directory:
        self.program.args = ("start",)
        os.chmod(self.ft_env.pid_dir, 0o000)
        self.ft_env.docker_user = "1000:1000"
        pidfile = os.path.join(
            self.ft_env.original_pid_dir, self.program_default_pidfile
        )
        error_msgs_screen =(
            PROTO_NO_PERMISSION_PIDFILE.format(
                pidfile=pidfile, action=PIDFILE_ACTION_CREATED),
        )
        error_msgs_logs = (f"Permission denied: '{pidfile}'",)+error_msgs_screen
        self.setup_logparser(target_strings=error_msgs_logs)
        old_lines_summary = self.tmplogparser._line_counting_history[-1]
        try:
            self.check_output_and_log_simple_cmd(
                programs, error_msgs_logs, error_msgs_screen, old_lines_summary, wait_t=5)
        finally:
            os.chmod(self.ft_env.pid_dir, 0o777)
            self.ft_env.docker_user = None#for other tests
        #  Moreover, what he considers extremely important is the exit code of the program,
        # which he expects to be different from zero:
        exit_code = self.program.exit_code
        self.assertNotEqual(exit_code, 0)

        #  Now he wants to check what happens if there is already a file with
        # the same name as the pidfile.
        #  It would be great if the program handles this properly.
        # Tux wonders what happens if the pidfile exists, but it does not contain
        # a PID OR if the PID exists with a PID, but no process is found:
        pidfile_name = "/tmp/my.pid"
        program_args = ("-p", pidfile_name, "start")
        unused_pid = get_unused_pid()
        log_msgs_list = [
            (ALREADY_RUNNING_MSG, PIDFILE_EXISTS.format(pidfile=pidfile_name), NO_PID_FOUND),
            (ALREADY_RUNNING_MSG, PIDFILE_EXISTS.format(pidfile=pidfile_name),
             PROCESS_DOES_NOT_EXIST.format(pid=unused_pid)),
        ]
        screen_msgs_list = [
            (ALREADY_RUNNING_MSG,),
            (ALREADY_RUNNING_MSG,),
        ]
        pidfile_contents_list = ["", unused_pid]
        self.ft_env.setup_pid_dir("/tmp", 0o755)
        pidfile_name = os.path.join(self.ft_env.pid_dir, "my.pid")
        for log_msgs, screen_msgs, pidfile_contents in zip(
                log_msgs_list, screen_msgs_list, pidfile_contents_list):
            self.program.args = program_args
            self.setup_logparser(target_strings=log_msgs)
            old_lines_summary = self.tmplogparser._line_counting_history[-1]
            try:
                with open(pidfile_name, "w") as pidfile:
                    print(pidfile_contents, file=pidfile)
                self.check_output_and_log_simple_cmd(programs, log_msgs, screen_msgs, old_lines_summary)
            finally:
                pidfile.close()
                os.unlink(pidfile_name)
            #  Moreover, what he considers extremely important is the exit code of the program,
            # which he expects to be different from zero:
            exit_code = self.program.exit_code
            self.assertNotEqual(exit_code, 0)
        self.ft_env.setup_pid_dir(DEFAULT_PID_DIR, 0o755)

        # For completeness, Tux wants to ensure that if the stop command  and
        # the -p option with a wrong pidfile (ie, with wrong contents) are given,
        cant_stop_message = PROTO_CANT_STOP_MSG.format(program=self.program.name)
        wrong_pids = ("wrong pid in here", "929284748329832", get_unused_pid())
        error_templates = (INVALID_PID, INVALID_PID, PROCESS_DOES_NOT_EXIST)
        for wrong_pid, error_template in zip(wrong_pids, error_templates):
            pidfile_name = "/tmp/wrong.pid"
            self.program.args = ("-p", pidfile_name, "stop")# .args is consummed every time
            log_msgs = (
                "{}: {}".format(cant_stop_message, error_template.format(pid=wrong_pid)), 
            )
            self.ft_env.setup_pid_dir("/tmp", 0o755)
            self.setup_logparser(target_strings=log_msgs)
            old_lines_summary = self.tmplogparser._line_counting_history[-1]
            try:
                pidfile_name = os.path.join(self.ft_env.pid_dir, "wrong.pid")
                with open(pidfile_name, "w") as pidfile:
                    print(wrong_pid, file=pidfile)
                # ... he gets a proper behaviour (without crashes):
                self.check_output_and_log_simple_cmd(programs, log_msgs, log_msgs, old_lines_summary)
            finally:
                pidfile.close()
                os.unlink(pidfile_name)
                self.ft_env.setup_pid_dir(DEFAULT_PID_DIR, 0o755)
            #  Moreover, what he considers extremely important is the exit code of the program,
            # which he expects to be different from zero:
            exit_code = self.program.exit_code
            self.assertNotEqual(exit_code, 0)
        #  And last, what happens if the stop command is issued and
        # the -p option with a pidfile that does not exist?
        cant_stop_message = PROTO_CANT_STOP_MSG.format(program=self.program.name)
        pidfile_name = "/tmp/_does_not_exist.pid"
        try:
            os.unlink(pidfile_name)
        except FileNotFoundError:
            pass
        self.program.args = ("-p", pidfile_name, "stop")# .args is consummed every time
        error_msgs = (
            "{}: {}".format(cant_stop_message, PIDFILE_NOT_FOUND.format(pidfile=pidfile_name)), 
        )
        self.setup_logparser(target_strings=error_msgs)
        old_lines_summary = self.tmplogparser._line_counting_history[-1]
        pidfile_name = os.path.join(self.ft_env.pid_dir, "_does_not_exist.pid")
        # ... he gets a proper behaviour (without crashes):
        self.check_output_and_log_simple_cmd(programs, error_msgs, error_msgs, old_lines_summary)
        #  Moreover, what he considers extremely important is the exit code of the program,
        # which he expects to be different from zero:
        exit_code = self.program.exit_code
        self.assertNotEqual(exit_code, 0)

    def test_logging_section_of_config_file_basic(self):
        #  Now that Tux is putting his hands on this nice software, he wants to
        # explore more possibilities.
        #  For example, can the software run as a normal user?
        # He tries it.
        #delete_log = ProgramWrapper("rm")
        #delete_log.args = ("/var/log/fructosa.log",)
        #print("log_file_name:", self.ft_env.log_file_name)
        #os.unlink(self.ft_env.log_file_name)
        os.chmod(self.ft_env.log_file_name, 0o000)
        self.ft_env.docker_user = "1000:1000"
        programs = (self.program,)
        self.program.args = ("start",)
        # he notices (there is a descriptive error message) that, by default, he cannot
        screen_msgs =[CANNOT_USE_LOG_HANDLER.format(target=self.ft_env.original_log_file_name)]
        self.check_output_and_log_simple_cmd(programs, screen_msgs=screen_msgs)#, wait_t=50)
        # (the exit code of the program is here be different from zero too):
        exit_code = self.program.exit_code
        self.assertNotEqual(exit_code, 0)
        os.chmod(self.ft_env.log_file_name, 0o644)
        #  But he learned that he can set the log file path in the configuration file
        conf_file = "logging-test.1.conf"
        conf = self.prepare_config_from_file(conf_file)
        log_filename = conf[OWN_LOG_SECTION][OWN_LOG_FILE_KEY]
        #open(log_filename, "w").close()# want to clean it...
        #self.ft_env.log_file_name = log_filename
        self.ft_env.prepare_logging(os.path.basename(log_filename), log_filename)
        starting_msg = self.program_starting_msg
        self.setup_logparser(target_strings=(starting_msg,))
        old_lines_summary = self.tmplogparser._line_counting_history[-1]
        # and, he launches again the program:
        self.program.args = ("-p", "/tmp/chirimoya.pid", "start",)
        programs = (self.program,)
        try:
            with self.ft_env(*programs) as start_command:
                self.wait_for_environment(1)
                new_lines = self.tmplogparser.get_new_lines()
                new_lines_summary = self.tmplogparser._line_counting_history[-1]
                # He finds in the right log file a message saying that the program started!
                self.assertEqual(
                    old_lines_summary[1][starting_msg]+1,
                    new_lines_summary[1][starting_msg]
                )
        finally:
            try:
                os.unlink(log_filename)
            except FileNotFoundError:
                pass
        self.ft_env.docker_user = None# restore user in ft_env

    def test_logging_section_of_config_file_more_details(self):
        # But wait a second. There are more options to customize the behaviour of the logging.
        # First off, he prepares a new conf file with more logging options 
        conf_file = f"logging-test.{self.program.name}.conf"
        conf = self.prepare_config_from_file(conf_file)
        log_filename = conf[OWN_LOG_SECTION][OWN_LOG_FILE_KEY]
        log_max_bytes = int(conf[OWN_LOG_SECTION][OWN_LOG_MAXBYTES_KEY])
        log_backup_count = int(conf[OWN_LOG_SECTION][OWN_LOG_BACKUPCOUNT_KEY])
        level = conf[OWN_LOG_SECTION][OWN_LOG_LEVEL_KEY]
        try:
            level = int(level)
        except ValueError:
            level = getattr(logging, level)
        all_levels = ("CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG")
        smaller_levels = [l for l in all_levels if getattr(logging, l) < level]
        self.ft_env.rotating_logs = log_backup_count
        self.ft_env.docker_bind_log_volumes = False
        self.ft_env.prepare_logging(os.path.basename(log_filename), log_filename)
        self.setup_logparser(target_strings=("",), additional_logs=log_backup_count)
        old_lines_summary = self.tmplogparser._line_counting_history[-1]
        # and, he launches again the program:
        self.program.args = ("start",)
        programs = (self.program,)
        with self.ft_env(*programs) as start_command:
            self.wait_for_environment(1)
            all_logs = self.ft_env.output
            all_logs_lines = all_logs.split("\n")
            print(all_logs_lines)
            # He confirms that all the files have been used for logging
            lines_where_logfile_name_appears = []
            for log_name in self.ft_env.original_log_file_names:
                self.assertIn(log_name, all_logs)
                log_name_line = f"==> {log_name} <=="
                lines_where_logfile_name_appears.append(all_logs_lines.index(log_name_line))
            lines_where_logfile_name_appears.sort()
            diffs = [b-a for a, b in pairwise(lines_where_logfile_name_appears)]
            # the container uses 'tail' to show the logs. The output format is:
            # ==> ca.log <==
            #dff
            #
            # ==> ca.log.1 <==
            #
            # ==> ca.log.2 <==
            #
            #  So to have non-empty files, the difference in the number of lines where
            # the '==> ... <==' strings occurs must be > 2:
            for delta in diffs:
                self.assertGreater(delta, 2)#if this happens, the 'tail' command prints something
            # and he doesn't see messages with log level smaller than the given one:
            for small in smaller_levels:
                self.assertNotIn(small, all_logs)
        # finally:
        #     try:
        #         os.unlink(log_filename)
        #     except FileNotFoundError:
        #         pass

    def test_configuration_read_is_reported_in_the_logs(self):
        # After preparing another conf file
        conf_file = "logging-test.1.conf"
        conf = self.prepare_config_from_file(conf_file)
        full_conf_file = self._make_test_conf_file_name(conf_file)
        with open(full_conf_file) as fconf:
            conf_literal_lines = [_.strip() for _ in fconf.readlines()]
        log_filename = conf[OWN_LOG_SECTION][OWN_LOG_FILE_KEY]
        self.ft_env.prepare_logging(os.path.basename(log_filename), log_filename)
        self.setup_logparser(target_strings=("",))
        old_lines_summary = self.tmplogparser._line_counting_history[-1]
        # he starts the program
        self.program.args = ("start",)
        programs = (self.program,)
        with self.ft_env(*programs) as start_command:
            self.wait_for_environment(1)
            new_lines = self.tmplogparser.get_new_lines()
            # and he sees, with satisfaction, the contents of the conf file in the logs:
            full_log = "".join(new_lines)
            for conf_line in conf_literal_lines:
                self.assertIn(" ... {}".format(conf_line), full_log)
                    
    def test_config_file_can_be_changed_from_command_line(self):
        #  For consistency, Tux wants to be able to change the path to the
        # configuration file. He sees in the help that there is an option for that:
        # -c, so he starts the program using that option
        conf_path = "/tmp/manchuria.conf"
        log_target = CONF_READ_MSG.format(config_file=conf_path)
        self.setup_logparser(target_strings=(log_target,))
        old_lines_summary = self.tmplogparser._line_counting_history[-1]
        self.program.args = ("-c", conf_path, "start",)
        programs = (self.program,)
        with self.ft_env(*programs) as start_command:
            self.wait_for_environment(10)
            new_lines = self.tmplogparser.get_new_lines()
            new_lines_summary = self.tmplogparser._line_counting_history[-1]
            # He finds in the right log file a message saying that the correct config
            # file has been read!
            self.assertEqual(
                old_lines_summary[1][log_target]+1,
                new_lines_summary[1][log_target]
            )


class MultiProgramBaseStartStop(BaseStartStop):
    _SINGLE_PROGRAM = False
    
    def backup_preexisting_config_files(self):
        for config_file in self.default_config_files:
            self.backup_preexisting_config_file(config_file)

    @unittest.skip
    def test_program_starts_and_stops(self):
        """I switch this off: each program must be tested separately"""
        pass
