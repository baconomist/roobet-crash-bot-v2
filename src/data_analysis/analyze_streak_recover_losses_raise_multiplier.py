from data_utils import *
from src.apis.simulated_api import TestAPI
from src.bots.streak_bot_recover_losses_multiplier_scaled_lower_multiplier import StreakBotRecoverLossesLowerMultiplier


class Config:
    BET = 0.1
    START_MULTIPLIER = 1.58
    MIN_STREAK_SIZE = 5
    INPUT_FILE = "../simulation/roobet_crash_history.txt"
    # SIMULATED_BALANCE = None


all_crash_vals = read_crash_txt_file(Config.INPUT_FILE)
all_crash_vals.reverse()

streak_frequencies = get_streak_frequencies_lower_multiplier(Config.START_MULTIPLIER, all_crash_vals,
                                                             Config.MIN_STREAK_SIZE,
                                                             lower_multiplier_by=-0.1)
streak_frequencies_list = dict_to_sorted_key_val_pairs(streak_frequencies)
max_streak_size = max(streak_frequencies.keys())

bet_amount_per_streak_size = calc_bet_amount_per_streak_size_lower_multiplier(Config.BET, Config.START_MULTIPLIER,
                                                                              max_streak_size,
                                                                              lower_multiplier_by=-0.1)



print("STREAK_FREQUENCIES:",
      dict_to_sorted_key_val_pairs(get_streak_frequencies(Config.START_MULTIPLIER, all_crash_vals)))
print("LOWER MULTIPLIER STREAK FREQUENCIES:", streak_frequencies_list)
print("MAX_STREAK_SIZE:", max_streak_size)

