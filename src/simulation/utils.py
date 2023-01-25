import time

import matplotlib
from matplotlib import pyplot as plt
from pony.orm import *

from src.database.types import CrashPoint

matplotlib.use('TkAgg')


class Window(object):
    def __init__(self, min: int, max: int = None):
        if max is None:
            max = Window.get_max_window()

        self.size = max - min

    @staticmethod
    def get_max_window():
        return Window(get_crashpoint_count())


def bar_graph(keys, values, show_for=0):
    plt.bar(keys, values, width=0.1, color=['black', 'red', 'green', 'blue', 'cyan'], edgecolor='black')
    plt.show(block=False)
    plt.pause(show_for)
    plt.close()


def get_optimal_streak_size_all_data_slow(multiplier, min_streak_freq=1):
    crash_vals = get_crashpoint_values(Window.get_max_window())
    all_streak_data = get_streak_data(multiplier, crash_vals)
    streak_frequencies = all_streak_data[2]
    frequencies_list = get_streak_frequencies_list_sorted(streak_frequencies)

    return get_optimal_streak_size(multiplier, streak_frequencies, frequencies_list, min_streak_freq=min_streak_freq)


"""
:returns (optimal streak size, optimal win loss ratio)
"""


def get_optimal_streak_size(multiplier, streak_freqs, freq_list, min_streak_freq=1):
    max_win_loss_ratio = -1
    max_win_loss_streak_size = -1
    for i in range(len(freq_list) - 1, -1, -1):
        streak_size = freq_list[i][0]
        curr_streak_freq = freq_list[i][1]

        sum_streak_frequencies_of_streaks_bigger_than_current = sum(
            [(x[1] if x[0] > streak_size else 0) for x in freq_list])

        # Don't include biggest streak since that's always guaranteed to have the max(infinite) win_loss ratio
        # and causes a division by 0
        if sum_streak_frequencies_of_streaks_bigger_than_current == 0:
            continue

        win_loss_ratio = streak_freqs[streak_size] / sum_streak_frequencies_of_streaks_bigger_than_current

        if win_loss_ratio > max_win_loss_ratio and curr_streak_freq >= min_streak_freq:
            max_win_loss_ratio = win_loss_ratio
            max_win_loss_streak_size = streak_size

    min_win_loss = calc_min_win_loss_ratio(multiplier)
    if min_win_loss > max_win_loss_ratio and freq_list[-1][1] >= min_streak_freq:
        return freq_list[-1][0], min_win_loss, True

    return max_win_loss_streak_size, max_win_loss_ratio, False


def calculate_frequency_below_multiplier(multiplier, window):
    return calculate_frequency_below_multiplier_values(multiplier, get_crashpoint_values(window))


def calculate_frequency_below_multiplier_values(multiplier, values):
    count = 0
    for val in values:
        if val < multiplier:
            count += 1

    return count / len(values)


def get_streak_frequencies_list_sorted(streak_freqs):
    frequencies_list = []
    for key, val in streak_freqs.items():
        frequencies_list.append((key, val))
    # SORT GREATEST -> LEAST streak size
    frequencies_list.sort(key=lambda x: x[0])

    return frequencies_list


def calculate_frequency_below_multiplier_avg_chunked(multiplier, chunk_size: Window):
    values = get_crashpoint_values(Window.get_max_window())
    frequencies = []
    for i in range(len(values)):
        frequencies.append(calculate_frequency_below_multiplier_values(multiplier, values[i:i + chunk_size.size]))
    return sum(frequencies) / len(frequencies)


def get_streak_data(multiplier, values):
    curr_streak_size = 0
    streak_sizes = []
    for i in range(len(values)):
        if values[i] < multiplier:
            curr_streak_size += 1
        elif curr_streak_size > 0:
            streak_sizes.append(curr_streak_size)
            curr_streak_size = 0

    streak_frequencies = {}
    for streak_size in streak_sizes:
        if streak_size not in streak_frequencies.keys():
            streak_frequencies[streak_size] = 0
        streak_frequencies[streak_size] += 1

    return round(sum(streak_sizes) / (len(streak_sizes) + 1E-100)), max(streak_sizes), streak_frequencies


def get_streak_end_indicies(multiplier, values):
    streak_freq = get_streak_data(multiplier, values)[2]

    streak_indicies = {}
    for key in streak_freq.keys():
        streak_indicies[key] = []

    curr_streak_size = 0
    for i in range(len(values)):
        val = values[i]
        if val < multiplier:
            curr_streak_size += 1
        elif curr_streak_size > 0:
            streak_indicies[curr_streak_size].append(i)
            curr_streak_size = 0

    return streak_indicies


def calc_min_win_loss_ratio(multiplier):
    # (bet) * (mul - 1) * wins = bet * losses --> to break even
    # MIN win / loss = 1 / (mul - 1)
    win_loss_ratio = 1 / (multiplier - 1)
    return win_loss_ratio


@db_session
def get_crashpoint_values(window: Window):
    # return [1.0, 1.0, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2, 1.2]
    num_points = select(c for c in CrashPoint).count()
    window_size = window.size if window.size > 0 else num_points
    return [c.crash_val for c in select(c for c in CrashPoint)[num_points - window_size:num_points]]


@db_session
def get_crashpoint_count():
    return select(c for c in CrashPoint).count()
