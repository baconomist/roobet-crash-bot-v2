from typing import Callable, Type

from src.apis.types import API
from src.bots.types import IBot


class TestAPI(API):
    def __init__(self, crash_vals, simulated_balance=None,
                 on_bet_placed_listener: Callable[[any, float, float, bool], None] = None):
        super(TestAPI, self).__init__()

        self.crash_vals = crash_vals
        self.simulated_balance = simulated_balance
        self.on_bet_placed_listener = on_bet_placed_listener

        self.profits_after_recover_losses = []

        self.consecutive_losses = []
        self.profit = 0
        self.win_count = 0
        self.loss_count = 0
        self.bet_indices = []
        self.profits_after_losses = []
        self.num_wins_between_losses = []
        self.losses_between_wins = []
        self.wins_between_losses = []

        self.current_loop_index = len(self.crash_vals) - 1

        self.current_win = 0
        self.current_loss = 0

        self.loss_streak_frequencies = {}
        self.max_loss_streak_size = 0
        self.current_loss_streak = 0

    def get_bet_count(self):
        return self.win_count + self.loss_count

    def poll_new_crashpoint(self):
        super()._notify_crashpoint_listeners(self.crash_vals[self.current_loop_index])

        self.current_loop_index -= 1

    def place_bet(self, bet, multiplier):
        if self.current_loop_index == -1:
            return

        if self.simulated_balance is not None and bet > self.simulated_balance:
            return

        self.bet_indices.append(self.get_next_crash_index())

        # Place bet on next crash val since bot analyzed the current val and in reality is betting on the next one
        if self.get_next_crash_val() >= multiplier:
            if self.simulated_balance is not None:
                self.simulated_balance += bet * (multiplier - 1)

            self.win_count += 1
            self.profit += bet * (multiplier - 1)
            self.current_win += bet * (multiplier - 1)

            self.wins_between_losses.append(self.current_win)
            self.losses_between_wins.append(self.current_loss)
            self.profits_after_recover_losses.append(bet * (multiplier - 1) - self.current_loss)

            if self.current_loss_streak not in self.loss_streak_frequencies.keys():
                self.loss_streak_frequencies[self.current_loss_streak] = 1
            else:
                self.loss_streak_frequencies[self.current_loss_streak] += 1

            self.current_loss = 0
            self.current_loss_streak = 0
        else:
            if self.simulated_balance is not None:
                self.simulated_balance -= bet

            self.profit -= bet
            self.loss_count += 1
            self.current_loss -= bet
            self.current_win = 0

            self.current_loss_streak += 1

            self.consecutive_losses.append(abs(self.current_loss))

            if len(self.num_wins_between_losses) == 0:
                self.num_wins_between_losses.append(self.win_count)
            else:
                self.num_wins_between_losses.append(self.win_count - sum(self.num_wins_between_losses))

            self.profits_after_losses.append(self.profit)

            if self.current_loss_streak > self.max_loss_streak_size:
                self.max_loss_streak_size = self.current_loss_streak

        if self.on_bet_placed_listener is not None:
            self.on_bet_placed_listener(self, bet, multiplier,
                                        self.get_next_crash_val() >= multiplier)

    def get_next_crash_val(self):
        return self.crash_vals[self.get_next_crash_index()]

    def get_next_crash_index(self):
        return self.current_loop_index - 1

    # Disable logging
    def log(self, *args):
        pass