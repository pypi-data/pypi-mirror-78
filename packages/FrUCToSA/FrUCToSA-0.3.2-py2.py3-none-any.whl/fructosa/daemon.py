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
import sys
import atexit
import signal

from fructosa.constants import (
    PROTO_NO_PERMISSION_PIDFILE, PIDFILE_EXISTS, RUNNING_PROCESS_FOUND,
    PROCESS_DOES_NOT_EXIST, NO_PID_FOUND, PIDFILE_ACTION_CREATED,
    ALREADY_RUNNING_MSG,
)

PRE_FORK_FAILED_MSG = 'fork #{} failed.'
RETURN_CODE_FOR_SIGTERM = 1


def daemonize(pidfile, *, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):#, to_stop=None):
    _check_pidfile(pidfile)
    _fork(1)
    os.chdir("/")
    os.umask(0)
    os.setsid()
    _fork(2)
    # _create_pidfile used to be called after _replacing_io_descriptors, BUT
    # that prevented to see errors occuring while _create_pidfile was called,
    # so I moved _create_pidfile immediately after _fork(2)
    _create_pidfile(pidfile)
    _flush_buffers()
    _replace_io_descriptors(stdin, stdout, stderr)
    _remove_pidfile_on_signal_or_exit(pidfile)
    _set_signal_handler_for_termination()

    
def _check_pidfile(pidfile):
    #  This function is a bit LBYL-ish. It looks ugly, but I think is not
    # completely bad:
    # after forking (later) it is difficult to get exit codes back. But
    # a simple check can solve the problem. And is not a big deal. Also the FTs
    # require it. On the other hand, if I don't pass the exit code to the user
    # who tried to call the program she/he can legitimately ask why.
    #                                                  -- DPalao, 11feb19
    if os.path.exists(pidfile):
        e = RuntimeError(ALREADY_RUNNING_MSG)
        try:
            pid = int(open(pidfile).read().strip())
        except ValueError:
            pid = None
        e.to_warning = [PIDFILE_EXISTS.format(pidfile=pidfile)]
        if pid:
            if os.path.exists("/proc/{}".format(pid)):
                e.to_warning.append(RUNNING_PROCESS_FOUND.format(pid=pid))
            else:
                e.to_warning.append(PROCESS_DOES_NOT_EXIST.format(pid=pid))
        else:
            e.to_warning.append(NO_PID_FOUND)
        raise e
    if not os.access(os.path.dirname(pidfile), os.X_OK|os.W_OK):
        e = PermissionError(f"Permission denied: '{pidfile}'")
        e.to_error = PROTO_NO_PERMISSION_PIDFILE.format(
            pidfile=pidfile, action=PIDFILE_ACTION_CREATED
        )
        raise e
    
def _fork(fork_number):
    try:
        if os.fork() > 0:
            raise SystemExit(0)# this is the point, check it with 0 -> 45
    except OSError:
        raise RuntimeError(PRE_FORK_FAILED_MSG.format(fork_number))
        
def _flush_buffers():
    sys.stdout.flush()
    sys.stderr.flush()

def _replace_io_descriptors(stdin, stdout, stderr):
    _replace_io_descriptor(sys.stdin, stdin, "rb")
    _replace_io_descriptor(sys.stdout, stdout, "ab")
    _replace_io_descriptor(sys.stderr, stderr, "ab")
    
def _replace_io_descriptor(old, new, mode):
    with open(new, mode, 0) as f:
        os.dup2(f.fileno(), old.fileno())
    
def _create_pidfile(pidfile):
    try:
        with open(pidfile, "w") as f:
            print(os.getpid(), file=f)
    except PermissionError as e:
        e.to_error = PROTO_NO_PERMISSION_PIDFILE.format(
            pidfile=pidfile, action=PIDFILE_ACTION_CREATED
        )
        raise e

def _remove_pidfile_on_signal_or_exit(pidfile):
    atexit.register(_remove_pidfile, pidfile)

def _remove_pidfile(pidfile):
    os.remove(pidfile)
    
def _set_signal_handler_for_termination():
    signal.signal(signal.SIGTERM, _sigterm_handler)

def _sigterm_handler(signo, frame):
    raise SystemExit(RETURN_CODE_FOR_SIGTERM)

