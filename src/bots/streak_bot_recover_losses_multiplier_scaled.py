import traceback

from src.bots.types import IBot


class StreakBotRecoverLosses(IBot):
    def __init__(self, bet, multiplier, streak_size, api):
        self.bet = bet
        self.multiplier = multiplier
        self.min_streak_size = streak_size
        self.api = api

        self.current_streak = 0
        self.did_just_bet = False
        self.api.log("BOT CREATED. BET: {0} MULTIPLIER: {1} STREAK_SIZE: {2}".format(bet, multiplier, streak_size))
        self.prev_bets = []  # prev bets added together after a loss

    def on_new_crash(self, crash_val):
        self.api.log("New Crash Val:", crash_val)
        self.update_streak_count(crash_val)

        self.did_just_bet = False
        if self.current_streak >= self.min_streak_size:
            self.place_bet()
            self.did_just_bet = True

    def update_streak_count(self, crash_val):
        if crash_val < self.multiplier:
            self.current_streak += 1
            self.api.log("Current Streak:", self.current_streak)
        else:
            self.api.log("Resetting Streak to 0")
            self.current_streak = 0
            self.prev_bets = []

    def place_bet(self):
        bet = sum(self.prev_bets) / (self.multiplier - 1) + self.bet
        self.api.place_bet(bet, self.multiplier)
        self.prev_bets.append(bet)
