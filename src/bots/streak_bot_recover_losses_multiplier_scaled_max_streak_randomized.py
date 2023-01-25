import traceback
from random import random

from src.bots.streak_bot_recover_losses_multiplier_scaled import StreakBotRecoverLosses
from src.bots.types import IBot

AVG_ROUNDS_24_HR = 2500

class StreakBotRecoverLossesMaxStreakRandomized(StreakBotRecoverLosses):
    def __init__(self, bet, multiplier, streak_size, api, max_streak):
        super().__init__(bet, multiplier, streak_size, api)
        self.max_streak = max_streak
        self.rounds_since_bet = 999999999999999

    def on_new_crash(self, crash_val):
        self.api.log("New Crash Val:", crash_val)
        self.update_streak_count(crash_val)

        self.did_just_bet = False
        if self.min_streak_size <= self.current_streak < self.max_streak and self.rounds_since_bet >= AVG_ROUNDS_24_HR * 7:
            self.place_bet()
            self.did_just_bet = True
            self.rounds_since_bet = 0

        self.rounds_since_bet += 1
