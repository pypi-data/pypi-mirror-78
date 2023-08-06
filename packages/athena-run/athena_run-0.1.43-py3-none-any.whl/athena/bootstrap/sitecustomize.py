"""
Bootstrapping code that is run when using the `athena-run` Python entrypoint
Add all monkey-patching that needs to run by default here
"""
from __future__ import print_function

import logging

log = logging.getLogger(__name__)

import threading

from athena.metrics import MetricsThread

try:
    from athena.patch import patch_all

    patch_all()  # noqa

    from athena.patch.statsd_config import DEFAULT_STATSD_CLIENT as stats
    from athena.tracing import DefaultContext

    _main_timer = stats.timer("main")
    setattr(stats, "_main_timer", _main_timer)
    _main_timer.start()
    stop = threading.Event()
    thread = MetricsThread(stop, DefaultContext.trace_id)
    thread.start()
    setattr(stats, "_metrics_thread", thread)
    setattr(stats, "_metrics_stop", stop)
except Exception as e:
    log.exception(e)
    log.warning("errors configuring Athena tracing")
