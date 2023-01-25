import traceback

from src.bots.streak_bot_recover_losses_multiplier_scaled import StreakBotRecoverLosses


class StreakBotRecoverLossesLowerMultiplier(StreakBotRecoverLosses):
    def __init__(self, bet, start_multiplier, streak_size, api, lower_multiplier_by=0.1, min_multiplier=1.1):
        super().__init__(bet, start_multiplier, streak_size, api)

        self.lower_multipleir_by = lower_multiplier_by
        self.min_multiplier = min_multiplier

    def place_bet(self):
        current_multiplier = max(self.multiplier - self.lower_multipleir_by * self.current_streak - self.min_streak_size,
                                 self.min_multiplier)
        bet = sum(self.prev_bets) / (current_multiplier - 1) + self.bet
        self.api.place_bet(bet, self.multiplier)
        self.prev_bets.append(bet)
