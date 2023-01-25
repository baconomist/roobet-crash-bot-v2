#
# theoretical_dist = get_probability_of_above_streak(Config.START_MULTIPLIER, 6, 11)
# current_streak = 0
# print("DISTS", theoretical_dist, get_actual_above_streak_distribution(6, streak_frequencies))
# win_count = 0
# loss_count = 0
# window = 100
# for i in range(window, 100000):
#     start = i - window
#     end = i
#     acc_dist = get_actual_above_streak_distribution(6, get_streak_frequencies(Config.START_MULTIPLIER, all_crash_vals[start:end]))
#
#     if acc_dist - theoretical_dist < -0.2:
#         if all_crash_vals[i] < Config.START_MULTIPLIER:
#             loss_count += 1
#         else:
#             win_count += 1
#
#     i += 1
#
# print(win_count, loss_count)
# print(win_count / loss_count)

# api = TestAPI(all_crash_vals)
# bot = StreakBotRecoverLossesLowerMultiplier(Config.BET, Config.START_MULTIPLIER, Config.MIN_STREAK_SIZE, api)
# api.register_new_crashpoint_listener(bot)
#
# for i in range(len(all_crash_vals)):
#     api.poll_new_crashpoint()
#
# print(api.profit)