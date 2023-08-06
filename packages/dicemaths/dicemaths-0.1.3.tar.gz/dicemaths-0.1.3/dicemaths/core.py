def prob_none(n, target_window, total_window):
    if target_window >= total_window:
        return 0.0
    elif target_window <= 0:
        return 1.0
    else:
        fail_window = float(total_window - target_window)
        prob_single_fail = fail_window / total_window
        prob_total_fail = prob_single_fail ** n
        return prob_total_fail


def prob_one_up(n, target_window, total_window):
    return 1 - prob_none(n, target_window, total_window)


def avg_successes(n, target_window, total_window):
    return n * target_window / float(total_window)
