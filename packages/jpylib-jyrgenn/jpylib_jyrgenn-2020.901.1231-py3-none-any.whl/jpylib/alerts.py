# print alerts and other messages depending on a verbosity level

import os
import sys
import syslog
import inspect
import jpylib as y
from .config import Config

# properties of the alert levels; the decoration will be formatted with the
# locals() values
alert_levels = (
    # level name, message decoration, fd (will look up later to make output
    # capturing work)
    ("L_ERROR", "{cfg.program}: Error:", 2),
    ("L_NOTICE", None,                     2),
    ("L_INFO",   None,                     2),
    ("L_DEBUG",  "DBG",                    2),
    ("L_TRACE",  "TRC",                    2),
)
for i, props in enumerate(alert_levels):
    name, *_ = props
    locals()[name] = i

# the module configuration; will be initialised in alert_init()
cfg = None

def alert_config(*, decoration=None, fd=None, level=None, program=None,
                 syslog_facility=None, syslog_prio=None, reset_defaults=None,
                 timestamps=None):
    """Reset everything to the specified or default values."""
    global cfg
    if not any(locals().values()) or reset_defaults:
        cfg = Config(
            # decoration to print before a message, per level
            decoration=[level[1] for level in alert_levels],
            
            # program name to use in a message
            program=os.path.basename(sys.argv[0]),
            
            # syslog facility; if set, syslog will be used
            syslog_facility=None,

            # syslog priority
            syslog_prio = [
                syslog.LOG_ERR,
                syslog.LOG_NOTICE,
                syslog.LOG_INFO,
                syslog.LOG_DEBUG,
                None,                   # don't let this go to syslog
            ],
            
            # status: syslog has been opened
            syslog_opened=False,
            
            # fd to print message to, per level
            fd=[level[2] for level in alert_levels],

            # current alert level
            level=L_NOTICE,
            
            # maximum alert level
            max_level=len(alert_levels)-1,

            # print timestamps with messages
            timestamps=False,

            # had any errors yet?
            had_errors=False,
        )
    del reset_defaults
    for var, value in locals().items():
        if value is not None:
            cfg.set(var, value)
    if cfg.timestamps is True:
        cfg.timestamps = y.isotime

def alert_init(**kwargs):
    alert_config(reset_defaults=True, **kwargs)

alert_init()


def alert_redirect(level, file):
    """Redirect printing of alerts from `level` to `file`."""
    cfg.fd[level] = file


def alert_level(level=None):
    """Get or set the verbosity level for the alert functions.

    err() will print something with level 0 (and greater), i.e. always.
    notice() will print something with level 1 (and greater).
    info() will print something with level 2 (and greater).
    debug() will print something with level 3 (and greater).
    trace() will print something with level 4 (and greater).
    """
    if level is not None:
        if type(level) is str:
            level = globals()[level]
        cfg.level = max(0, min(level, cfg.max_level))
    return cfg.level

def alcf():
    return cfg

def alert_level_name(level=None):
    """Return the name of the specified (or current) level number."""
    if level is None:
        level = cfg.level
    return alert_levels[level][0]


def alert_level_up():
    """Increase the alert level by one.

    This is intended to be used as the callback function for the default value
    of a pgetopt option to increase the verbosity.

    """
    if cfg.level < cfg.max_level:
        cfg.level += 1
    return cfg.level


def alert_level_zero():
    """Set the alert level to zero (errors only).

    This is intended to be used as the callback function for the default value
    of a pgetopt option to set the verbosity to zero.

    """
    cfg.level = 0
    return cfg.level


def is_notice():
    """Return True iff the alert level is at least at notice."""
    return cfg.level >= L_NOTICE

def is_info():
    """Return True iff the alert level is at least at info."""
    return cfg.level >= L_INFO

def is_debug():
    """Return True iff the alert level is at least at debugging."""
    return cfg.level >= L_DEBUG

def is_trace():
    """Return True iff the alert level is at least at tracing."""
    return cfg.level >= L_TRACE


def alert_if_level(level, *msgs):
    """Print a message if `level` is <= the cfg.level.

    If a decoration exists in `cfg.decoration[]` for that level, is it prepended
    to the message. By default, all levels print to stderr; this can be changed
    in `cfg.fd[]` by level.

    If one of the elements in `msgs` is a callable, it will be called withaout
    arguments to get the value of the element. This way, compute-intensive task
    can be delayed to the alerting moment, meaning they don't need to be done if
    not called for.

    """
    # return fast if not needed
    if level > cfg.level:
        return

    # make all msgs elements strings, calling those that are callable
    msgs = list(msgs)                   # is a tuple before
    for i, elem in enumerate(msgs):
        if callable(elem):
            msgs[i] = elem()
        else:
            msgs[i] = str(elem)
    if cfg.decoration[level]:
        msgs = [cfg.decoration[level].format(**globals()), *msgs]
    if cfg.timestamps:
        msgs.insert(0, cfg.timestamps())

    channel = cfg.fd[level]
    channel = { 1: sys.stdout, 2: sys.stderr }.get(channel) or channel

    msgtext = " ".join(msgs).rstrip()
    print(msgtext, file=channel, flush=True)

    if cfg.syslog_facility and cfg.syslog_prio[level]:
        if not cfg.syslog_opened:
            syslog.openlog(logoption=syslog.LOG_PID,
                           facility=cfg.syslog_facility)
            cfg.syslog_opened = True
        level = max(0, min(cfg.max_level, level))
        message = " ".join(map(str, msgs))
        syslog.syslog(cfg.syslog_prio[level], message)


def debug_vars(*vars):
    """Print debug output for the named variables if alert level >= L_DEBUG."""
    if cfg.level >= L_DEBUG:
        context = inspect.currentframe().f_back.f_locals
        for var in vars:
            debug("VAR {}: {}".format(var, repr(context[var])))


def err(*msgs):
    """Print error level output."""
    cfg.had_errors = True
    alert_if_level(L_ERROR, *msgs)
error = err                             # alias

def fatal(*msgs, exit_status=1):
    """Print error level output."""
    alert_if_level(L_ERROR, "Fatal", *msgs)
    sys.exit(exit_status)

def notice(*msgs):
    """Print notice level output according to alert level."""
    alert_if_level(L_NOTICE, *msgs)

def info(*msgs):
    """Print info level output according to alert level."""
    alert_if_level(L_INFO, *msgs)

def debug(*msgs):
    """Print debug level output according to alert level."""
    alert_if_level(L_DEBUG, *msgs)
dbg = debug                             # alias

def trace(*msgs):
    """Print debug level output according to alert level."""
    alert_if_level(L_TRACE, *msgs)

# EOF
