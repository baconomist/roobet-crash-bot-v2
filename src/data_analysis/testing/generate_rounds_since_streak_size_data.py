import json

from src.data_analysis.data_utils import read_crash_txt_file, get_rounds_since_streak_size_data

print("Loading Data...")
all_crash_vals = read_crash_txt_file("../../simulation/roobet_crash_history_100_years.txt")
print("Done Loading Data")

with open("output.json", "w") as f:
    json.dump(get_rounds_since_streak_size_data(1.58, all_crash_vals), f)