class IRequestHandler(object):
    def do_bet_request(self, bet, multiplier):
        raise NotImplementedError()

    def get_recent_bets(self):
        raise NotImplementedError()
