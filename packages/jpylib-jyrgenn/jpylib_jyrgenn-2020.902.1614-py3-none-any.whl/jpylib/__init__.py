#!/usr/bin/env python3
# Have all support function modules here at hand.

import os
import pwd
import sys

from .pgetopt import parse as pgetopts
from .alerts import L_ERROR, L_NOTICE, L_INFO, L_DEBUG, L_TRACE, \
    alert_config, alert_level, alert_level_name, \
    alert_level_up, alert_level_zero, is_notice, is_info, is_debug, is_trace, \
    debug_vars, fatal, err, notice, info, debug, trace
from .fntrace import tracefn
from .stringreader import StringReader
from .kvs import parse_kvs
from .namespace import Namespace
from .config import Config
from .secrets import putsecret, getsecret, getsecret_main, putsecret_main
from .sighandler import sanesighandler
from .terminal import ttyi, ttyo, ptty
from .capture import outputCaptured, outputAndExitCaptured
from .process import backquote
from .assorted import boolish, flatten, is_sequence
from .assorted import maybe_int, is_int, maybe_num, is_num
from .time import isotime, iso_time, iso_time_ms, iso_time_us
from .table import format_table

version = "2020.902.1614"
program = os.path.basename(sys.argv[0])
real_home = pwd.getpwuid(os.getuid()).pw_dir
home = os.environ.get("HOME") or real_home
verbosity_option = ("verbose", alert_level_up, alert_level(L_NOTICE),
                    "increase verbosity")
