import time
from statistics import median

import matplotlib
from matplotlib import pyplot as plt
from pony.orm import *

from src.database.types import ICrashPoint

matplotlib.use('TkAgg')


def bar_graph(keys, values, show_for=0):
    plt.bar(keys, values, width=0.1, color=['black', 'red', 'green', 'blue', 'cyan'], edgecolor='black')
    plt.show(block=False)
    plt.pause(show_for)
    plt.close()


def get_probability_below_multiplier(multiplier):
    # https://www.youtube.com/watch?v=F1HA7e3acSI
    return 1 / 33 + 32 / 33 * (0.01 + 0.99 * (1 - 1 / multiplier))


def get_probability_above_multiplier(multiplier):
    return 1 - get_probability_below_multiplier(multiplier)


def get_probability_of_streak(multiplier, streak_size):
    return get_probability_below_multiplier(multiplier) ** streak_size


def get_probability_of_above_streak(multiplier, min_streak_size, max_streak_size):
    total = 0
    for i in range(min_streak_size, max_streak_size + 1):
        total += get_probability_of_streak(multiplier, i)
    return total


def get_actual_streak_distribution(streak_size, streak_frequencies):
    if streak_size not in streak_frequencies.keys():
        return 9999999999999

    total = 0
    for key, val in streak_frequencies.items():
        if key < streak_size:
            total += val

    return streak_frequencies[streak_size] / total


def get_actual_above_streak_distribution(min_streak_size, streak_frequencies):
    if min_streak_size not in streak_frequencies.keys():
        return -999999999999999

    total = 0
    total2 = 0
    for key, val in streak_frequencies.items():
        if key < min_streak_size:
            total += val
        else:
            total2 += val

    return total2 / total


def get_actual_distribution_above_multiplier(multiplier, values):
    count_above = 0
    count_below = 0
    for x in values:
        if x >= multiplier:
            count_above += 1
        else:
            count_below += 1

    return count_above / (count_above + count_below)


def calc_bet_amount_per_streak_size(bet, multiplier, max_streak_size):
    temp = []
    for i in range(max_streak_size + 1):
        prev_bets = []
        for k in range(i):
            prev_bets.append(sum(prev_bets) / (multiplier - 1) + bet)

        temp.append((i, round(sum(prev_bets) / (multiplier - 1) + bet, 2)))
    return temp


def calc_amount_in_account_per_streak_size(bet, multiplier, max_streak_size):
    bet_per_streak_size = calc_bet_amount_per_streak_size(bet, multiplier, max_streak_size)
    return [(key, sum([val2 if key2 <= key else 0 for (key2, val2) in bet_per_streak_size])) for (key, val) in
            bet_per_streak_size]


def calc_bet_amount_per_streak_size_lower_multiplier(bet, start_multiplier, max_streak_size, min_multiplier=1.1,
                                                     lower_multiplier_by=0.1):
    temp = []
    for i in range(max_streak_size + 1):
        multiplier = max(start_multiplier - i * lower_multiplier_by, min_multiplier)
        prev_bets = []
        for k in range(i):
            prev_bets.append(sum(prev_bets) / (multiplier - 1) + bet)

        temp.append((i, round(sum(prev_bets) / (multiplier - 1) + bet, 2)))
    return temp


def dict_to_sorted_key_val_pairs(streak_freqs):
    frequencies_list = []
    for key, val in streak_freqs.items():
        frequencies_list.append((key, val))
    # SORT GREATEST -> LEAST streak size
    frequencies_list.sort(key=lambda x: x[0])

    return frequencies_list


def get_streak_frequencies(multiplier, values):
    curr_streak_size = 0
    streak_sizes = []
    for i in range(len(values)):
        if values[i] < multiplier:
            curr_streak_size += 1
        else:
            streak_sizes.append(curr_streak_size)
            curr_streak_size = 0

    streak_frequencies = {}
    for streak_size in streak_sizes:
        if streak_size not in streak_frequencies.keys():
            streak_frequencies[streak_size] = 0
        streak_frequencies[streak_size] += 1

    return streak_frequencies


def get_streak_frequencies_lower_multiplier(start_multiplier, values, start_streak_size, min_multiplier=1.10,
                                            lower_multiplier_by=0.1):
    curr_streak_size = 0
    streak_sizes = []
    multiplier = start_multiplier
    for i in range(len(values)):
        if values[i] < multiplier:
            curr_streak_size += 1

            multiplier = start_multiplier - lower_multiplier_by * (curr_streak_size - start_streak_size)
            multiplier = max(multiplier, min_multiplier)

        elif curr_streak_size > 0:
            streak_sizes.append(curr_streak_size)
            curr_streak_size = 0
            multiplier = start_multiplier

    streak_frequencies = {}
    for streak_size in streak_sizes:
        if streak_size not in streak_frequencies.keys():
            streak_frequencies[streak_size] = 0
        streak_frequencies[streak_size] += 1

    return streak_frequencies


def calc_min_win_loss_ratio(multiplier):
    # (bet) * (mul - 1) * wins = bet * losses --> to break even
    # MIN win / loss = 1 / (mul - 1)
    win_loss_ratio = 1 / (multiplier - 1)
    return win_loss_ratio


def get_rounds_since_streak_size(multiplier, values, max_streak_size):
    rounds_since_streak_size = {}
    current_streak = 0
    for i in range(len(values)):
        finished = True
        for k in range(1, max_streak_size + 1):
            if k not in rounds_since_streak_size.keys():
                finished = False
        if finished:
            return rounds_since_streak_size

        if values[i] < multiplier:
            current_streak += 1
        else:
            if current_streak not in rounds_since_streak_size.keys():
                rounds_since_streak_size[current_streak] = i

            current_streak = 0

    return rounds_since_streak_size


def get_rounds_since_streak_size_data(multiplier, values):
    streak_indices = {}
    current_streak = 0
    for i in range(len(values)):
        if values[i] < multiplier:
            current_streak += 1
        else:
            if current_streak not in streak_indices.keys():
                streak_indices[current_streak] = [i]
            else:
                streak_indices[current_streak].append(i)

            current_streak = 0

    distances_between_streak_indices = {}
    for streak, indicies in streak_indices.items():
        distances_between_streak_indices[streak] = []
        for i in range(len(indicies) - 1):
            distances_between_streak_indices[streak].append(indicies[i + 1] - indicies[i])

        if len(indicies) == 1:
            distances_between_streak_indices[streak] = [indicies[0]]

    # median_rounds_between_streaks = {key: median(val) for key, val in distances_between_streak_indicies.items()}
    # # Remove outliers
    # for key, val in distances_between_streak_indicies.items():
    #     indicies_to_remove = []
    #     for i in range(len(val)):
    #         if val[i] / median_rounds_between_streaks[key] < 0.2:
    #             indicies_to_remove.append(i)
    #
    #     for i in indicies_to_remove[::-1]:
    #         val.pop(i)
    #
    #     distances_between_streak_indicies[key] = val

    avg_rounds_between_streaks = {key: sum(val) / len(val) for key, val in distances_between_streak_indices.items()}
    min_rounds_between_streaks = {key: min(val) for key, val in distances_between_streak_indices.items()}
    median_rounds_between_streaks = {key: median(val) for key, val in distances_between_streak_indices.items()}
    max_rounds_between_streaks = {key: max(val) for key, val in distances_between_streak_indices.items()}

    return {'distances': distances_between_streak_indices, "avg": avg_rounds_between_streaks,
            "median": median_rounds_between_streaks, "min": min_rounds_between_streaks, 'indices': streak_indices,
            'max': max_rounds_between_streaks}


def read_crash_txt_file(file_path):
    all_crash_vals = []
    with open(file_path, "r") as f:
        for l in f.readlines():
            all_crash_vals.append(float(l.split(" ")[1]))
    return all_crash_vals


def read_crash_txt_file_chunked(file_path, chunk_listener, chunk_size=10 ** 5):
    all_crash_vals = []
    with open(file_path, "r") as f:
        c = 0
        for l in f.readlines():
            all_crash_vals.append(float(l.split(" ")[1]))
            if c % chunk_size == 0:
                chunk_listener(all_crash_vals)
                all_crash_vals = []
                c = 0
            c += 1

    chunk_listener(all_crash_vals)
