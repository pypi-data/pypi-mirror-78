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

import subprocess as sp
import psutil
import os

from fructosa.constants import FRUCTOSAD_PROGRAM, LAGENT_PROGRAM, LMASTER_PROGRAM

from tests.functional.environment import DOCKER_FT_ENVIRONMENT, LOCALHOST_FT_ENVIRONMENT


def _is_process_running_in_docker_container(process):
    """The answer is based on whether the process has 'dockerd' as one of its ancestors.
    The function can accept a psutil.Process instance; process can also be None."""
    names = []
    while True:
        try:
            names.append(process.name())
            process = process.parent()
        except AttributeError:
            break
    if "dockerd" in names:
        return True
    else:
        return False

def get_NSpid(pid):
    """It returns the pid of the process in the innermost namespace it belongs to
    (which is rightmost element in the NSpid line of /proc/{pid}/status)."""
    with open("/proc/{}/status".format(pid)) as f:
        lines = f.readlines()
    for l in lines:
        if l.startswith("NSpid"):
            return int(l.strip().split()[-1])
    
    
class ProgramWrapper:
    def __init__(self, exe=None, execution_timeout=10, pidfile=None):
        self._args = ()
        if exe is None:
            exe = self.default_exe
        self.exe = exe
        self.execution_timeout = execution_timeout
        self.test_conf = None
        self.standard_conf = None
        self.pidfile = pidfile
        self.exit_code = None

    @property
    def pidfile(self):
        return os.path.join(self._piddir, self._pid_file_name)

    @pidfile.setter
    def pidfile(self, value):
        head, tail = os.path.split(value)
        self._piddir = head
        self._pid_file_name = tail
        
    @property
    def args(self):
        value = self._args
        self._args = ()
        return value

    @args.setter
    def args(self, new_value):
        self._args = new_value
    
    @property
    def name(self):
        return self.exe

    def full_command_line(self, *arguments):
        if len(arguments) == 0:
            arguments = self.args
        return (self.exe,) + arguments
            
    def __call__(self, *arguments, timeout=None, pre_exe=()):
        executable_with_arguments = pre_exe + self.full_command_line(*arguments)
        proc = sp.Popen(
            executable_with_arguments,
            stdout=sp.PIPE,
            stderr=sp.PIPE)
        if timeout:
            timeout = timeout
        else:
            timeout = self.execution_timeout
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
        except sp.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
        result = {
            "returncode": proc.returncode, "stdout": stdout, "stderr": stderr
        }
        self.exit_code = result["returncode"]
        return result
        
    def _find_process_instance_excluding_docker(self):
        """Checks if the process is running in the local host. If it's found to
        be running inside a docker container, it is ignored."""
        self_process = None
        for process in psutil.process_iter():
            if process.name() == os.path.basename(self.exe):
                if not _is_process_running_in_docker_container(process):
                    self_process = process
                    break
        return self_process

    def _find_process_instance(self):
        """Checks if the process is running in the local host, regardless of which
        environement is running on (directly on the localhost or inside a
        container)."""
        self_process = None
        for process in psutil.process_iter():
            if process.name() == os.path.basename(self.exe):
                self_process = process
                break
        return self_process

    def find_process_instance_in_environment(self, environment):
        """Checks if the process is running in the given environment
        (localhost or docker).
        If a process is a zombie, I don't consider it a running process.
        The method also sets a new attribute in the resulting found process:
        NSpid, see 'get_NSpid'."""
        self_process = None
        for process in psutil.process_iter():
            if process.name() == os.path.basename(self.exe) and process.status() != "zombie":
                running_in_docker = _is_process_running_in_docker_container(process)
                if running_in_docker:
                    running_environment = DOCKER_FT_ENVIRONMENT
                else:
                    running_environment =  LOCALHOST_FT_ENVIRONMENT
                if running_environment == environment:
                    self_process = process
                    self_process.NSpid = get_NSpid(process.pid)
                    break
        return self_process

        
class FrUCToSADWrapper(ProgramWrapper):
    default_exe = FRUCTOSAD_PROGRAM

    def help(self):
        return self("--help")
    
    def start(self):
        return self("start")

    def stop(self):
        return self("stop")

            
class LAgentWrapper(FrUCToSADWrapper):
    default_exe = LAGENT_PROGRAM


class LMasterWrapper(FrUCToSADWrapper):
    default_exe = LMASTER_PROGRAM

