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

"""This module contains code to start some services using docker-compose.
It has been devised to be used within the functional tests for FrUCToSA.
"""

import time
import os
#import multiprocessing as mp
import subprocess as sp
import sys
from contextlib import contextmanager
import io
from operator import attrgetter
from contextlib import redirect_stderr

from compose.cli.main import TopLevelCommand, project_from_options, compute_service_exit_code
from compose.cli.log_printer import LogPrinter, build_log_presenters
from compose.project import OneOffFilter

from urllib import request, parse


GENERAL_COMPOSE_OPTIONS = {
    "--no-deps": False,
    "--always-recreate-deps": False,
    "--abort-on-container-exit": False,
    "SERVICE": "",
    "--remove-orphans": False,
    "--no-recreate": True,
    "--force-recreate": False,
    "--build": False,
    "--no-build": False,
    "--scale": "",
    "--no-color": False,
    "--rmi": "none",
    "--detach": True,
    "--volumes": True,
    "--quiet": True,
    "--services": False,
}

# @contextmanager
# def redirect_std_streams(stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
#     temp_std_stuff = stdin, stdout, stderr
#     original_std_stuff = sys.stdin, sys.stdout, sys.stderr
#     sys.stdin, sys.stdout, sys.stderr = temp_std_stuff
#     yield
#     sys.stdin, sys.stdout, sys.stderr = original_std_stuff

    
class FTDocker:
    """This class is an interface to docker through docker-compose. It can create
    and manipulate a set of services by means of the docker-compose API.
    """
    
    def __init__(self, yml_dir):
        self._output = io.StringIO()
        self.path_to_yml_dir = yml_dir
        self.options = GENERAL_COMPOSE_OPTIONS
        self.project = project_from_options(self.path_to_yml_dir, self.options)
        self._cmd = TopLevelCommand(self.project)

    def _up(self):
        self._cmd.up(self.options)

    @property
    def output(self):
        return self._output.getvalue()
    
    def up(self):
        self._up()
        #self._proc = mp.Process(target=self._up)
        #self._proc.daemon = True
        #self._proc.start()

    def down(self):
        self._cmd.down(self.options)
        try:
            pass#self._proc.join()
        except AttributeError:
            pass

    def stop(self):
        self._cmd.stop(self.options)
        
    def ps(self):
        return [_.name for _ in self.project.services]

    def ids(self, *services):
        containers = sorted(
            self.project.containers(service_names=services, stopped=True) +
            self.project.containers(service_names=services, one_off=OneOffFilter.only),
            key=attrgetter('name')
        )
        return [container.id for container in containers]

    def get_logs(self, to_file=None):
        """Show output from containers.
        """
        containers = self._cmd.project.containers(service_names=self.options['SERVICE'], stopped=True)
        tail = None
        log_args = {
            'follow': False,
            'tail': None,
            'timestamps': False
        }
        with redirect_stderr(self._output):
            LogPrinter(
                containers,
                build_log_presenters(self._cmd.project.service_names, self.options['--no-color']),
                event_stream=self._cmd.project.events(service_names=self.options['SERVICE']),
                output=self._output,
                log_args=log_args,
            ).run()

    def get_output(self):
        options = {"--tail": None, '--follow': False, '--timestamps': False, '--no-color': True}
        options.update(self.options)
        #with redirect_std_streams(stdout=self._output, stderr=self._output):
        backup, sys.stdout = sys.stdout, self._output
        self._cmd.logs(options)
        
    def wait_until_running(self, step_timeout=1):
        while True:
            containers = self._cmd.project.containers()
            if not containers:
                time.sleep(step_timeout)
            else:
                #print("Container is", containers[0].human_readable_state)
                if containers[0].is_running:
                    # Sometimes the status is Up, but some time is still needed:
                    time.sleep(step_timeout)
                    break

    def exit_code(self, service):
        return compute_service_exit_code(service, self._cmd.project.containers(stopped=True))
    

def get_id_of_container(container_name):
    cmd = ["docker", "ps", "--filter", f'"name={container_name}"', "--format", '"{{.ID}}"']
    p = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
    stdout = p.output.decode()
    return stdout.split("\n")
    
