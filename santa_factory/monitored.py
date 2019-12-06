from contextlib import contextmanager
from functools import wraps
from types import MethodType


class Monitored:
    def _do(self, action: str):
        """Monitored action caught by Monitor"""
        pass

    @contextmanager
    def _do_long(self, action: str):
        """For long actions"""
        self._do(f"begin {action}")
        yield
        self._do(f"end {action}")


class Monitor:
    @staticmethod
    def print(msg: str):
        """Print the monitored thing"""
        print(msg)

    def monitor(self, monitored: Monitored):
        """Monitor a thing"""
        _do = monitored._do

        @wraps(_do)
        def do(this: Monitored, action: str):
            _do(action)
            self.print(f"{this}: {action}")

        monitored._do = MethodType(do, monitored)  # type: ignore
