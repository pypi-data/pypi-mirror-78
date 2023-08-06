from urllib import request
import threading
import os
import psutil
import time
import json

import logging

log = logging.getLogger(__name__)
from athena.config import TracerConfig


def get_pid():
    os.environ.get("ATHENA_PID", None)


class MetricsThread(threading.Thread):
    REPORTING_INTERVAL = 1  # seconds
    MAX_BUFFER_SIZE = 10

    def __init__(self, event, trace_id):
        super().__init__(daemon=True)
        self.stopped = event
        self.trace_id = trace_id
        self.stats_buffer = []
        self.process = psutil.Process(get_pid())

    def flush_stats_buffer(self):
        try:
            url = TracerConfig.host + TracerConfig.metrics_url
            # default to stringifying anything not json-serializable
            data = json.dumps(
                {"id": self.trace_id, "metrics": self.stats_buffer}, default=str
            )
            payload = data.encode("utf-8")
            req = request.Request(url, data=payload)

            req.add_header("Content-Type", "application/json")
            resp = request.urlopen(req)
        except Exception as e:
            log.error("Failed to submit metrics. Still clearing buffer: %s", e)

        self.stats_buffer[:] = []

    def add_stats(self, *stats):
        self.stats_buffer.append(
            {
                "timestamp": int(time.time() * (10 ** 6)),
                "metrics": {
                    "cpu_times": stats[0],
                    "cpu_percent": stats[1],
                    "mem_info": stats[2],
                    "mem_percent": stats[3],
                    "num_threads": stats[4],
                    "num_ctx_switches": stats[5],
                    "num_open_files": stats[6],
                },
            }
        )
        if len(self.stats_buffer) >= self.MAX_BUFFER_SIZE:
            self.flush_stats_buffer()

    def log_metrics(self):
        with self.process.oneshot():
            cpu_times = self.process.cpu_times()
            cpu_percent = self.process.cpu_percent()
            mem_info = self.process.memory_info()
            mem_percent = self.process.memory_percent()
            num_threads = self.process.num_threads()
            num_ctx_switches = self.process.num_ctx_switches()

        num_open_files = len(self.process.open_files())

        self.add_stats(
            cpu_times,
            cpu_percent,
            mem_info,
            mem_percent,
            num_threads,
            num_ctx_switches,
            num_open_files,
        )

    def run(self):
        while not self.stopped.wait(self.REPORTING_INTERVAL):
            # call a function
            self.log_metrics()
