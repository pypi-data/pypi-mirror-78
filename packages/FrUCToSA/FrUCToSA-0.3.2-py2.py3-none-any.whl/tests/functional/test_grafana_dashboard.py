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
import functools
import json

import pytest

from .utils import run_program, normalize_whitespaces

from fructosa.constants import (
    MAKE_DASHBOARD_PROGRAM, HOSTS_FILE_METAVAR, MAKE_DASHBOARD_HOSTS_HELP,
    HOSTS_SECTION_SHORT_OPTION, HOSTS_SECTION_LONG_OPTION, HOSTS_FILE_STR,
    HOSTS_SECTION_METAVAR, HOSTS_SECTION_HELP, PROJECT_NAME,
    MAKE_DASHBOARD_FILE_ERROR_MSG, 
)


make_fructosa_dashboard = functools.partial(run_program, MAKE_DASHBOARD_PROGRAM)


class CreationOfGrafanaDashboardsTestCase(unittest.TestCase):
    # 'autouse' to use the fixture in current and the included scopes
    @pytest.fixture(autouse=True)
    def hostsfiles(self, tmpdir):
        tmpdir.chdir()
        # One host:
        self.one_host_file = "one_host"
        self.one_host_name = "funnyhost"
        one_host_contents = f"[hosts]\n{self.one_host_name}\n"
        tmpdir.join(self.one_host_file).write(one_host_contents)
        # Multiple hosts:
        self.multi_hosts_file = "multiple_hosts"
        self.multi_hosts = ["hoston{:02d}".format(_) for _ in range(3)]
        multi_hosts_contents = "[hosts]\n"
        for h in self.multi_hosts:
            multi_hosts_contents += f"{h}\n"
        tmpdir.join(self.multi_hosts_file).write(multi_hosts_contents)
        # One host, different section:
        self.another_host_file = "another_host"
        self.another_host_name = "yahost"
        self.another_hosts_section = "all"
        another_host_contents = (
            f"[{self.another_hosts_section}]\n{self.another_host_name}\n"
        )
        tmpdir.join(self.another_host_file).write(another_host_contents)
        # Missing file:
        self.missing_hosts_file = "no_hosts_file"
        # Missing section:
        self.missing_section_hosts_file = "no_section_hosts_file"
        tmpdir.join(self.missing_section_hosts_file).write("\n")
        # # Empty section:
        # self.empty_section_hosts_file = "empty_section_hosts_file"
        # tmpdir.join(self.empty_section_hosts_file).write("[hosts]\n")
        # Malformed file:
        self.malformed_hosts_file = "malformed_hosts_file"
        self.malformed_contents = "include *-text\n"
        tmpdir.join(self.malformed_hosts_file).write(self.malformed_contents)
        
    def check_one_grafana_dashboard(self, hostname, hostsfile, section=None):
        args = (hostsfile,)
        if section:
            args = args + ("-s", section)
        with make_fructosa_dashboard(*args) as result:
            with open("{}.json".format(hostname)) as f:
                result = f.read()
            normal_out = normalize_whitespaces(result)
            # Is it valid json? Let us try to validate it:
            result_dict = json.loads(normal_out)
            # Fine. Now, does it have the expected contents=
            self.assertEqual(result_dict["title"], hostname)
            tags = result_dict["tags"]
            self.assertIn(PROJECT_NAME, tags)
            self.assertIn(hostname, tags)

    def test_executable_to_create_json_grafana_dashboards(self):
        uphosts = HOSTS_FILE_METAVAR
        hosts_help = MAKE_DASHBOARD_HOSTS_HELP
        short_section = HOSTS_SECTION_SHORT_OPTION
        long_section = HOSTS_SECTION_LONG_OPTION
        section_meta = HOSTS_SECTION_METAVAR
        section_help = HOSTS_SECTION_HELP % {"default": HOSTS_FILE_STR}
        #  After starting the FrUCToSA system, Tux would like to connect
        # it to Grafana. He finds out that there is an executable shipped
        # with the package that can create a dashboard importable by
        # Grafana. Great! Time to find out more about it:
        with make_fructosa_dashboard() as result_mk_fruct_dash:
            self.assertIn(
                f"the following arguments are required: {uphosts}",
                result_mk_fruct_dash.stderr.decode()
            )
        # Okay, okay. He tries the "-h" option:
        with make_fructosa_dashboard("-h") as result_mk_fruct_dash:
            normal_out = normalize_whitespaces(
                result_mk_fruct_dash.stdout.decode()
            )
            self.assertIn(
                f"positional arguments: {uphosts} {hosts_help}",
                normal_out
            )
            self.assertIn(
                (f"optional arguments: -h, --help show this help message and exit"
                 f" {short_section} {section_meta}"
                 f", {long_section} {section_meta} {section_help}"
                ),
                normal_out
            )
        #  Fine, so he prepares a hosts file with only one file and creates
        # a dashboard from it:
        self.check_one_grafana_dashboard(
            hostname=self.one_host_name,
            hostsfile=self.one_host_file
        )
        # Now he can import the created dashboard in Grafana and use it!
        #  ...but actually he is interested in having a dashboard with multiple
        # hosts. He he goes to test this:
        for hostname in self.multi_hosts:
            self.check_one_grafana_dashboard(
                hostname=hostname,
                hostsfile=self.multi_hosts_file,
            )
        # Tux believes firmly in the DRY principle. He allready has a hosts file with
        # a list of hosts, BUT they are under the section "all".
        # ...
        # After looking at the output of help above, he understands that the section
        # where the hosts can be found is customizable. Great!
        # He tests it:
        self.check_one_grafana_dashboard(
            hostname=self.another_host_name,
            hostsfile=self.another_host_file,
            section=self.another_hosts_section,
        )
        #  Wonderful! Tux is delighted with FrUCToSA! He is eager to use it in the
        # cluster!

    def test_missing_hosts_in_hosts_file(self):
        # Out of curiosity. What happens if there is no "hostsfile"?
        with make_fructosa_dashboard(self.missing_hosts_file) as result:
            err = result.stderr.decode().strip()
            expected_err = MAKE_DASHBOARD_FILE_ERROR_MSG.format(
                hosts_file=self.missing_hosts_file,
                hosts_section=HOSTS_FILE_STR,
            )
            self.assertEqual(err, expected_err)
        # or if the file does not contain the proper section?
        with make_fructosa_dashboard(self.missing_section_hosts_file) as result:
            err = result.stderr.decode().strip()
            expected_err = MAKE_DASHBOARD_FILE_ERROR_MSG.format(
                hosts_file=self.missing_section_hosts_file,
                hosts_section=HOSTS_FILE_STR,
            )
            self.assertEqual(err, expected_err)
        # # or if the section is empty?
        # with make_fructosa_dashboard(self.missing_section_hosts_file) as result:
        #     err = result.stderr.decode()
        #     expected_err = MAKE_DASHBOARD_MISSING_HOSTS_MSG.format(
        #         hosts_file=self.missing_section_hosts_file,
        #         hosts_section=HOSTS_FILE_STR,
        #     )
        #     self.assertEqual(err, expected_err)
        # or a malformed file is given?
        with make_fructosa_dashboard(self.malformed_hosts_file) as result:
            err = result.stderr.decode().strip()
            expected_err = (
                "File contains no section headers.\nfile: '{}', line: 1\n"
                "{}"
            ).format(self.malformed_hosts_file, repr(self.malformed_contents))
            self.assertEqual(err, expected_err)
        #  Interesting! This software seems reasonably well behaved!
        # That is important for Tux: it is a sign of quality to his eyes.
