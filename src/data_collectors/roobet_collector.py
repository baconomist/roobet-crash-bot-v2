import random
import time
import traceback
from typing import Callable

from pony.orm import *

import logging

from src.bots.types import ICrashpointReceiver
from src.database.types import CrashPoint
from src.global_logging import init_logging

init_logging()
logger = logging.getLogger(__file__)


class RoobetCollector(ICrashpointReceiver):
    def __init__(self):
        self.api = RoobetAPI()
        self.api.register_new_crashpoint_listener(self)

    @db_session
    def on_new_crashpoint(self, crash_point: CrashPoint):
        # TODO: WHY -c.id???
        db_crashpoints = select(c for c in CrashPoint).order_by(lambda c: -c.id).limit(10)[:]
        logger.info("Newest DB CrashPoints new->old:", [c.crash_val for c in db_crashpoints])
        logger.info("Num DB CrashPoints:", CrashPoint.select().count())

        CrashPoint(crash_val=crash_point.crash_val, api_id=crash_point.id)
        logger.info("Added new CrashPoints to db:", crash_point.crash_val)

        # TODO: WHY .reverse()?
        db_crashpoints.reverse()

    def update(self):
        self.api.poll_new_crashpoint()
