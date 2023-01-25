import hashlib
import hmac
import json

from pony.orm import db_session

from src.database import init_db
from src.database.types import RoobetCrashPoint


class Config:
    LATEST_GAME = "0002b3c14352f52ed58a3e2364e061325e5297ce521ce5e1495947fe73eaa67e"
    AVG_GAMES_24H = 2500
    YEARS_TO_GENERATE = 1


crashHash = ""
salt = "0x9b7d58e36dd542604d84c0d253f0cdd993ba193a974c32d9d50e27628a17392f"
FIRST_GAME = "8268068224d61ef1c0392f735a3ef29c38ef404ef26272c08457ca277d6c00a6"

e = pow(2, 52)


# https://www.youtube.com/watch?v=F1HA7e3acSI
def get_result(game_hash):
    hm = hmac.new(str.encode(game_hash), b'', hashlib.sha256)
    hm.update(salt.encode("utf-8"))
    h = hm.hexdigest()
    if int(h, 16) % 33 == 0:
        return 1
    h = int(h[:13], 16)
    return ((100 * e - h) / (e - h) // 1) / 100.0


def get_prev_game(hash_code):
    m = hashlib.sha256()
    m.update(hash_code.encode("utf-8"))
    return m.hexdigest()


@db_session
def commit_to_db(results):
    for r in results:
        c = RoobetCrashPoint("test_id", r[1])
    print(f"Commited {len(results)} to DB")


prev_game = Config.LATEST_GAME
results = []
crash_count = 0
max_crash_count = (365 * Config.AVG_GAMES_24H) * Config.YEARS_TO_GENERATE

while crash_count < max_crash_count:
    results.append((prev_game, get_result(prev_game)))
    prev_game = get_prev_game(prev_game)
    crash_count += 1

    if len(results) % 1000000 == 0:
        print("Generated", len(results), "results", f"{crash_count / max_crash_count * 100:.2f} percent complete.")
        commit_to_db(results)
        results = []

# while prev_game != FIRST_GAME:
#     results.append((prev_game, get_result(prev_game)))
#     prev_game = get_prev_game(prev_game)
#


commit_to_db(results)

print(f"Generated {len(results)} results.")

# print(get_result("0f6e2b8ca48c2d55b814b6d69d307584322b24b8debf680ac513590d9d99c7f9"))
