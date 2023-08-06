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
import time
import psutil
import subprocess as sp

from fructosa.global_conf import FRUCTOSA_CONF_ENVIRON_VAR

class LinuxSystem:
    """A class which instances identify the underlying linux flavour."""
    id_files = {"/etc/gentoo-release": "gentoo"}
    
    def __init__(self):
        self.get_flavour()

    def get_flavour(self):
        for file_name in self.id_files.keys():
            if os.path.exists(file_name):
                self.flavour = self.id_files[file_name]
                break
        else:
            raise TypeError("The linux flavour is unknown")


class InitScript:
    script_names_dict = {
        "gentoo": "fructosa.openrc"
    }
    daemon_process_name = "fructosad"
    
    def __init__(self, script_dir=None, non_default_conf_file=None):
        if script_dir:
            self.script_dir = script_dir
        else:
            cwd = os.path.dirname(__file__)
            script_dir = os.path.join(cwd, "..", "..", "bin")
            self.script_dir = os.path.normpath(script_dir)
        self.create_script()
        self.non_default_conf_file = non_default_conf_file

    def run_command(self, cmd, env=None):
        return sp.Popen(
            [self.script_path, cmd], 
            stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, env=env,
        )

    def get_daemon_procs(self):
        iprocs = psutil.process_iter()
        procs = [
            proc for proc in iprocs if proc.name() == self.daemon_process_name
        ]
        self._daemon_procs = procs

    def environment_change_needed_to_start(self):
        if self.non_default_conf_file:
            need = True
        else:
            need = False
        return need
        
    def get_proper_environment(self):
        env = os.environ
        if self.environment_change_needed_to_start():
            env[FRUCTOSA_CONF_ENVIRON_VAR] = self.non_default_conf_file
        return env
        
    def start(self):
        env = self.get_proper_environment()
        # debug begins:
        print(env)
        if FRUCTOSA_CONF_ENVIRON_VAR in env:
            verb = "is"
        else:
            verb = "is not"
        print("{0} {1} in environment".format(FRUCTOSA_CONF_ENVIRON_VAR, verb))
        # debug ends.
        self._init_proc = self.run_command("start", env=env)
        # debug begins:
        print("%"*30)
        print(self._init_proc.stdout.read().decode())
        print("%"*30)
        print(self._init_proc.stderr.read().decode())
        print("%"*30)
        # debug ends.
        self.get_daemon_procs()
        #print(self._init_proc.stderr.read())

    def stop(self, wait=None):
        proc = self.run_command("stop")
        if wait:
            gone, alive = psutil.wait_procs(self._daemon_procs, timeout=wait)
            for p in alive:
                p.kill()
            #print(self._stop_proc.stdout.read())
            #print(self._stop_proc.stderr.read())

    def create_script(self):
        """A Factory Method to select the right InitScript 
        depending on the system we are running on."""
        local_linux = LinuxSystem()
        linux_flavour = local_linux.flavour
        self.script_path = os.path.join(
            self.script_dir,
            self.script_names_dict[linux_flavour]
        )
        
# class SysVInitScript(InitScript):
#     script_path = os.path.join("..", "..", "bin", "fructosa.upstart")


# class OpenRCInitScript(InitScript):
#     script_path = os.path.join("..", "..", "bin", "fructosa.openrc")


