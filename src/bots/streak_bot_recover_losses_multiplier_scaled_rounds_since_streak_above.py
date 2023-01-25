import traceback

from src.bots.streak_bot_recover_losses_multiplier_scaled import StreakBotRecoverLosses
from src.bots.types import IBot
from src.data_analysis.data_utils import get_rounds_since_streak_size, get_rounds_since_streak_size_data


class StreakBotRecoverLossesRoundsSinceStreakAbove(StreakBotRecoverLosses):

    def __init__(self, bet, multiplier, streak_size, api, rounds_since_streak_size_data, current_rounds_since_streak_size):
        super().__init__(bet, multiplier, streak_size, api)
        self.rounds_since_streak_size_data = rounds_since_streak_size_data

        self.rounds_since_streak_size = current_rounds_since_streak_size
        self.did_start_bet_streak = False

    def on_new_crash(self, crash_val):
        self.api.log("New Crash Val:", crash_val)

        if crash_val >= self.multiplier:
            if self.current_streak > 0:
                self.rounds_since_streak_size[self.current_streak] = 0

            self.did_start_bet_streak = False

        for i in range(11):
            if i not in self.rounds_since_streak_size.keys():
                self.rounds_since_streak_size[i] = 0
            self.rounds_since_streak_size[i] += 1

        self.update_streak_count(crash_val)

        is_less_than_median = True
        for key, val in self.rounds_since_streak_size.items():
            if key < 10:
                continue

            if key not in self.rounds_since_streak_size_data:
                continue

            if self.rounds_since_streak_size[key] > self.rounds_since_streak_size_data['median'][key]:
                is_less_than_median = False
                break

        self.did_just_bet = False
        if (is_less_than_median and self.current_streak == self.min_streak_size) or self.did_start_bet_streak:
            self.place_bet()
            self.did_just_bet = True
            self.did_start_bet_streak = True
