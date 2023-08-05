"""Trace code, so that libpymemprofile_api know's where we are."""

import atexit
from ctypes import PyDLL
from datetime import datetime
import os
import sys
import threading
import webbrowser
from contextlib import contextmanager

from ._utils import timestamp_now, library_path
from ._report import render_report

preload = PyDLL(library_path("_filpreload"))
preload.fil_initialize_from_python()


def start_tracing(output_path: str):
    """Start tracing allocations."""
    path = os.path.join(output_path, timestamp_now()).encode("utf-8")
    preload.fil_reset(path)
    threading.setprofile(_start_thread_trace)
    preload.register_fil_tracer()


def _start_thread_trace(frame, event, arg):
    """Trace function that can be passed to sys.settrace.

    All this does is register the underlying C trace function, using the
    mechanism described in
    https://github.com/nedbat/coveragepy/blob/master/coverage/ctracer/tracer.c's
    CTracer_call.
    """
    if event == "call":
        preload.register_fil_tracer()
    return _start_thread_trace


def stop_tracing(output_path: str) -> str:
    """Finish tracing allocations, and dump to disk.

    Returns path to the index HTML page of the report.
    """
    sys.setprofile(None)
    threading.setprofile(None)
    preload.fil_shutting_down()
    return create_report(output_path)


def create_report(output_path: str) -> str:
    now = datetime.now()
    output_path = os.path.join(output_path, now.isoformat(timespec="milliseconds"))
    preload.fil_dump_peak_to_flamegraph(output_path.encode("utf-8"))
    return render_report(output_path, now)


def trace_until_exit(code, globals_, output_path: str):
    """
    Given code (Python or code object), run it under the tracer until the
    program exits.
    """

    def shutdown():
        index_path = stop_tracing(output_path)
        print("=fil-profile= Wrote HTML report to " + index_path, file=sys.stderr)
        try:
            webbrowser.open("file://" + os.path.abspath(index_path))
        except webbrowser.Error:
            print(
                "=fil-profile= Failed to open browser. You can find the new run at:",
                file=sys.stderr,
            )
            print("=fil-profile= " + index_path, file=sys.stderr)

    # Use atexit rather than try/finally so threads that live beyond main
    # thread also get profiled:
    atexit.register(shutdown)
    start_tracing(output_path)
    exec(code, globals_, None)
