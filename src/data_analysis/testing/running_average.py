from statistics import median

from src.data_analysis.data_utils import read_crash_txt_file, bar_graph, calc_min_win_loss_ratio


class Config:
    BET = 0.1
    MULTIPLIER = 1.5
    MIN_STREAK_SIZE = 0
    INPUT_FILE = "../../simulation/roobet_crash_history_5_years.txt"
    # SIMULATED_BALANCE = None


print("LOADING DATA...")
all_crash_vals = read_crash_txt_file(Config.INPUT_FILE)
print("DONE LOADING DATA")
simulation_crash_vals = all_crash_vals[:10 ** 6]

running_avg = 0
n = 1
i = 0
WINDOW = 25
running_averages = []
values_after_averages = []
win = 0
loss = 0
random_win = 0
random_loss = 0
for x in simulation_crash_vals[:len(simulation_crash_vals) - 1]:
    running_avg = (running_avg * n + x) / n
    n += 1

    if n % WINDOW == 0:
        # print(running_avg, simulation_crash_vals[i - 5:i + 5])
        if simulation_crash_vals[i + 1] < 100:
            values_after_averages.append(simulation_crash_vals[i + 1])
            running_averages.append(running_avg)

        n = 1
        running_avg = 0

    if simulation_crash_vals[i + 1] > Config.MULTIPLIER:
        random_win += 1
    else:
        random_loss += 1

    i += 1

# print("MIN WIN/LOSS", calc_min_win_loss_ratio(Config.MULTIPLIER))
# print("ACC WIN/LOSS", win / loss, win, loss)
# print("RANDOM WIN/LOSS", random_win / random_loss, random_win, random_loss)
# print("MEDIAN OF AVERAGES", median(running_averages), min(running_averages))
# bar_graph(range(len(running_averages)), running_averages)
bar_graph(values_after_averages[:10000], running_averages[:10000])
