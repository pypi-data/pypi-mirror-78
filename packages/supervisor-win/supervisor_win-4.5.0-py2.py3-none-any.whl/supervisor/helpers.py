"""
Extension of existing classes by changing or adding behaviors.
"""

import random
import sys

import subprocess
import threading

from supervisor.compat import as_string

__author__ = 'alex'


class DummyPopen(object):
    """Test process"""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.pid = random.randint(1, 500)
        self.returncode = 0


class Popen(subprocess.Popen):
    """
    Opens a new process (just as subprocess), but lets you know when the
    process was killed (using the kill attribute).
    """

    @property
    def message(self):
        if self.returncode is None:
            return 'still running'
        if self.returncode == 0:
            msg = "termination normal"
        elif self.returncode < 0:
            msg = "termination by signal"
        else:
            msg = "exit status %s" % (self.returncode,)
        return msg

    def kill2(self, sig, as_group=False):
        if as_group:
            return self.taskkill()
        else:
            return self.send_signal(sig)

    def taskkill(self):
        """Kill process group"""
        output = subprocess.check_output(['taskkill',
                                          '/PID',  str(self.pid),
                                          '/F', '/T'])
        return as_string(output, encoding=sys.getfilesystemencoding(), ignore=True).strip()


class StreamAsync(threading.Thread):
    """
    Class of asynchronous reading of stdout data, stderr of a process
    """

    def __init__(self, stream, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.setDaemon(True)
        self.stream = stream
        self.queue = set()
        self._event = threading.Event()
        self.mutex = threading.Lock()
        self.res_put = threading.Condition(self.mutex)
        self.res_get = threading.Condition(self.mutex)

    def __getattr__(self, item):
        return getattr(self.stream, item)

    def run(self):
        while not self._event.is_set():
            try:
                data = self.stream.readline()
            except (IOError, ValueError):
                # occurs when the supervisor is
                # restarted with the reload command
                break
            if not data:
                break
            self.res_put.acquire()
            try:
                self.queue.add(data)
                self.res_put.wait()
            finally:
                self.res_put.release()

    def close(self):
        """Stops thread execution"""
        self._event.set()
        self.readline()

    def readline(self):
        """read one line from queue"""
        self.res_get.acquire()
        try:
            return self.queue.pop()
        except KeyError:
            return None
        finally:
            self.res_put.notify()
            self.res_get.release()
