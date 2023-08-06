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
from unittest.mock import patch, MagicMock, mock_open, call
import sys

from fructosa.grafana.dashboard import (
    make_dashboard, _render_dashboard_template, _collect_hosts,
    _write_dashboard,
)
from fructosa.constants import (
    MAKE_DASHBOARD_DESCRIPTION, MAKE_DASHBOARD_HOSTS_HELP,
    HOSTS_FILE_STR, HOSTS_FILE_METAVAR,
    HOSTS_SECTION_SHORT_OPTION, HOSTS_SECTION_LONG_OPTION,
    HOSTS_SECTION_METAVAR, HOSTS_SECTION_HELP, HOSTS_SECTION_STR,
    MAKE_DASHBOARD_FILE_ERROR_MSG, START_STOP_ERROR
)
from fructosa.grafana.node import node_template_dict, node_panels_template
from fructosa.error_handling import FructosaError


HOST1 = "mastodonte"
CONF_DATA1 = f"[hosts]\n{HOST1}\n"


class ControlError(Exception):
    pass


@patch("fructosa.grafana.dashboard._collect_hosts")
@patch("fructosa.grafana.dashboard._render_dashboard_template")
@patch("fructosa.grafana.dashboard.CLConf")
@patch("fructosa.grafana.dashboard.json.dumps")
@patch("fructosa.grafana.dashboard._write_dashboard")
class MakeDashboardTestCase(unittest.TestCase):
    def test_creates_CLConf_object(
            self, mwrite, mdumps, pCLConf, mrender_template, mcollect_hosts):
        expected_args = (
            (
                "hosts",
                (
                    ("hosts",),
                    {
                        "metavar": HOSTS_FILE_METAVAR,
                        "help": MAKE_DASHBOARD_HOSTS_HELP
                    }
                )
            ),
            (
                "section",
                (
                    (HOSTS_SECTION_SHORT_OPTION, HOSTS_SECTION_LONG_OPTION),
                    {
                        "metavar": HOSTS_SECTION_METAVAR,
                        "help": HOSTS_SECTION_HELP,
                        "default": HOSTS_FILE_STR,
                    }
                )
            ),
        )
        make_dashboard()
            
        pCLConf.assert_called_once_with(
            description=MAKE_DASHBOARD_DESCRIPTION,
            arguments=expected_args,
        )

    def test_print_out_result(
            self, mwrite, mdumps, pCLConf, mrender_template, mcollect_hosts):
        hosts = ["t", None, 0, "-----"]
        jsons = ["a", "v", "z", "D"]
        mcollect_hosts.return_value = hosts
        mdumps.side_effect = jsons
        make_dashboard()
        expected_calls = [call(_, h) for _,h in zip(jsons, hosts)]
        mwrite.assert_has_calls(expected_calls, any_order=True)

    def test_json_created_from_rendered_template(
            self, mwrite, mdumps, pCLConf, mrender_template, mcollect_hosts):
        hosts = [334, "a"]
        jsons = ["aa", "xx"]
        mcollect_hosts.return_value = hosts
        mrender_template.side_effect = jsons
        make_dashboard()
        mdumps.assert_has_calls([call(j, indent=4) for j in jsons])

    def test_render_dashboard_template_called(
            self, mwrite, mdumps, pCLConf, mrender_template,
            mcollect_hosts):
        hosts = ["winni", "peg", "glez"]
        mcollect_hosts.return_value = hosts
        make_dashboard()
        mrender_template.assert_has_calls([call(h) for h in hosts], any_order=True)

    def test_collect_hosts_called(
            self, mwrite, mdumps, pCLConf, mrender_template,
            mcollect_hosts):
        make_dashboard()
        mcollect_hosts.assert_called_once_with(
            pCLConf.return_value[HOSTS_FILE_STR],
            pCLConf.return_value[HOSTS_SECTION_STR],
        )

    def test_exceptions_converted_to_SystemExit(
            self, mwrite, mdumps, pCLConf, mrender_template,
            mcollect_hosts):
        mcollect_hosts.side_effect = Exception("empty message")
        with self.assertRaises(SystemExit):
            make_dashboard()

    def test_handling_KeyError_in_collect_hosts(
            self, mwrite, mdumps, pCLConf, mrender_template,
            mcollect_hosts):
        unwrapped_make_dashboard = make_dashboard.__wrapped__
        hosts_file = "majadaonda"
        mcollect_hosts.side_effect = KeyError(hosts_file)
        def getitem(item):
            if item == HOSTS_FILE_STR:
                return hosts_file
            elif item == HOSTS_SECTION_STR:
                return HOSTS_FILE_STR
        pCLConf.return_value.__getitem__.side_effect = getitem
        msg = MAKE_DASHBOARD_FILE_ERROR_MSG.format(
            hosts_file=hosts_file,
            hosts_section=HOSTS_FILE_STR
        )
        with self.assertRaises(FructosaError) as cm:
            unwrapped_make_dashboard()
        self.assertEqual(str(cm.exception), msg)


class RenderDashboardTemplateTestCase(unittest.TestCase):
    def test_host_included_in_dashboard_tags(self):
        host = "mylittle host"
        dashboard = _render_dashboard_template(host)
        self.assertIn(host, dashboard["tags"])
                              
    def test_hostname_rendered_in_dashboard_title(self):
        host = "myhost"
        dashboard = _render_dashboard_template(host)
        self.assertIn(host, dashboard["title"])
        
    def test_returns_dashboard_with_one_host_if_one_argument(self):
        dashboard = _render_dashboard_template("mylittle host")
        one_dashboard_num_panels = len(node_panels_template)
        self.assertEqual(len(dashboard["panels"]), one_dashboard_num_panels)

    def test_panels_have_host_name_with_one_host(self):
        host = "mylittle host"
        dashboard = _render_dashboard_template(host)
        for panel in dashboard["panels"]:
            try:
                description = panel["description"]
            except KeyError:
                pass
            else:
                self.assertNotIn("{hostname}", description)
            try:
                targets = panel["targets"]
            except KeyError:
                pass
            else:
                for target in targets:
                    try:
                        target_str = target["target"]
                    except KeyError:
                        pass
                    else:
                        self.assertNotIn("{hostname}", target_str)
                        self.assertIn(host, target_str)
                        

class CollectHostsTestCase(unittest.TestCase):
    @staticmethod
    def make_mocked_section_object(section, keyless_values):
        mocked_section_object = MagicMock()
        mocked_section_object.keys.return_value = iter(keyless_values)
        def mocked_section(item):
            if item == section:
                return mocked_section_object
        return mocked_section

    @patch("fructosa.grafana.dashboard.configparser.ConfigParser")
    def test_returns_list_of_hosts_from_file_name(self, pConfigParser):
        expected = 'moN', 8, None, "3"
        sections = ("hosts", "other")
        for section in sections:
            conf_mock = MagicMock()
            conf_mock.section = section
            with self.subTest(section=section):
                mocked_section = self.make_mocked_section_object(section, expected)
                conf_mock.__getitem__.side_effect = mocked_section
                pConfigParser.return_value = conf_mock
                hosts = _collect_hosts("my_test_file.conf", section)
                self.assertEqual(hosts, expected)

    @patch("fructosa.grafana.dashboard.configparser.ConfigParser")
    def test_config_file_read_before_getting_values(self, pConfigParser):
        conf = MagicMock()
        conf.__getitem__.side_effect = ControlError
        pConfigParser.return_value = conf
        with self.assertRaises(ControlError):
            hosts = _collect_hosts("telesforo", "oh")
        conf.read.assert_called_once_with("telesforo")

    def test_accepts_hosts_file_without_values(self):
        with patch(
                "configparser.open", mock_open(read_data=CONF_DATA1)) as mopen:
            hosts = _collect_hosts("telesforo", "hosts")
        

class WriteDashboardTestCase(unittest.TestCase):
    def test_saves_file_with_contents(self):
        m = mock_open()
        host = "mocodepavo"
        contents = "myfu\n\nycontents"
        with patch('fructosa.grafana.dashboard.open', m):
            _write_dashboard(contents, host)
        m.assert_called_once_with(host+".json", "w")
        handle = m()
        handle.write.assert_called_once_with(contents)
