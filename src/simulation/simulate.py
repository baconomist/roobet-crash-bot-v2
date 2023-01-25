from src.bots.types import IBot


# Takes bot as input, runs sim on test api and prints results

def run_simulation(bot: IBot):
    api = TestAPI(crash_vals, simulated_balance=Config.SIMULATED_BALANCE)

