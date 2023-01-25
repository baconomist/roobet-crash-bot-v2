import json

from src.apis.simulated_api import TestAPI
from src.bots.streak_bot_recover_losses_multiplier_scaled_rounds_since_streak import \
    StreakBotRecoverLossesRoundsSinceStreak
from src.data_analysis.data_utils import read_crash_txt_file, get_rounds_since_streak_size_data, \
    read_crash_txt_file_chunked, get_rounds_since_streak_size

with open('rounds_since_streak_size_100_years.json', 'r') as f:
    rounds_since_streak_size_data = json.load(f)


def on_chunk(chunk):
    api = TestAPI(chunk)
    bot = StreakBotRecoverLossesRoundsSinceStreak(0.1, 1.58, 0, api,
                                                  rounds_since_streak_size_data,
                                                  get_rounds_since_streak_size(1.58, chunk, 15))
    api.register_new_crashpoint_listener(bot)

    for i in range(len(chunk)):
        api.poll_new_crashpoint()
        if i % 10000 == 0:
            print(f"Simulation {i / len(chunk) * 100:.2f}% complete.")

    print("NUM SIMULATION POINTS:", len(chunk))
    print("PROFIT:", api.profit, api.profit / (len(chunk) / 2500))
    print("MAX LOSS:", max(api.consecutive_losses if len(api.consecutive_losses) > 0 else [0]))
    print(f"LOSS STREAKS:", api.loss_streak_frequencies)


all_crash_vals = read_crash_txt_file_chunked("../../simulation/roobet_crash_history_100_years.txt", on_chunk)
