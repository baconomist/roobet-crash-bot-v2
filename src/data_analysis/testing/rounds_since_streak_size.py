from statistics import median

from matplotlib import pyplot as plt

from src.apis.simulated_api import TestAPI
from src.bots.streak_bot_recover_losses_multiplier_scaled import StreakBotRecoverLosses
from src.bots.streak_bot_recover_losses_multiplier_scaled_max_streak import StreakBotRecoverLossesMaxStreak
from src.bots.streak_bot_recover_losses_multiplier_scaled_rounds_since_streak import \
    StreakBotRecoverLossesRoundsSinceStreak
from src.bots.streak_bot_recover_losses_multiplier_scaled_rounds_since_streak_above import \
    StreakBotRecoverLossesRoundsSinceStreakAbove
from src.bots.streak_bot_rounds_since_streak import StreakBotRoundsSinceStreak
from src.data_analysis.data_utils import read_crash_txt_file, get_streak_frequencies, dict_to_sorted_key_val_pairs, \
    get_rounds_since_streak_size, get_rounds_since_streak_size_data, calc_amount_in_account_per_streak_size, bar_graph, \
    calc_bet_amount_per_streak_size, get_probability_above_multiplier


class Config:
    BET = 2000
    MULTIPLIER = 1.5
    MIN_STREAK_SIZE = 0
    INPUT_FILE = "../../simulation/roobet_crash_history_5_years.txt"
    # SIMULATED_BALANCE = None


print("LOADING DATA...")
all_crash_vals = read_crash_txt_file(Config.INPUT_FILE)
print("NUM CRASHPOINTS", len(all_crash_vals))
print("DONE LOADING DATA")
simulation_crash_vals = all_crash_vals[:10 ** 6 * 2]
# simulation_crash_vals = all_crash_vals

# Exclude real crash vals from analysis
# generated_crash_vals = all_crash_vals[len(simulation_crash_vals):]
generated_crash_vals = all_crash_vals
rounds_since_streak_size_data = get_rounds_since_streak_size_data(Config.MULTIPLIER, generated_crash_vals)

frequencies_sim = get_streak_frequencies(Config.MULTIPLIER, simulation_crash_vals)
print("BET AMOUNTS", calc_bet_amount_per_streak_size(Config.BET, Config.MULTIPLIER, max(frequencies_sim.keys())))
print("FREQUENCIES SIM:", frequencies_sim)
print("FREQUENCIES:", get_streak_frequencies(Config.MULTIPLIER, generated_crash_vals))

freqs = get_streak_frequencies(Config.MULTIPLIER, generated_crash_vals)
print("BABABABA", sum([val if 10 <= key <= 11 else 0 for key, val in freqs.items()]),
      sum([val if key > 11 else 0 for key, val in freqs.items()]))

print("AVG", rounds_since_streak_size_data['avg'])
print("MEDIAN", rounds_since_streak_size_data['median'])
print("MIN", rounds_since_streak_size_data['min'])
print("MAX", rounds_since_streak_size_data['max'])

print("ABC", get_streak_frequencies(rounds_since_streak_size_data['avg'][8],
                                    rounds_since_streak_size_data['distances'][8]))

data1 = get_rounds_since_streak_size_data(rounds_since_streak_size_data['avg'][8],
                                          rounds_since_streak_size_data['distances'][8])

api = TestAPI(simulation_crash_vals)
bot = StreakBotRecoverLossesMaxStreak(Config.BET, Config.MULTIPLIER, 10, api, 12)
api.register_new_crashpoint_listener(bot)

for i in range(len(simulation_crash_vals)):
    api.poll_new_crashpoint()
    if i % 10000 == 0:
        print(f"Simulation {i / len(simulation_crash_vals) * 100:.2f}% complete.")

print("NUM SIMULATION POINTS:", len(simulation_crash_vals))
print("PROFIT:", api.profit, api.profit / (len(simulation_crash_vals) / 2500))
print("MAX LOSS:", max(api.consecutive_losses if len(api.consecutive_losses) > 0 else [0]))
print(f"LOSS STREAKS: (ADD {Config.MIN_STREAK_SIZE})", api.loss_streak_frequencies)

# rounds_since_streak_size = get_rounds_since_streak_size(Config.MULTIPLIER, generated_crash_vals,
#                                                         13)
# bot = StreakBotRecoverLossesRoundsSinceStreakAbove(Config.BET, Config.MULTIPLIER, Config.MIN_STREAK_SIZE, api,
#                                                    get_rounds_since_streak_size_data(Config.MULTIPLIER,
#                                                                                      generated_crash_vals),
#                                                    rounds_since_streak_size)
# print(rounds_since_streak_size)
# bot = StreakBotRecoverLossesRoundsSinceStreak(Config.BET, Config.MULTIPLIER, Config.MIN_STREAK_SIZE, api,
#                                               get_rounds_since_streak_size_data(Config.MULTIPLIER, generated_crash_vals))
# bot = StreakBotRecoverLosses(Config.BET, Config.MULTIPLIER, Config.MIN_STREAK_SIZE, api)

# print(get_streak_frequencies(rounds_since_streak_size_data['median'][5], rounds_since_streak_size_data['distances'][5]))

# def recurse_until_single_distance(median, values, iterations=0):
#     print(dict_to_sorted_key_val_pairs(get_streak_frequencies(median, values)))
#     data = get_rounds_since_streak_size_data(median, values)
#     if 4 not in data['median'].keys():
#         return {'result': data, 'iterations': iterations}
#     bar_graph(range(len(values)), values)
#     return recurse_until_single_distance(data['median'][1], data['distances'][1], iterations + 1)
#
#
# print(recurse_until_single_distance(rounds_since_streak_size_data['median'][5],
#                                     rounds_since_streak_size_data['distances'][5]))

# Distances between distances of streaks of 5
# data1 = get_rounds_since_streak_size_data(rounds_since_streak_size_data['median'][1],
#                                           rounds_since_streak_size_data['distances'][1])

# print("")
# print("DATA1 MEDIAN:", data1['median'])
# print("DATA1 FREQUENCIES:", get_streak_frequencies(data1['median'][1], data1['distances'][1]))
# print("")
#
# # Distances between distances of streaks of 1 of distances of streaks of 5
# data2 = get_rounds_since_streak_size_data(data1['median'][1],
#                                           data1['distances'][1])
#
# print("DATA2 MEDIAN:", data2['median'])
# print("")
#
# data3 = get_rounds_since_streak_size_data(data2['median'][1],
#                                           data2['distances'][1])
#
# print("DATA3 MEDIAN:", data3['median'])

# print(data2)
# print(get_streak_frequencies(data2['median'][1], data2['distances'][1]))

# # Distances between streaks of 1 below median of distances between streaks of 9
# print(data['median'][1], data['distances'][1])
#
# plt.axline((0, data['median'][1]), (len(data['distances'][1]), data['median'][1]),
#            marker='o')
# bar_graph(range(len(data['distances'][1])), data['distances'][1])

# plt.axline((0, rounds_since_streak_size_data['median'][9]), (len(rounds_since_streak_size_data['distances'][9]), rounds_since_streak_size_data['median'][9]),
#            marker='o')
# bar_graph(range(len(rounds_since_streak_size_data['distances'][9])), rounds_since_streak_size_data['distances'][9])

# bar_graph(range(len(simulation_crash_vals)), simulation_crash_vals)

# print("NUM CRASH POINTS:", len(all_crash_vals))
#
# print("AMOUNT IN ACCOUNT:", calc_amount_in_account_per_streak_size(Config.BET, Config.MULTIPLIER, 15))
# freqs = get_streak_frequencies(Config.MULTIPLIER, all_crash_vals)
# print("FREQUENCIES:", freqs)
# print(sum([val if Config.MIN_STREAK_SIZE < key < 10 else 0 for key, val in freqs.items()]),
#       sum([val if key >= 10 else 0 for key, val in freqs.items()]))
#
