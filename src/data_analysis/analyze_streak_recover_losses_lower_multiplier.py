from data_utils import *
from src.apis.simulated_api import TestAPI
from src.bots.streak_bot_recover_losses_multiplier_scaled_lower_multiplier import StreakBotRecoverLossesLowerMultiplier


class Config:
    BET = 0.1
    START_MULTIPLIER = 2
    MIN_MULTIPLIER = 1.58
    MIN_STREAK_SIZE = 2
    INPUT_FILE = "../simulation/roobet_crash_history.txt"
    # SIMULATED_BALANCE = None


all_crash_vals = read_crash_txt_file(Config.INPUT_FILE)
all_crash_vals.reverse()

streak_frequencies = get_streak_frequencies_lower_multiplier(Config.START_MULTIPLIER, all_crash_vals,
                                                             Config.MIN_STREAK_SIZE,
                                                             min_multiplier=Config.MIN_MULTIPLIER)
streak_frequencies_list = dict_to_sorted_key_val_pairs(streak_frequencies)
max_streak_size = max(streak_frequencies.keys())

bet_amount_per_streak_size = calc_bet_amount_per_streak_size_lower_multiplier(Config.BET, Config.START_MULTIPLIER,
                                                                              max_streak_size,
                                                                              min_multiplier=Config.MIN_MULTIPLIER)
print(bet_amount_per_streak_size)

print("STREAK_FREQUENCIES:",
      dict_to_sorted_key_val_pairs(get_streak_frequencies(Config.START_MULTIPLIER, all_crash_vals)))
print("LOWER MULTIPLIER STREAK FREQUENCIES:", streak_frequencies_list)
print("MAX_STREAK_SIZE:", max_streak_size)
#
# theoretical_dist = get_probability_of_above_streak(Config.START_MULTIPLIER, 6, 11)
# current_streak = 0
# print("DISTS", theoretical_dist, get_actual_above_streak_distribution(6, streak_frequencies))
# win_count = 0
# loss_count = 0
# window = 100
# for i in range(window, 100000):
#     start = i - window
#     end = i
#     acc_dist = get_actual_above_streak_distribution(6, get_streak_frequencies(Config.START_MULTIPLIER, all_crash_vals[start:end]))
#
#     if acc_dist - theoretical_dist < -0.2:
#         if all_crash_vals[i] < Config.START_MULTIPLIER:
#             loss_count += 1
#         else:
#             win_count += 1
#
#     i += 1
#
# print(win_count, loss_count)
# print(win_count / loss_count)

# api = TestAPI(all_crash_vals)
# bot = StreakBotRecoverLossesLowerMultiplier(Config.BET, Config.START_MULTIPLIER, Config.MIN_STREAK_SIZE, api)
# api.register_new_crashpoint_listener(bot)
#
# for i in range(len(all_crash_vals)):
#     api.poll_new_crashpoint()
#
# print(api.profit)
