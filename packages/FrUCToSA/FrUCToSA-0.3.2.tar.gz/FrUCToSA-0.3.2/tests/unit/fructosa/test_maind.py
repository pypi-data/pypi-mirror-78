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
from unittest.mock import patch, MagicMock, call, mock_open
from inspect import signature, Parameter

from fructosa.maind import generic_main
from fructosa.error_handling import CannotLog


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.conf_class = MagicMock()
        self.main_class = MagicMock()
        
    def test_arguments(self):
        s = signature(generic_main)
        parameters = s.parameters
        param_kinds = [param.kind for param in parameters.values()]
        self.assertEqual(len(parameters), 2)
        for param_kind in param_kinds:
            self.assertEqual(Parameter.POSITIONAL_OR_KEYWORD, param_kind)

    def test_creates_conf_instance(self):
        generic_main(self.conf_class, self.main_class)
        self.conf_class.assert_called_once_with()

    def test_creates_main_instance(self):
        conf = MagicMock()
        self.conf_class.return_value = conf
        generic_main(self.conf_class, self.main_class)
        self.main_class.assert_called_once_with(conf)

    def test_calls_main_instance(self):
        mocked_instance = MagicMock()
        self.main_class.return_value = mocked_instance
        generic_main(self.conf_class, self.main_class)
        mocked_instance.assert_called_once_with()

    def test_handle_errors_called(self):
        self.conf_class.side_effect = CannotLog()
        with self.assertRaises(SystemExit):
            generic_main(self.conf_class, self.main_class)
    
        
if __name__ == "__main__":
    unittest.main()
