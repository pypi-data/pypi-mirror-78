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

from unittest import TestCase, skip
from unittest.mock import patch, MagicMock, call, mock_open
from inspect import signature, Parameter
import os

import fructosa.daemon
from fructosa.daemon import ALREADY_RUNNING_MSG
from fructosa.constants import (
    PROTO_NO_PERMISSION_PIDFILE, PIDFILE_EXISTS, RUNNING_PROCESS_FOUND,
    PROCESS_DOES_NOT_EXIST, NO_PID_FOUND, PIDFILE_ACTION_CREATED,
)


class daemonizeTestCase(TestCase):
    def setUp(self):
        self.test_func = fructosa.daemon.daemonize
        self.pidfile_mock = MagicMock()
        
    def test_parameters(self):
        s = signature(self.test_func)
        parameters = s.parameters
        param_kinds = [param.kind for param in parameters.values()]
        self.assertEqual(len(parameters), 4)
        self.assertEqual(Parameter.POSITIONAL_OR_KEYWORD, param_kinds[0])
        for param_kind in param_kinds[1:]:
            self.assertEqual(Parameter.KEYWORD_ONLY, param_kind)

    @patch("fructosa.daemon._set_signal_handler_for_termination")
    @patch("fructosa.daemon._remove_pidfile_on_signal_or_exit")
    @patch("fructosa.daemon._create_pidfile")
    @patch("fructosa.daemon._replace_io_descriptors")
    @patch("fructosa.daemon._flush_buffers")
    @patch("fructosa.daemon.os.setsid")
    @patch("fructosa.daemon.os.umask")
    @patch("fructosa.daemon.os.chdir")
    @patch("fructosa.daemon._fork")
    @patch("fructosa.daemon._check_pidfile")
    def test_daemonize_call_sequence(
            self, pcheck_pidfile, pfork, pchdir, pumask, psetsid, pflush_buffers,
            preplace_io_descriptors, pcreate_pidfile, premove_pidfile_on_signal_or_exit,
            pset_signal_handler_for_termination):
        stdin_mock = MagicMock()
        stdout_mock = MagicMock()
        stderr_mock = MagicMock()
        manager = MagicMock()
        manager.attach_mock(pcheck_pidfile, "_check_pidfile")
        manager.attach_mock(pfork, "_fork")
        manager.attach_mock(pchdir, "chdir")
        manager.attach_mock(pumask, "umask")
        manager.attach_mock(psetsid, "setsid")
        manager.attach_mock(pcreate_pidfile, "_create_pidfile")
        manager.attach_mock(pflush_buffers, "_flush_buffers")
        manager.attach_mock(preplace_io_descriptors, "_replace_io_descriptors")
        manager.attach_mock(premove_pidfile_on_signal_or_exit, "_remove_pidfile_on_signal_or_exit")
        manager.attach_mock(pset_signal_handler_for_termination, "_set_signal_handler_for_termination")
        self.test_func(self.pidfile_mock, stdin=stdin_mock, stdout=stdout_mock, stderr=stderr_mock)
        expected_calls = [
            call._check_pidfile(self.pidfile_mock),
            call._fork(1),
            call.chdir("/"),
            call.umask(0),
            call.setsid(),
            call._fork(2),
            call._create_pidfile(self.pidfile_mock),
            call._flush_buffers(),
            call._replace_io_descriptors(stdin_mock, stdout_mock, stderr_mock),
            call._remove_pidfile_on_signal_or_exit(self.pidfile_mock),
            call._set_signal_handler_for_termination(),
        ]
        manager.assert_has_calls(expected_calls)

    @patch("fructosa.daemon.os.path.exists")
    def test_check_pidfile_calls_exists_with_pidfile(self, pexists):
        try:
            fructosa.daemon._check_pidfile(self.pidfile_mock)
        except RuntimeError:
            pass
        pexists.assert_has_calls([call(self.pidfile_mock)])

    @patch("fructosa.daemon.os.path.exists")
    def test_check_pidfile_if_pidfile_exists_and_process_found(self, pexists):
        pid = 445343453
        def ospathexists(filename):
            if filename == self.pidfile_mock:
                return True
            elif filename == "/proc/{}".format(pid):
                return True
            else:
                return False
        pexists.side_effect = ospathexists
        with self.assertRaises(RuntimeError) as e:
            with patch('fructosa.daemon.open', mock_open(read_data='{}\n'.format(pid))) as m:
                fructosa.daemon._check_pidfile(self.pidfile_mock)
        self.assertEqual(str(e.exception), ALREADY_RUNNING_MSG)
        self.assertIn(
            PIDFILE_EXISTS.format(pidfile=self.pidfile_mock), e.exception.to_warning
        )
        self.assertIn(
            RUNNING_PROCESS_FOUND.format(pid=pid), e.exception.to_warning
        )

    @patch("fructosa.daemon.os.path.exists")
    def test_check_pidfile_if_pidfile_exists_and_process_not_found(self, pexists):
        pid = 44538890
        def ospathexists(filename):
            if filename == self.pidfile_mock:
                return True
            else:
                return False
        pexists.side_effect = ospathexists
        with self.assertRaises(RuntimeError) as e:
            with patch('fructosa.daemon.open', mock_open(read_data='{}\n'.format(pid))) as m:
                fructosa.daemon._check_pidfile(self.pidfile_mock)
        self.assertEqual(str(e.exception), ALREADY_RUNNING_MSG)
        self.assertIn(
            PIDFILE_EXISTS.format(pidfile=self.pidfile_mock), e.exception.to_warning
        )
        self.assertIn(
            PROCESS_DOES_NOT_EXIST.format(pid=pid), e.exception.to_warning
        )
        
    @patch("fructosa.daemon.os.path.exists")
    def test_check_pidfile_if_pidfile_exists_but_no_pid_in_it(self, pexists):
        pid = 44538890
        def ospathexists(filename):
            if filename == self.pidfile_mock:
                return True
            else:
                return False
        pexists.side_effect = ospathexists
        with self.assertRaises(RuntimeError) as e:
            with patch('fructosa.daemon.open', mock_open(read_data='ca'.format(pid))) as m:
                fructosa.daemon._check_pidfile(self.pidfile_mock)
        self.assertEqual(str(e.exception), ALREADY_RUNNING_MSG)
        self.assertIn(
            PIDFILE_EXISTS.format(pidfile=self.pidfile_mock), e.exception.to_warning
        )
        self.assertIn(NO_PID_FOUND, e.exception.to_warning)
        
    
    @patch("fructosa.daemon.os.access")
    @patch("fructosa.daemon.os.path.exists")
    def test_check_pidfile_if_pidfile_doesnt_exist_and_can_write(self, pexists, paccess):
        pexists.return_value = False
        paccess.return_value = True
        pidfile = "/a/b/c.pid"
        fructosa.daemon._check_pidfile(pidfile)

    @patch("fructosa.daemon.os.access")
    @patch("fructosa.daemon.os.path.exists")
    def test_check_pidfile_calls_access_properly_if_pidfile_doesnt_exist(self, pexists, paccess):
        pexists.return_value = False
        pidfile = "/winnipef/gomez/ju.pid"
        fructosa.daemon._check_pidfile(pidfile)
        paccess.assert_called_once_with(
            "/winnipef/gomez", os.X_OK|os.W_OK
        )

    @patch("fructosa.daemon.os.access")
    @patch("fructosa.daemon.os.path.exists")
    def test_check_pidfile_if_pidfile_doesnt_exist_but_cannot_write(self, pexists, paccess):
        pexists.return_value = False
        paccess.return_value = False
        pidfile = "/my/funny/file.pid"
        error_msg = PROTO_NO_PERMISSION_PIDFILE.format(
            pidfile=pidfile, action=PIDFILE_ACTION_CREATED
        )
        with self.assertRaises(PermissionError) as e:
            fructosa.daemon._check_pidfile(pidfile)
        self.assertEqual(str(e.exception), f"Permission denied: '{pidfile}'")
        self.assertEqual(e.exception.to_error, error_msg)

    @patch("fructosa.daemon.os.fork")
    def test_fork_calls_osfork(self, pfork):
        def gttrue(val):
            return True
        def gtfalse(val):
            return False   
        mock_gt = MagicMock()
        for f in gttrue, gtfalse:
            mock_gt.__gt__.side_effect = f
            pfork.return_value = mock_gt        
            try:
                fructosa.daemon._fork(MagicMock())
            except SystemExit:
                pass
            pfork.assert_called_once_with()
            pfork.reset_mock()

    @patch("fructosa.daemon.os.fork")
    def test_fork_parent_exits(self, pfork):
        def gt(val):
            if val == 0:
                return True
            else:
                return False
        mock_gt = MagicMock()
        mock_gt.__gt__.side_effect = gt
        pfork.return_value = mock_gt
        with self.assertRaises(SystemExit) as e:
            fructosa.daemon._fork(MagicMock())
        self.assertEqual(e.exception.code, 0)

    @patch("fructosa.daemon.os.fork")
    def test_fork_child_does_not_exit(self, pfork):
        def gt(val):
            if val == 0:
                return False
            else:
                return True
        mock_gt = MagicMock()
        mock_gt.__gt__.side_effect = gt
        pfork.return_value = mock_gt
        fructosa.daemon._fork(MagicMock())

    @patch("fructosa.daemon.os.fork")
    def test_fork_raises_oserror(self, pfork):
        from fructosa.daemon import PRE_FORK_FAILED_MSG
        pfork.side_effect = OSError
        fork_number = MagicMock()
        with self.assertRaises(RuntimeError) as e:
            fructosa.daemon._fork(fork_number)
        self.assertEqual(str(e.exception), PRE_FORK_FAILED_MSG.format(fork_number))
        
    @patch("fructosa.daemon.sys.stdout")
    @patch("fructosa.daemon.sys.stderr")
    def test_flush_buffers(self, pstderr, pstdout):
        fructosa.daemon._flush_buffers()
        pstdout.flush.assert_called_once_with()
        pstderr.flush.assert_called_once_with()

    @patch("fructosa.daemon.sys.stderr")
    @patch("fructosa.daemon.sys.stdout")
    @patch("fructosa.daemon.sys.stdin")
    @patch("fructosa.daemon._replace_io_descriptor")
    def test_replace_io_descriptors_call_sequence(
            self, preplace_io_descriptor, pstdin, pstdout, pstderr):
        stdin_mock = MagicMock()
        stdout_mock = MagicMock()
        stderr_mock = MagicMock()
        calls = [
            call(pstdin, stdin_mock, "rb"),
            call(pstdout, stdout_mock, "ab"),
            call(pstderr, stderr_mock, "ab"),
        ]
        fructosa.daemon._replace_io_descriptors(stdin_mock, stdout_mock, stderr_mock)
        preplace_io_descriptor.assert_has_calls(calls)

    @patch("fructosa.daemon.os.dup2")
    def test_replace_io_descriptor_with(self, pdup2):
        f = MagicMock()
        mopen = mock_open()
        mopen.return_value = f
        with patch("fructosa.daemon.open", mopen):
            old = MagicMock()
            new = MagicMock()
            mode = MagicMock()
            fructosa.daemon._replace_io_descriptor(old, new, mode)
            mopen.assert_called_once_with(new, mode, 0)
            handle = mopen()
            pdup2.assert_called_once_with(handle.__enter__().fileno(), old.fileno())

    @patch("fructosa.daemon.print")
    @patch("fructosa.daemon.os.getpid")
    def test_create_pidfile(self, posgetpid, pprint):
        pid = MagicMock()
        posgetpid.return_value = pid
        pidfile = MagicMock()
        mopen = mock_open()
        with patch("fructosa.daemon.open", mopen):
            fructosa.daemon._create_pidfile(pidfile)
            mopen.assert_called_once_with(pidfile, "w")
            handle = mopen()
            f = handle.__enter__()
            pprint.assert_called_once_with(pid, file=f)

    @patch("fructosa.daemon.print")
    @patch("fructosa.daemon.os.getpid")
    def test_create_pidfile_raises_correct_exception_if_no_permission(self, posgetpid, pprint):
        pid = MagicMock()
        pidfile = MagicMock()
        posgetpid.side_effect = PermissionError("something here")
        error_msg = PROTO_NO_PERMISSION_PIDFILE.format(
            pidfile=pidfile, action=PIDFILE_ACTION_CREATED
        )
        mopen = mock_open()
        with patch("fructosa.daemon.open", mopen):
            with self.assertRaises(PermissionError) as e:
                fructosa.daemon._create_pidfile(pidfile)
        self.assertEqual(e.exception.to_error, error_msg)

    @patch("fructosa.daemon._remove_pidfile")
    @patch("fructosa.daemon.atexit.register")
    def test_remove_pidfile_on_signal_or_exit_calls_register(
            self, pregister, premove_pidfile):
        pidfile = MagicMock()
        fructosa.daemon._remove_pidfile_on_signal_or_exit(pidfile)
        pregister.assert_called_once_with(premove_pidfile, pidfile)

    @patch("fructosa.daemon.os.remove")
    def test_remove_pidfile_calls_osremove(self, posremove):
        pidfile = MagicMock()
        fructosa.daemon._remove_pidfile(pidfile)
        posremove.assert_called_once_with(pidfile)

    @patch("fructosa.daemon._sigterm_handler")
    @patch("fructosa.daemon.signal.signal")
    def test_set_signal_handler_for_termination_calls_signal(
            self, psignal, psigterm_handler):
        import signal
        fructosa.daemon._set_signal_handler_for_termination()
        psignal.assert_called_once_with(signal.SIGTERM, psigterm_handler)

    def test_sigterm_handler_arguments(self):
        from fructosa.daemon import _sigterm_handler
        s = signature(_sigterm_handler)
        parameters = s.parameters
        param_args = [param.kind for param in parameters.values()]
        expected = [Parameter.POSITIONAL_OR_KEYWORD, Parameter.POSITIONAL_OR_KEYWORD]
        self.assertListEqual(expected, param_args)

    def test_sigterm_handler_action(self):
        from fructosa.daemon import RETURN_CODE_FOR_SIGTERM
        with self.assertRaises(SystemExit) as e:
            fructosa.daemon._sigterm_handler(MagicMock(), MagicMock())
        self.assertEqual(e.exception.code, RETURN_CODE_FOR_SIGTERM)
