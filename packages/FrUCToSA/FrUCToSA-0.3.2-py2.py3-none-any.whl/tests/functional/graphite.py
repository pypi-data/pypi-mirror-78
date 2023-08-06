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

"""This module contains code to interact with Graphite. It has been
devised to be used within the functional tests for FrUCToSA.
"""

import time
import os
import multiprocessing as mp

from compose.cli.main import TopLevelCommand, project_from_options
from urllib import request, parse

from tests.common.docker import FTDocker


def get_data_from_graphite_render_api(target, **other_options):
    base_url = "http://localhost/render"
    #"?target=&format=raw&from=-1800s"
    parms = {
        "target": target,
        "format": "raw",
        "from": "-10s",
    }
    parms.update(other_options)
    querystring = parse.urlencode(parms)
    u = request.urlopen(base_url+"?"+querystring)
    #print("[X] URL='{}'".format(base_url+"?"+querystring))
    resp = u.read()
    return resp.decode()


class Graphite(FTDocker):
    """This class is an interface to Graphite through docker-compose. It can create
    and manipulate a Graphite system.
    """
    
    def __init__(self):
        base = os.path.dirname(__file__)
        super().__init__(os.path.join(base, "data/graphite"))

                

if __name__ == "__main__":
    # some test:
    g = Graphite()
    g.down()
    g.up()
    g.wait_until_running()
    time.sleep(60)
    g.down()


