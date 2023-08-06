from dicemaths.core import prob_none

# Returns the average hits and crits for p1 in a contested roll as a tuple
def contested_roll_hit_avg(attacker_burst, attacker_target, target_burst, target_target):
    attacker_bonus = max(0, attacker_target - 20)
    attacker_target = min(20, attacker_target)
    target_bonus = max(0, target_target - 20)
    target_target = min(20, target_target)
    single_dice_hit_prob = 0
    single_dice_crit_prob = 0.0
    for i in range(1, 21):
        value_rolled = i + attacker_bonus
        #print("_rolled {0}".format(value_rolled))
        if(value_rolled == attacker_target or value_rolled > 20):
            prob_no_contest = prob_none(target_burst, 1 + target_bonus, 20)
            prob_crit_from_roll = (1.0 / 20) * prob_no_contest
            single_dice_crit_prob += prob_crit_from_roll
            #print("crit probability: {0}".format(prob_crit_from_roll))
        elif(value_rolled < attacker_target):
            window_with_mods = max(1, min(20, (target_target - value_rolled + 1 + target_bonus)))
            prob_no_contest = prob_none(target_burst, window_with_mods, 20)
            prob_hit_from_roll = (1.0 / 20) * prob_no_contest
            single_dice_hit_prob += prob_hit_from_roll
            #print(prob_hit_from_roll)
    return (attacker_burst * single_dice_hit_prob, attacker_burst * single_dice_crit_prob)


def contested_roll_crit_avg(attacker_burst, attacker_target, attacker_bonus, target_burst, target_target, target_bonus):
    singleDiceProb = 0.0
    for i in range(1, 21):
        value_rolled = i + attacker_bonus
        #print("_rolled {0}".format(value_rolled))
        if (value_rolled == attacker_target or value_rolled > 20):
            prob_no_contest = prob_none(target_burst, 1 + target_bonus, 20)
            prob_hit_from_roll = (1.0 / 20) * prob_no_contest
            singleDiceProb += prob_hit_from_roll
            #print(prob_hit_from_roll)
    return attacker_burst * singleDiceProb
