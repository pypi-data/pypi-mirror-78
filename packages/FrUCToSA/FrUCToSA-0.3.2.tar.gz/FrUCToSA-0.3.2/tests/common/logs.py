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


class LogParser:
    def __init__(self, log_file_name, id_strings=None):
        self.log_file_name = log_file_name
        self._id_strings = []
        if id_strings:
            for id_string in id_strings:
                self._id_strings.append(id_string)
        self._line_counting_history = []
        if not os.path.exists(self.log_file_name):
            open(self.log_file_name, "w").close()
        self.count_lines()

    def _simple_line_matches(self, target, line):
        result = False
        if target in line:
            result = True
        return result

    _line_matches = _simple_line_matches
    
    def count_lines(self):
        total_lines = 0
        matched_lines = {k: 0 for k in self._id_strings}
        with open(self.log_file_name, "r") as log_file:
            for line in log_file:
                total_lines += 1
                for target in self._id_strings:
                    if self._line_matches(target, line):
                        matched_lines[target] += 1
            position = log_file.tell()
        self._line_counting_history.append(
            (total_lines, matched_lines, position)
        )
                            
    def get_new_lines(self):
        new_lines = []
        pre_values = self._line_counting_history[-1]
        pre_total_lines, pre_matched_lines, pre_end_position = pre_values
        self.count_lines()
        actual_values = self._line_counting_history[-1]
        total_lines, matched_lines, end_position = actual_values
        if pre_total_lines != total_lines:
            with open(self.log_file_name, "r") as log_file:
                log_file.seek(pre_end_position)
                for line in log_file:
                    for target in self._id_strings:
                        if self._line_matches(target, line):
                            new_lines.append(line)
                            break
        return new_lines


# if __name__ == "__main__":
#     log = LogParser("/var/log/syslog", id_strings=("fructosad",))
#     print(log._line_counting_history)
#     import time
#     time.sleep(30)# send some message with the "logger" command line
#     print(log.get_new_lines())
        

