from typing import List
import requests

from src.database.types import ICrashPoint


class ICrashpointReceiver:
    def on_new_crash(self, crash_point: ICrashPoint):
        raise NotImplementedError()


class IBot(ICrashpointReceiver):
    pass
