from typing import List, Callable

import requests

from src.bots.types import ICrashpointReceiver
from src.database.types import ICrashPoint


class API:
    def __init__(self):
        self.crashpoint_listeners: [ICrashpointReceiver] = []

    # TODO: CRASH VALS OR APIICrashpointS?
    def register_new_crashpoint_listener(self, listener: ICrashpointReceiver):
        self.crashpoint_listeners.append(listener)

    def _notify_crashpoint_listeners(self, new_crashpoint: ICrashPoint):
        for listener in self.crashpoint_listeners:
            listener: ICrashpointReceiver
            listener.on_new_crash(new_crashpoint)

    def _on_new_crashpoint(self, new_crashpoint: ICrashPoint):
        self._notify_crashpoint_listeners(new_crashpoint)

    def _get_recent_crashpoints_crash_api(self) -> List[ICrashPoint]:
        raise NotImplementedError()

    def _get_recent_crashpoints_local_server_db(self) -> List[ICrashPoint]:
        recent_crashpoints_dat = [requests.get(global_config.data_server_url + "/get_most_recent_crash").json()]

        recent_api_crashpoints: List[ICrashPoint] = []
        for x in recent_crashpoints_dat:
            recent_api_crashpoints.append(ICrashPoint(x['crashpoint'], x['id']))

        return recent_api_crashpoints

    def poll_new_crashpoint(self):
        raise NotImplementedError()

    def place_bet(self, bet, multiplier):
        raise NotImplementedError()

    def log(self, *args):
        print(*args)