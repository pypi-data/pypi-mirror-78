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

import asyncio
from unittest.mock import MagicMock


def asyncio_run(coroutine):
    return asyncio.get_event_loop().run_until_complete(coroutine)

def AsyncioMock(*args, **kwargs):
    mock = MagicMock(*args, **kwargs)
    async def mock_coroutine(*args, **kwargs):
        return mock(*args, **kwargs)
    mock_coroutine.mock = mock
    return mock_coroutine
