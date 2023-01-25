from pony.orm import *

from src.apis.simulated_api import TestAPI
from src.bots.streak_bot_recover_losses_multiplier_scaled_max_streak import StreakBotRecoverLossesMaxStreak
from src.data_analysis.data_utils import read_crash_txt_file, get_streak_frequencies, dict_to_sorted_key_val_pairs, \
    get_rounds_since_streak_size, get_rounds_since_streak_size_data, calc_amount_in_account_per_streak_size, bar_graph
from src.database.types import RoobetCrashPoint


# TODO: get distances between wins and run that recursive

# TODO: for 100 years see if betting on 10 streak is profitable

def get_crash_vals(start_index, chunk_size):
    print("Getting crash vals...")
    result = RoobetCrashPoint.select().order_by(lambda c: c.id).limit(chunk_size, offset=start_index)[:]
    result = [c.crash_val for c in result]
    print(f"Got {len(result)} crash vals.")
    return result


with db_session:
    frequencies = {}

    profit = 0
    max_loss = 0

    bet = 500
    multiplier = 1.5
    chunk_size = 10 ** 6
    for i in range(10 * 10 - 1):
        crash_vals = get_crash_vals(i * chunk_size, chunk_size)
        print(get_streak_frequencies(multiplier, crash_vals))

        api = TestAPI(crash_vals)
        bot = StreakBotRecoverLossesMaxStreak(bet, multiplier, 11, api, 12)
        api.register_new_crashpoint_listener(bot)

        for i in range(len(crash_vals)):
            api.poll_new_crashpoint()

        profit += api.profit
        if max_loss < max(api.consecutive_losses):
            max_loss = max(api.consecutive_losses)

        print("NUM SIMULATION POINTS:", len(crash_vals))
        print("PROFIT:", api.profit, api.profit / (len(crash_vals) / 2500))
        print("MAX LOSS:", max(api.consecutive_losses if len(api.consecutive_losses) > 0 else [0]))
        print(f"LOSS STREAKS:", api.loss_streak_frequencies)

        print("TOTAL PROFIT:", profit)
        print("OVERALL MAX LOSS:", max_loss)

        # frequencies_tmp = get_streak_frequencies(multiplier, crash_vals)
        # for key, val in frequencies_tmp.items():
        #     if key not in frequencies.keys():
        #         frequencies[key] = 0
        #     frequencies[key] += val
        #
        # print(frequencies)
