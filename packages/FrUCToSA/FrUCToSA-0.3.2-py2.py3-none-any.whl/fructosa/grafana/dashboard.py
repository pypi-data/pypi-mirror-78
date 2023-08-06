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

import json
import copy
import configparser

from ..ui.cl import CLConf
from .node import node_template_dict, node_panels_template
from ..error_handling import handle_errors, FructosaError

from ..constants import (
    MAKE_DASHBOARD_DESCRIPTION, MAKE_DASHBOARD_HOSTS_HELP, HOSTS_FILE_STR,
    HOSTS_FILE_METAVAR, HOSTS_SECTION_STR, HOSTS_SECTION_SHORT_OPTION,
    HOSTS_SECTION_LONG_OPTION, HOSTS_SECTION_METAVAR, HOSTS_SECTION_HELP,
    MAKE_DASHBOARD_FILE_ERROR_MSG,
)


HOSTS_FILE_ARG = (
    HOSTS_FILE_STR,
    ((HOSTS_FILE_STR,),
         dict(help=MAKE_DASHBOARD_HOSTS_HELP, metavar=HOSTS_FILE_METAVAR))
)
HOSTS_SECTION_ARG = (
    HOSTS_SECTION_STR,
    ((HOSTS_SECTION_SHORT_OPTION, HOSTS_SECTION_LONG_OPTION),
         dict(
             help=HOSTS_SECTION_HELP,
             metavar=HOSTS_SECTION_METAVAR,
             default=HOSTS_FILE_STR
        )
    )
)


def _collect_hosts(file_name, section):
    conf = configparser.ConfigParser(allow_no_value=True)
    conf.read(file_name)
    return tuple(conf[section].keys())


def _render_dashboard_template(host):
    """It produces a dictionary defining a dashboard from an input host"""
    dashboard = copy.deepcopy(node_template_dict)
    dashboard["tags"].append(host)
    dashboard["title"] = dashboard["title"].format(hostname=host)
    dashboard["panels"] = copy.deepcopy(node_panels_template)
    for panel in dashboard["panels"]:
        try:
            targets = panel["targets"]
        except KeyError:
            pass
        else:
            for target in targets:
                target["target"] = target["target"].format(hostname=host)
        try:
            description = panel["description"]
        except KeyError:
            pass
        else:
            panel["description"] = description.format(hostname=host)
    return dashboard


def _write_dashboard(dashboard, filename_prefix):
    """Writes down the (implicitly) expected json serialized object
    to file with name 'filename_prefix.json'"""
    with open(filename_prefix+".json", "w") as f:
        f.write(dashboard)


@handle_errors
def make_dashboard():
    conf = CLConf(
        description=MAKE_DASHBOARD_DESCRIPTION,
        arguments=(HOSTS_FILE_ARG, HOSTS_SECTION_ARG)
    )
    try:
        hosts = _collect_hosts(conf[HOSTS_FILE_STR], conf[HOSTS_SECTION_STR])
    except KeyError as e:
        msg = MAKE_DASHBOARD_FILE_ERROR_MSG.format(
            hosts_file=conf[HOSTS_FILE_STR],
            hosts_section=conf[HOSTS_SECTION_STR]
        )
        raise FructosaError(msg)
    for host in hosts:
        dashboard_dict = _render_dashboard_template(host)
        dashboard_json = json.dumps(dashboard_dict, indent=4)
        _write_dashboard(dashboard_json, host)
