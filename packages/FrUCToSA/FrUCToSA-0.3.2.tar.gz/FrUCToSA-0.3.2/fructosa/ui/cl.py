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

import argparse


class CLConf:
    def __init__(self, description: str="", arguments=None, defaults=None):
        """The arguments to the constractor are passed to an 
        ArgumentParser instance. They are like follows:
        
        * `arguments` must be a sequence of tuples/lists of the form
          (name: str, argument_definition: sequence)
          where `argument_definition` is expected to be itself
          (args: tuple, kwargs: dictionary)
          They will be passed to the method add_argument of the parser
          like this:
          parser.add_argument(*args, **kwargs)

          For example:
          cl = CLConf(
              description="my important program", 
              arguments=[
                  ("input file", (("-f", "--file"), {"help": "some help"}),
                  ("version", (
                      ("--version"), 
                      {"action": "version", "version": "0.4.9"}
                  ),
                  ...
              ]
              defaults = {"input file": "mydefaultinput.conf"}
        """
        self.description = description
        self.arguments = arguments or ()
        self.defaults = defaults or {}
        self._create_cl_parser()
        self._add_arguments()
        self._parse_arguments()

    def _create_cl_parser(self):
        parser = argparse.ArgumentParser(description=self.description)
        self._cl_parser = parser

    def _add_arguments(self):
        for name, arg in self.arguments:
            args, kwargs = arg
            if name in self.defaults:
                kwargs["default"] = self.defaults[name]
            self._cl_parser.add_argument(*args, **kwargs)

    def _parse_arguments(self):
        args = self._cl_parser.parse_args()
        self._command_line_conf = vars(args)

    def __getitem__(self, item):
        return self._command_line_conf[item]
