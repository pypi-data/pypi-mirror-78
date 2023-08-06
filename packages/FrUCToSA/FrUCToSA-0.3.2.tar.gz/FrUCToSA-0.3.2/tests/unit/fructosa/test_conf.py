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

import fructosa.conf
from fructosa.sensors import sensor_factory

from fructosa.constants import (
    LAGENT_TO_LMASTER_DATA_PORT_KEY, LAGENT_TO_LMASTER_DATA_PORT,
    LMASTER_HOST_KEY, LMASTER_HOST, LMASTER_PROGRAM,
    GRAPHITE_HOST, GRAPHITE_HOST_KEY, GRAPHITE_CARBON_RECEIVER_PICKLE_PORT,
    GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY, GRAPHITE_SECTION,
    OWN_LOG_FILE_KEY, DEFAULT_OWN_FILE_LOGGING_PATH,
    OWN_LOG_LEVEL_KEY, DEFAULT_OWN_FILE_LOGGER_LEVEL,
    OWN_LOG_MAXBYTES_KEY, OWN_LOG_BACKUPCOUNT_KEY,
    OWN_LOG_SECTION, 
)

class FructosaDConfTestCase(unittest.TestCase):
    @patch("fructosa.conf.FructosaDConf._post_process_configuration")
    @patch("fructosa.conf.FructosaDConf._prepare_logging")
    @patch("fructosa.conf.FructosaDConf._set_config_file")
    @patch("fructosa.conf.FructosaDConf._get_conf_from_config_file")
    @patch("fructosa.conf.FructosaDConf._get_conf_from_command_line")
    def setUp(
            self, pget_cnf_frm_cmdl, pget_cnf_frm_cfgf, pset_config_file,
            pprepare_logging, ppost_process_configuration):
        logger = MagicMock()
        self.logger = logger
        self.test_class = fructosa.conf.FructosaDConf
        self.empty_init_instance = self.test_class()
        #mocked_cl_parser = MagicMock()
        #self.empty_init_instance._cl_parser = mocked_cl_parser
        
    def test_instance_has_description_attribute(self):
        from fructosa.constants import FRUCTOSAD_DESCRIPTION
        self.assertEqual(self.empty_init_instance.description, FRUCTOSAD_DESCRIPTION)

    def test_description_is_strable(self):
        str(self.empty_init_instance)

    @patch("fructosa.conf.FructosaDConf._post_process_configuration")
    @patch("fructosa.conf.FructosaDConf._prepare_logging")
    @patch("fructosa.conf.FructosaDConf._set_config_file")
    @patch("fructosa.conf.FructosaDConf._get_conf_from_config_file")
    @patch("fructosa.conf.FructosaDConf._get_conf_from_command_line")
    def test_setup_logging_called_before_post_process_configuration(
            self, pget_cnf_frm_cmdl, pget_cnf_frm_cfgf, pset_config_file,
            pprepare_logging, ppost_process_configuration):
        pprepare_logging.side_effect = Exception
        with self.assertRaises(Exception):
            self.test_class()
        ppost_process_configuration.assert_not_called()

    def test_instance_has_correct_default_values(self):
        from fructosa.conf import FRUCTOSAD_DEFAULT_PIDFILE
        from fructosa.constants import FRUCTOSAD_DEFAULT_CONFIGFILE
        from fructosa.constants import PIDFILE_STR, ACTION_STR, CONFIGFILE_STR
        self.assertEqual(
            self.empty_init_instance.default_values[PIDFILE_STR], FRUCTOSAD_DEFAULT_PIDFILE
        )
        self.assertEqual(
            self.empty_init_instance.default_values[CONFIGFILE_STR], FRUCTOSAD_DEFAULT_CONFIGFILE
        )
        with self.assertRaises(KeyError):
            self.empty_init_instance.default_values[ACTION_STR]

    def test_init_parameters(self):
        s = signature(self.test_class)
        parameters = s.parameters
        self.assertEqual(len(parameters), 1)

    def test_init_parameter_args(self):
        s = signature(self.test_class)
        parameters = s.parameters
        param_args = [param.kind for param in parameters.values()][0]
        expected = Parameter.POSITIONAL_OR_KEYWORD
        self.assertEqual(expected, param_args)

    @patch("fructosa.conf.FructosaDConf._set_config_file")
    @patch("fructosa.conf.FructosaDConf._get_conf_from_command_line")
    def test_init_sets_command_line_conf(
            self, pget_conf_from_cmdl, pset_config_file):
        pset_config_file.side_effect = Exception
        with self.assertRaises(Exception):
            self.test_class("jama")
        pget_conf_from_cmdl.assert_called_once_with()

    @patch("fructosa.conf.FructosaDConf._post_process_configuration")
    @patch("fructosa.conf.FructosaDConf._prepare_logging")
    @patch("fructosa.conf.FructosaDConf._set_config_file")
    @patch("fructosa.conf.FructosaDConf._get_conf_from_config_file")
    @patch("fructosa.conf.FructosaDConf._get_conf_from_command_line")
    def test_init_set_config_file(
            self, pget_conf_from_cmdl, pget_conf_from_configfile, pset_config_file,
            pprepare_logging, ppost_process_configuration):
        self.test_class()
        pset_config_file.assert_called_once_with()

    @patch("fructosa.conf.FructosaDConf._set_config_file")
    @patch("fructosa.conf.FructosaDConf._get_conf_from_config_file")
    @patch("fructosa.conf.FructosaDConf._get_conf_from_command_line")
    def test_init_calls_get_conf_from_config_file_after_set_config_file(
            self, pget_conf_from_cmdl, pget_conf_from_configfile, pset_config_file):
        pget_conf_from_configfile.side_effect = Exception
        with self.assertRaises(Exception):
            self.test_class()
        pget_conf_from_configfile.assert_called_once_with()
        pset_config_file.assert_called_once_with()

    @patch("fructosa.conf.FructosaDConf._prepare_logging")
    @patch("fructosa.conf.FructosaDConf._set_config_file")
    @patch("fructosa.conf.FructosaDConf._get_conf_from_config_file")
    @patch("fructosa.conf.FructosaDConf._get_conf_from_command_line")
    def test_init_calls_prepare_logging_after_get_conf_from_configfile(
            self, pget_conf_from_cmdl, pget_conf_from_configfile,
            pset_config_file, pprepare_logging):
        pprepare_logging.side_effect = Exception
        with self.assertRaises(Exception):
            self.test_class()
        pprepare_logging.assert_called_once_with()
        pget_conf_from_configfile.assert_called_once_with()

    @patch("fructosa.conf.FructosaDConf._post_process_configuration")
    @patch("fructosa.conf.FructosaDConf._prepare_logging")
    @patch("fructosa.conf.FructosaDConf._set_config_file")
    @patch("fructosa.conf.FructosaDConf._get_conf_from_config_file")
    @patch("fructosa.conf.FructosaDConf._get_conf_from_command_line")
    def test_init_calls_post_process_configuration_after_prepare_logging(
            self, pget_conf_from_cmdl, pget_conf_from_configfile,
            pset_config_file, pprepare_logging, ppost_process_configuration):
        ppost_process_configuration.side_effect = Exception
        with self.assertRaises(Exception):
            self.test_class()
        ppost_process_configuration.assert_called_once_with()
        pprepare_logging.assert_called_once_with()

    @patch("fructosa.conf.CLConf")
    def test_get_conf_from_command_line_creates_CLConf_object(self, pCLConf):
        instance = self.empty_init_instance
        instance._get_conf_from_command_line()
        pCLConf.assert_called_once_with(
            arguments=instance.arguments,
            description=instance.description,
            defaults=instance.default_values,
        )
        self.assertEqual(instance._command_line_conf, pCLConf.return_value)
    
    @patch("fructosa.conf.FructosaDConf._parse_config_file")
    @patch("fructosa.conf.FructosaDConf._create_config_parser")
    def test_get_conf_from_config_file_call_sequence(
            self, pcreate_config_parser, pparse_config_file):
        manager = MagicMock()
        manager.attach_mock(pcreate_config_parser, "_create_config_parser")
        manager.attach_mock(pparse_config_file, "_parse_config_file")
        expected_calls = [
            call._create_config_parser(),
            call._parse_config_file(),
        ]
        instance = self.empty_init_instance
        instance._config_file = MagicMock()
        instance._config_file_conf = MagicMock()
        instance._get_conf_from_config_file()
        manager.assert_has_calls(expected_calls)

    @patch("fructosa.conf.FructosaDConf._logging_from_config_file")
    @patch("fructosa.conf.setup_logging")
    def test_prepare_logging_sets_logger_attribute(
            self, psetup_logging, plogging_from_config_file):
        logger = MagicMock()
        psetup_logging.return_value = logger
        self.empty_init_instance.logging = MagicMock()
        with self.assertRaises(AttributeError):
            self.empty_init_instance.logger
        self.empty_init_instance._prepare_logging()
        self.empty_init_instance.logger

    @patch("fructosa.conf.FructosaDConf._logging_from_config_file")
    @patch("fructosa.conf.setup_logging")
    def test_prepare_logging_calls_setup_logging_after_logging_from_config_file(
            self, psetup_logging, plogging_from_config_file):
        psetup_logging.side_effect = Exception
        self.empty_init_instance.logging = MagicMock()
        with self.assertRaises(Exception):
            self.empty_init_instance._prepare_logging()
        psetup_logging.assert_called_once_with(
            logger_name=self.empty_init_instance.__class__.__name__,
            rotatingfile_conf=self.empty_init_instance.logging
        )
        plogging_from_config_file.assert_called_once_with()

    @patch("fructosa.conf.configparser.ConfigParser")
    def test_create_config_parser_sets_config_file_conf_attribute(self, pconfigparser):
        instance = self.empty_init_instance
        conf = MagicMock()
        pconfigparser.return_value = conf
        instance._create_config_parser()
        self.assertEqual(instance._config_file_conf, conf)

    def test_parse_config_file_calls_configparser_read_method(self):
        from fructosa.constants import CONFIGFILE_STR
        instance = self.empty_init_instance
        conf = MagicMock()
        configfile = MagicMock()
        instance._config_file_conf = conf
        instance._config_file = configfile
        instance._parse_config_file()
        conf.read.assert_called_once_with(configfile)

    @patch("fructosa.conf.FructosaDConf.__getitem__")
    def test_set_config_file_sets_config_file_attribute(self, pgetitem):
        from fructosa.constants import CONFIGFILE_STR
        instance = self.empty_init_instance
        mock_conf = MagicMock()
        def getitem(item):
            if item == CONFIGFILE_STR:
                return mock_conf
        pgetitem.side_effect = getitem
        instance._set_config_file()
        self.assertEqual(instance._config_file, mock_conf)

    def test_getitem_wraps_command_line_confs_getitem(self):
        key = MagicMock()
        confini = MagicMock()
        conf = self.empty_init_instance
        conf._command_line_conf = confini
        res = conf[key]
        self.assertEqual(res, conf._command_line_conf[key])

    @patch("fructosa.conf.FructosaDConf._lmaster_from_config_file")
    def test_post_process_configuration_calls_lmaster_from_config_file(
            self, plmaster_from_config_file):
        self.empty_init_instance.logger = MagicMock()
        self.empty_init_instance._config_file = MagicMock()
        self.empty_init_instance._post_process_configuration()
        plmaster_from_config_file.assert_called_once_with()

    @patch("fructosa.conf.FructosaDConf._lmaster_from_config_file")
    def test_post_process_configuration_messages_to_logger(
            self, plmaster_from_config_file):
        from fructosa.constants import CONF_READ_MSG
        from fructosa.logs import setup_logging
        instance = self.empty_init_instance
        logger = setup_logging(
            logger_name=instance.__class__.__name__,
            rotatingfile_conf={"filename": "/dev/null"},
        )
        instance.logger = logger
        config_file = MagicMock()
        instance._config_file = config_file
        msg = CONF_READ_MSG.format(config_file=config_file)
        other_msg = 'winnipeg\ngonzalez'
        with self.assertLogs(instance.__class__.__name__, level="INFO") as log:
            with patch('fructosa.conf.open', mock_open(read_data=other_msg)) as m:
                instance._post_process_configuration()
        self.assertIn(msg, log.output[0])
        self.assertEqual(len(log.output), 3)
        for ielement, element in enumerate(other_msg.split("\n")):
            self.assertIn(f" ... {element}", log.output[ielement+1])
        m.assert_called_once_with(config_file)

    @patch("fructosa.conf.FructosaDConf._lmaster_from_config_file")
    def test_post_process_configuration_messages_to_logger_if_missing_conf_file(
            self, plmaster_from_config_file):
        from fructosa.constants import CONF_READ_MSG
        from fructosa.logs import setup_logging
        instance = self.empty_init_instance
        logger = setup_logging(
            logger_name=instance.__class__.__name__,
            rotatingfile_conf={"filename": "/dev/null"},
        )
        instance.logger = logger
        config_file = MagicMock()
        mopen = MagicMock(side_effect=OSError)
        instance._config_file = config_file
        msg = CONF_READ_MSG.format(config_file=config_file)
        with self.assertLogs(instance.__class__.__name__, level="INFO") as log:
            with patch('fructosa.conf.open', mopen) as m:
                instance._post_process_configuration()
        self.assertIn(msg, log.output[0])
        self.assertEqual(len(log.output), 1)
        m.assert_called_once_with(config_file)

    def test_lmaster_from_config_file_sets_lmaster_attribute(self):
        with self.assertRaises(AttributeError):
            self.empty_init_instance.lmaster
        self.empty_init_instance._config_file_conf = MagicMock()
        self.empty_init_instance._lmaster_from_config_file()
        self.empty_init_instance.lmaster
        
    def test_lmaster_from_config_file_returns_defaults_if_missing_section(self):
        self.empty_init_instance._config_file_conf = {}
        #self.empty_init_instance._config_file_conf.sections().return_value = None
        self.empty_init_instance._lmaster_from_config_file()
        lmaster = self.empty_init_instance.lmaster
        self.assertEqual(lmaster[LMASTER_HOST_KEY], LMASTER_HOST)
        self.assertEqual(lmaster[LAGENT_TO_LMASTER_DATA_PORT_KEY], LAGENT_TO_LMASTER_DATA_PORT)

    def test_lmaster_from_config_file_give_priority_to_file_over_defaults_in_lmaster_section(self):
        test_conf = {
            LMASTER_HOST_KEY: "winnipoj",
            LAGENT_TO_LMASTER_DATA_PORT_KEY: 23452
        }
        self.empty_init_instance._config_file_conf = {LMASTER_PROGRAM: test_conf}
        self.empty_init_instance._lmaster_from_config_file()
        lmaster = self.empty_init_instance.lmaster
        self.assertEqual(lmaster[LMASTER_HOST_KEY], "winnipoj")
        self.assertEqual(lmaster[LAGENT_TO_LMASTER_DATA_PORT_KEY], 23452)

    def test_lmaster_from_config_file_host_has_priority_over_default_in_lmaster_section(self):
        test_conf = {LMASTER_HOST_KEY: "winnipeg"}
        self.empty_init_instance._config_file_conf = {LMASTER_PROGRAM: test_conf}
        self.empty_init_instance._lmaster_from_config_file()
        lmaster = self.empty_init_instance.lmaster
        self.assertEqual(lmaster[LMASTER_HOST_KEY], "winnipeg")
        self.assertEqual(lmaster[LAGENT_TO_LMASTER_DATA_PORT_KEY], LAGENT_TO_LMASTER_DATA_PORT)

    def test_lmaster_from_config_file_port_has_priority_over_default_in_lmaster_section(self):
        test_conf = {LAGENT_TO_LMASTER_DATA_PORT_KEY: 54545}
        self.empty_init_instance._config_file_conf = {LMASTER_PROGRAM: test_conf}
        self.empty_init_instance._lmaster_from_config_file()
        lmaster = self.empty_init_instance.lmaster
        self.assertEqual(lmaster[LMASTER_HOST_KEY], LMASTER_HOST)
        self.assertEqual(lmaster[LAGENT_TO_LMASTER_DATA_PORT_KEY], 54545)

    def test_logging_from_config_file_sets_logging_attribute(self):
        with self.assertRaises(AttributeError):
            self.empty_init_instance.logging
        self.empty_init_instance._config_file_conf = MagicMock()
        self.empty_init_instance._logging_from_config_file()
        self.empty_init_instance.logging

    def test_logging_from_config_file_returns_defaults_if_missing_section(self):
        self.empty_init_instance._config_file_conf = {}
        self.empty_init_instance._logging_from_config_file()
        logging = self.empty_init_instance.logging
        self.assertEqual(logging[OWN_LOG_FILE_KEY], DEFAULT_OWN_FILE_LOGGING_PATH)
        self.assertEqual(logging[OWN_LOG_LEVEL_KEY], DEFAULT_OWN_FILE_LOGGER_LEVEL)

    def test_logging_from_config_file_give_priority_to_file_over_defaults_in_logging_section(self):
        test_conf = {
            OWN_LOG_FILE_KEY: "/winnipoj",
            OWN_LOG_LEVEL_KEY: "WHATEVER",
        }
        self.empty_init_instance._config_file_conf = {OWN_LOG_SECTION: test_conf}
        self.empty_init_instance._logging_from_config_file()
        logging = self.empty_init_instance.logging
        self.assertEqual(logging[OWN_LOG_FILE_KEY], "/winnipoj")
        self.assertEqual(logging[OWN_LOG_LEVEL_KEY], "WHATEVER")

    def test_logging_from_config_file_valid_optional_keys_if_given(self):
        test_conf = {
            OWN_LOG_MAXBYTES_KEY: "1005",
            OWN_LOG_BACKUPCOUNT_KEY: "4",
            "parida": 23,
        }
        self.empty_init_instance._config_file_conf = {OWN_LOG_SECTION: test_conf}
        self.empty_init_instance._logging_from_config_file()
        logging = self.empty_init_instance.logging
        self.assertEqual(logging[OWN_LOG_MAXBYTES_KEY], 1005)
        self.assertEqual(logging[OWN_LOG_BACKUPCOUNT_KEY], 4)
        with self.assertRaises(KeyError):
            logging["parida"]

    def test_logging_from_config_file_log_file_has_priority_over_default_in_logging_section(self):
        test_conf = {OWN_LOG_FILE_KEY: "/machu/pichu.log"}
        self.empty_init_instance._config_file_conf = {OWN_LOG_SECTION: test_conf}
        self.empty_init_instance._logging_from_config_file()
        logging = self.empty_init_instance.logging
        self.assertEqual(logging[OWN_LOG_FILE_KEY], "/machu/pichu.log")
        self.assertEqual(logging[OWN_LOG_LEVEL_KEY], DEFAULT_OWN_FILE_LOGGER_LEVEL)

    def test_logging_from_config_file_level_has_priority_over_default_in_logging_section(self):
        test_conf = {OWN_LOG_LEVEL_KEY: "CRITICAL"}
        self.empty_init_instance._config_file_conf = {OWN_LOG_SECTION: test_conf}
        self.empty_init_instance._logging_from_config_file()
        logging = self.empty_init_instance.logging
        self.assertEqual(logging[OWN_LOG_FILE_KEY], DEFAULT_OWN_FILE_LOGGING_PATH)
        self.assertEqual(logging[OWN_LOG_LEVEL_KEY], "CRITICAL")

    def test_logging_from_config_file_optional_values_raise_KeyError_if_not_given(self):
        test_conf = {}
        self.empty_init_instance._config_file_conf = {OWN_LOG_SECTION: test_conf}
        self.empty_init_instance._logging_from_config_file()
        logging = self.empty_init_instance.logging
        with self.assertRaises(KeyError):
            logging[OWN_LOG_MAXBYTES_KEY]
        with self.assertRaises(KeyError):
            logging[OWN_LOG_BACKUPCOUNT_KEY]
        
        
class LAgentConfTestCaseBase(unittest.TestCase):
    @patch("fructosa.conf.LAgentConf._post_process_configuration")
    @patch("fructosa.conf.LAgentConf._prepare_logging")
    @patch("fructosa.conf.LAgentConf._set_config_file")                
    @patch("fructosa.conf.LAgentConf._get_conf_from_config_file")
    @patch("fructosa.conf.LAgentConf._get_conf_from_command_line")
    def setUp(self, pget_cnf_frm_cmdl, pget_cnf_frm_cfgf, pset_config_file,
              psetup_logging, pfinalize_after_config_file):
        self.test_class = fructosa.conf.LAgentConf
        self.empty_init_instance = self.test_class()
        #mocked_cl_parser = MagicMock()
        #self.empty_init_instance._cl_parser = mocked_cl_parser
        
    
class LAgentConfTestCase(LAgentConfTestCaseBase):
    def test_instance_has_description_attribute(self):
        from fructosa.constants import LAGENT_DESCRIPTION
        self.assertEqual(self.empty_init_instance.description, LAGENT_DESCRIPTION)

    def test_is_subclass_of_FructosaDConf(self):
        from fructosa.conf import FructosaDConf
        self.assertTrue(issubclass(self.test_class, FructosaDConf))
        
    def test_description_is_strable(self):
        str(self.empty_init_instance)
        
    def test_instance_has_correct_default_values(self):
        from fructosa.conf import LAGENT_DEFAULT_PIDFILE
        from fructosa.constants import (
            PIDFILE_STR, ACTION_STR, CONFIGFILE_STR, LAGENT_DEFAULT_CONFIGFILE,
        )
        self.assertEqual(
            self.empty_init_instance.default_values[PIDFILE_STR], LAGENT_DEFAULT_PIDFILE)
        self.assertEqual(
            self.empty_init_instance.default_values[CONFIGFILE_STR], LAGENT_DEFAULT_CONFIGFILE
        )
        with self.assertRaises(KeyError):
            self.empty_init_instance.default_values[ACTION_STR]

    @patch("fructosa.conf.LAgentConf._graphite_from_config_file")
    @patch("fructosa.conf.FructosaDConf._post_process_configuration")
    @patch("fructosa.conf.LAgentConf._sensors_from_config_file_sections")
    def test_post_process_configuration_calls_sensors_from_config_file_sections(
            self, psensors_from_config_file_sections,
            ppost_process_configuration, pgraphite_from_config_file):
        self.empty_init_instance._post_process_configuration()
        psensors_from_config_file_sections.assert_called_once_with()

    @patch("fructosa.conf.FructosaDConf._post_process_configuration")
    @patch("fructosa.conf.LAgentConf._graphite_from_config_file")
    @patch("fructosa.conf.LAgentConf._sensors_from_config_file_sections")
    def test_post_process_configuration_calls_graphite_from_config_file(
            self, psensors_from_config_file_sections,
            pgraphite_from_config_file, ppost_process_configuration):
        self.empty_init_instance._post_process_configuration()
        pgraphite_from_config_file.assert_called_once_with()

    @patch("fructosa.conf.LAgentConf._graphite_from_config_file")
    @patch("fructosa.conf.FructosaDConf._post_process_configuration")
    @patch("fructosa.conf.LAgentConf._sensors_from_config_file_sections")
    def test_post_process_configuration_calls_same_method_in_FructosaDConf(
            self, psensors_from_config_file_sections, pgraphite_from_config_file,
            ppost_process_configuration):
        self.empty_init_instance._post_process_configuration()
        ppost_process_configuration.assert_called_once_with()

    def test_make_sensor_from_section_return_value_if_input_not_a_sensor(self):
        not_a_sensor = MagicMock()
        result = self.empty_init_instance._make_sensor_from_section(not_a_sensor)
        self.assertEqual(result, None)

    @patch("fructosa.conf.sensor_factory")
    def test_make_sensor_from_section_return_value_if_input_is_a_sensor(self, psensor_factory):
        sensor = MagicMock()
        psensor_factory.return_value = sensor
        section = MagicMock()
        sensor_name = "{}".format(sensor)
        section.partition.return_value = ("sensor", ":", sensor_name)
        conf = MagicMock()
        conf_item = MagicMock()
        def getitem(item):
            if item == section:
                return conf_item
            else:
                return MagicMock()
        conf.__getitem__.side_effect = getitem
        self.empty_init_instance._config_file_conf = conf
        logging = MagicMock()
        self.empty_init_instance.logging = logging
        result = self.empty_init_instance._make_sensor_from_section(section)
        psensor_factory.assert_called_once_with(sensor_name, conf_item, logging)
        self.assertEqual(result, sensor)        

    @patch("fructosa.conf.sensor_factory")
    def test_make_sensor_from_section_behaviour_if_NameError_raised(self, psensor_factory):
        from fructosa.constants import PROTO_INVALID_SENSOR_MSG
        from fructosa.logs import setup_logging
        psensor_factory.side_effect = NameError()
        section = MagicMock()
        sensor = MagicMock()
        section.partition.return_value = ("sensor", ":", sensor)
        self.empty_init_instance._config_file_conf = MagicMock()
        logging = MagicMock()
        self.empty_init_instance.logging = logging
        logger = setup_logging(
            logger_name=self.empty_init_instance.__class__.__name__,
            rotatingfile_conf={"filename": "/dev/null"},
        )
        self.empty_init_instance.logger = logger
        with self.assertLogs(self.empty_init_instance.__class__.__name__, "ERROR") as cm:
            result = self.empty_init_instance._make_sensor_from_section(section)
        self.assertEqual(result, None)
        self.assertIn(PROTO_INVALID_SENSOR_MSG.format(sensor_name=sensor), cm.output[0])

    
class LAgentConf_sensors_from_config_file_sectionsTestCase(LAgentConfTestCaseBase):
    def setUp(self):
        super().setUp()
        self.conf = MagicMock()
        self.empty_init_instance._config_file_conf = self.conf
        
    @patch("fructosa.conf.LAgentConf._make_sensor_from_section")
    def test_sets_sensors_attribute(self, pmake_sensor_from_section):
        self.empty_init_instance._sensors_from_config_file_sections()
        self.assertTrue(hasattr(self.empty_init_instance, "sensors"))

    @patch("fructosa.conf.LAgentConf._make_sensor_from_section")
    def test_iterates_over_sections(self, pmake_sensor_from_section):
        sections = MagicMock()
        self.conf.sections.return_value = sections
        self.empty_init_instance._sensors_from_config_file_sections()
        sections.__iter__.assert_called_once_with()

    @patch("fructosa.conf.LAgentConf._make_sensor_from_section")
    def test_calls_make_sensor_from_section_with_each_section(self, pmake_sensor_from_section):
        sections = MagicMock()
        sections_results = [MagicMock() for _ in range(5)]
        sections.__iter__.return_value = sections_results
        self.conf.sections.return_value = sections
        expected_calls = [call(section) for section in sections_results]
        self.empty_init_instance._sensors_from_config_file_sections()
        pmake_sensor_from_section.assert_has_calls(expected_calls, any_order=True)

    @patch("fructosa.conf.LAgentConf._make_sensor_from_section")
    def test_sensors_attribute_contents(self, pmake_sensor_from_section):
        sections = MagicMock()
        not_sensors = [MagicMock() for _ in range(5)]
        sensors = [MagicMock() for _ in range(5)]
        def my_side_effect(section):
            if section in sensors:
                return section
            else:
                return None
        in_sections = set(sensors+not_sensors)
        sections_results = list(in_sections)
        sections.__iter__.return_value = sections_results
        self.conf.sections.return_value = sections
        pmake_sensor_from_section.side_effect = my_side_effect
        self.empty_init_instance._sensors_from_config_file_sections()
        self.assertSetEqual(set(self.empty_init_instance.sensors), set(sensors))

    def test_graphite_from_config_file_sets_graphite_attribute(self):
        with self.assertRaises(AttributeError):
            self.empty_init_instance.graphite
        self.empty_init_instance._config_file_conf = MagicMock()
        self.empty_init_instance._graphite_from_config_file()
        self.empty_init_instance.graphite

    def test_graphite_from_config_file_returns_defaults_if_missing_section(self):
        self.empty_init_instance._config_file_conf = {}
        self.empty_init_instance._graphite_from_config_file()
        graphite = self.empty_init_instance.graphite
        self.assertEqual(graphite[GRAPHITE_HOST_KEY], GRAPHITE_HOST)
        self.assertEqual(
            graphite[GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY],
            GRAPHITE_CARBON_RECEIVER_PICKLE_PORT
        )

    def test_graphite_from_config_file_give_priority_to_file_over_defaults_in_section(
            self):
        test_conf = {
            GRAPHITE_HOST_KEY: "winnipoj",
            GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY: 23452
        }
        self.empty_init_instance._config_file_conf = {GRAPHITE_SECTION: test_conf}
        self.empty_init_instance._graphite_from_config_file()
        graphite = self.empty_init_instance.graphite
        self.assertEqual(graphite[GRAPHITE_HOST_KEY], "winnipoj")
        self.assertEqual(graphite[GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY], 23452)

    def test_graphite_from_config_file_host_has_priority_over_default_in_graphite_section(self):
        test_conf = {GRAPHITE_HOST_KEY: "winnipeg"}
        self.empty_init_instance._config_file_conf = {GRAPHITE_SECTION: test_conf}
        self.empty_init_instance._graphite_from_config_file()
        graphite = self.empty_init_instance.graphite
        self.assertEqual(graphite[GRAPHITE_HOST_KEY], "winnipeg")
        self.assertEqual(
            graphite[GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY],
            GRAPHITE_CARBON_RECEIVER_PICKLE_PORT
        )

    def test_graphite_from_config_file_port_has_priority_over_default_in_graphite_section(self):
        test_conf = {GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY: 54545}
        self.empty_init_instance._config_file_conf = {GRAPHITE_SECTION: test_conf}
        self.empty_init_instance._graphite_from_config_file()
        graphite = self.empty_init_instance.graphite
        self.assertEqual(graphite[GRAPHITE_HOST_KEY], GRAPHITE_HOST)
        self.assertEqual(graphite[GRAPHITE_CARBON_RECEIVER_PICKLE_PORT_KEY], 54545)
        
    
class LMasterConfTestCase(unittest.TestCase):
    @patch("fructosa.conf.LMasterConf._post_process_configuration")
    @patch("fructosa.conf.LMasterConf._prepare_logging")
    @patch("fructosa.conf.LMasterConf._set_config_file")                
    @patch("fructosa.conf.LMasterConf._get_conf_from_config_file")
    @patch("fructosa.conf.LMasterConf._get_conf_from_command_line")
    def setUp(self, pget_cnf_frm_cmdl, pget_cnf_frm_cfgf, pset_config_file,
              pprepare_logging, ppost_process_configuration):
        self.test_class = fructosa.conf.LMasterConf
        self.empty_init_instance = self.test_class()
        #mocked_cl_parser = MagicMock()
        #self.empty_init_instance._cl_parser = mocked_cl_parser

    def test_instance_has_description_attribute(self):
        from fructosa.constants import LMASTER_DESCRIPTION
        self.assertEqual(self.empty_init_instance.description, LMASTER_DESCRIPTION)

    def test_is_subclass_of_FructosaDConf(self):
        from fructosa.conf import FructosaDConf
        self.assertTrue(issubclass(self.test_class, FructosaDConf))
        
    def test_description_is_strable(self):
        str(self.empty_init_instance)
        
    def test_instance_has_correct_default_values(self):
        from fructosa.conf import LMASTER_DEFAULT_PIDFILE
        from fructosa.constants import (
            PIDFILE_STR, ACTION_STR, CONFIGFILE_STR, LMASTER_DEFAULT_CONFIGFILE,
        )
        self.assertEqual(
            self.empty_init_instance.default_values[PIDFILE_STR], LMASTER_DEFAULT_PIDFILE)
        self.assertEqual(
            self.empty_init_instance.default_values[CONFIGFILE_STR], LMASTER_DEFAULT_CONFIGFILE
        )
        with self.assertRaises(KeyError):
            self.empty_init_instance.default_values[ACTION_STR]

    @patch("fructosa.conf.FructosaDConf._post_process_configuration")
    def test_post_process_configuration_calls_same_method_in_FructosaDConf(
            self, ppost_process_configuration):
        self.empty_init_instance._post_process_configuration()
        ppost_process_configuration.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
