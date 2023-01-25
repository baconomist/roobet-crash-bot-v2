import traceback

from src.bots.streak_bot_recover_losses_multiplier_scaled import StreakBotRecoverLosses
from src.bots.types import IBot
from src.data_analysis.data_utils import get_rounds_since_streak_size, get_rounds_since_streak_size_data


class StreakBotRecoverLossesRoundsSinceStreak(StreakBotRecoverLosses):

    def __init__(self, bet, multiplier, streak_size, api, rounds_since_streak_size_data,
                 latest_rounds_since_streak_size):
        super().__init__(bet, multiplier, streak_size, api)
        self.rounds_since_streak_size_data = rounds_since_streak_size_data

        self.rounds_since_streak_size = latest_rounds_since_streak_size
        self.did_start_bet_streak = False

    def on_new_crash(self, crash_val):
        self.api.log("New Crash Val:", crash_val)

        if crash_val >= self.multiplier:
            if self.current_streak > 0:
                self.rounds_since_streak_size[self.current_streak] = 0

            self.did_start_bet_streak = False

        for key in self.rounds_since_streak_size.keys():
            self.rounds_since_streak_size[key] += 1

        self.update_streak_count(crash_val)

        should_bet = True
        for x in self.rounds_since_streak_size.keys():
            if 6 <= x <= 12 and self.rounds_since_streak_size[x] > self.rounds_since_streak_size_data['avg'][x]:
                # and get_rounds_since_streak_size(self.data1['avg'][1], self.data1['distances'][1], 4)[8] < self.data1['avg'][8]: # TODO AHAHAHAHHAHHA GET ROUNDS SINCE STREAK SIZE DATA1 I DONUT INDEUERSTAND!?!??!
                should_bet = False

        # TODO: CHECK IF STREAK ABOVE IS < AVG CUS THEN IT SHOULDNT HAPPEN AS OFTEN?
        self.did_just_bet = False
        # if (should_bet and self.current_streak == self.min_streak_size) or self.did_start_bet_streak:
        if (self.rounds_since_streak_size[0] < self.rounds_since_streak_size_data['avg'][0] and self.current_streak == self.min_streak_size) or self.did_start_bet_streak:
            self.place_bet()
            self.did_just_bet = True
            self.did_start_bet_streak = True
