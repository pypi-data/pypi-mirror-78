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


import subprocess as sp
from contextlib import contextmanager


@contextmanager
def run_program(program, *args):
    line = (program,)+args
    result = sp.run(line, stdout=sp.PIPE, stderr=sp.PIPE)
    yield result


def normalize_whitespaces(text):
    """Normalize the whitespaces in the text: any whitespace sequence -> ' '
    """
    text = text.replace("\n", " ")
    while True:
        new_text = text.replace("\t", " ")
        new_new_text = new_text.replace("  ", " ")
        if new_new_text == text:
            break
        else:
            text = new_new_text
    return text
