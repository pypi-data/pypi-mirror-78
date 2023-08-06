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

import unittest
from unittest.mock import MagicMock, patch

import sys
from fructosa.error_handling import CannotLog, FructosaError, handle_errors
from fructosa.constants import START_STOP_ERROR


class CannotLogTestCase(unittest.TestCase):
    def test_is_exception(self):
        with self.assertRaises(CannotLog):
            raise CannotLog()


class FructosaErrorTestCase(unittest.TestCase):
    def test_is_exception(self):
        with self.assertRaises(FructosaError):
            raise FructosaError()

        
class handle_errorsTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_f = MagicMock()
        
    def test_calls_the_decorated_function(self):
        decorated_f = handle_errors(self.mock_f)
        args = (8, "se")
        kwargs = {"ke": "kieres", "WW": 3}
        decorated_f(*args, **kwargs)
        self.mock_f.assert_called_once_with(*args, **kwargs)

    def test_returns_result_from_function(self):
        result = "$$$%$L"
        self.mock_f.return_value=result
        decorated_f = handle_errors(self.mock_f)
        returned = decorated_f()
        self.assertEqual(result, returned)

    @patch("fructosa.error_handling.print")
    def test_behaviour_with_different_errors(self, pprint):
        msgs = ["bla bla", "blo", "bli", "fol"]
        ex_classes = [FructosaError, KeyError, FileNotFoundError, CannotLog]
        for ex_class, msg in zip(ex_classes, msgs):
            ex = ex_class(msg)
            with self.subTest(ex=ex, msg=msg):
                self.mock_f.side_effect=ex
                decorated_f = handle_errors(self.mock_f)
                with self.assertRaises(SystemExit) as e:
                    decorated_f()
                self.assertEqual(e.exception.code, START_STOP_ERROR)
                pprint.assert_called_once_with(msg, file=sys.stderr)
                pprint.reset_mock()

    def test_function_metadada_preserved(self):
        self.mock_f.__doc__ = "shf"
        decorated_f = handle_errors(self.mock_f)
        self.assertEqual(decorated_f.__doc__, "shf")
        
