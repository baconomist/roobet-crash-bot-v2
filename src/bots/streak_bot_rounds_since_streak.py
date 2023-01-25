import traceback

from src.bots.streak_bot_recover_losses_multiplier_scaled import StreakBotRecoverLosses
from src.bots.types import IBot
from src.data_analysis.data_utils import get_rounds_since_streak_size, get_rounds_since_streak_size_data


class StreakBotRoundsSinceStreak(IBot):

    def __init__(self, bet, multiplier, streak_size, api, rounds_since_streak_size_data,
                 latest_rounds_since_streak_size):
        self.bet = bet
        self.multiplier = multiplier
        self.min_streak_size = streak_size
        self.api = api

        self.current_streak = 0
        self.did_just_bet = False
        self.api.log("BOT CREATED. BET: {0} MULTIPLIER: {1} STREAK_SIZE: {2}".format(bet, multiplier, streak_size))

        self.rounds_since_streak_size_data = rounds_since_streak_size_data

        self.rounds_since_streak_size = latest_rounds_since_streak_size
        self.did_start_bet_streak = False

    def update_streak_count(self, crash_val):
        if crash_val < self.multiplier:
            self.current_streak += 1
            self.api.log("Current Streak:", self.current_streak)
        else:
            self.api.log("Resetting Streak to 0")
            self.current_streak = 0
            self.prev_bets = []

    def place_bet(self):
        self.api.place_bet(self.bet, self.multiplier)

    def on_new_crash(self, crash_val):
        self.api.log("New Crash Val:", crash_val)

        if crash_val >= self.multiplier:
            if self.current_streak > 0:
                self.rounds_since_streak_size[self.current_streak] = 0

        for key in self.rounds_since_streak_size.keys():
            self.rounds_since_streak_size[key] += 1

        self.update_streak_count(crash_val)

        # TODO: CHECK IF STREAK ABOVE IS < AVG CUS THEN IT SHOULDNT HAPPEN AS OFTEN?
        if self.rounds_since_streak_size[1] > self.rounds_since_streak_size_data['median'][1] \
                and self.rounds_since_streak_size[2] < self.rounds_since_streak_size_data['median'][2] \
                and self.rounds_since_streak_size[3] < self.rounds_since_streak_size_data['median'][3] \
                and self.rounds_since_streak_size[4] < self.rounds_since_streak_size_data['median'][4] \
                and self.rounds_since_streak_size[5] < self.rounds_since_streak_size_data['median'][5]:

            self.place_bet()
