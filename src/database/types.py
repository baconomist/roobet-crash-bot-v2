from datetime import datetime

from orator.schema import Blueprint
from pony.orm import *
from src.database import db_instance, init_db


# SHARED INTERFACE FOR CASTING
class ICrashPoint:
    id: int
    api_id: str
    crash_val: float


class RoobetCrashPoint(db_instance.Entity, ICrashPoint):
    id = PrimaryKey(int, auto=True)
    api_id = Required(str)
    crash_val = Required(float)

    def __init__(self, api_id: str, crash_val: float):
        super(RoobetCrashPoint, self).__init__(api_id=api_id, crash_val=crash_val)


class TrustDiceCrashPoint(db_instance.Entity, ICrashPoint):
    id = PrimaryKey(int, auto=True)
    api_id = Required(str)
    crash_val = Required(float)

    def __init__(self, api_id: str, crash_val: float):
        super(TrustDiceCrashPoint, self).__init__(api_id=api_id, crash_val=crash_val)


init_db(db_instance, "./database.sqlite")

if __name__ == "__main__":
    @db_session
    def test():
        c = RoobetCrashPoint(api_id="a", crash_val=1.01)
        c = TrustDiceCrashPoint(api_id="a", crash_val=1.01)

    @db_session
    def test2():
        c = select(c for c in RoobetCrashPoint).order_by(lambda c: -c.id).limit(10)[0]
        print(c.id, c.api_id, c.crash_val)

    test()
    test2()
