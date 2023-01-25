import time
import traceback
import random

from src.data_collectors.roobet_collector import RoobetCollector

if __name__ == "__main__":
    # TODO: SHOULD create a separate python process for each collector so that if one breaks the other one doesnt, use parallelprocess module
    # TODO: SHOULD TRY TO REFRESH PAGE IF BROKEN, else if x retries failed, spin up new instance
    collectors = [RoobetCollector()]

    # Prevent polling too often
    MIN_UPDATE_DELAY = 1
    while True:
        try:
            for collector in collectors:
                collector.update()
            time.sleep(MIN_UPDATE_DELAY + random.random())
        except:
            traceback.print_exc()
