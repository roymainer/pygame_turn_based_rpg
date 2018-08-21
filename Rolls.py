"""
Created on Feb 13, 2017

@author: rmainer

This module handles all of the dice rolls required to play the game
Used both by Models and units alike

"""

from random import choice


def get_d6_roll():
    return choice([1, 2, 3, 4, 5, 6])


def get_two_d6_roll():
    return get_d6_roll() + get_d6_roll()


def get_d7_plus_roll(to_hit):
    """
    7 : 6 followed by 4+
    8 : 6 followed by 5+
    9 : 6 followed by 6
    10+ : not possible
    """
    if to_hit >= 10:
        return False

    rolls = [get_d6_roll(), get_d6_roll()]

    if rolls[0] == 6:
        if (to_hit == 7 and rolls[1] >= 4) or (to_hit == 8 and rolls[1] >= 5) or (to_hit == 9 and rolls[1] == 6):
            return True
        else:
            return False
    else:
        return False


def get_artillery_dice_roll():
    return choice([0, 2, 4, 6, 8, 10])  # 0 == misfire


def get_scatter_dice_roll():
    return choice(["UP", "DOWN", "LEFT", "RIGHT", "HIT"])


def get_roll_for_winds_of_magic():
    r1 = get_d6_roll()
    r2 = get_d6_roll()
    power_pool = r1 + r2
    dispel_pool = max(r1, r2)
    return power_pool, dispel_pool


def get_channeling_power_roll(number_of_wizards):
    """For each wizard the player has, he can channel more power from the winds of magic into the power pool"""
    power = 0
    for _ in range(number_of_wizards):
        # for each roll of 6, the wizard can roll another D6 dice
        while True:
            p = get_d6_roll()
            power += p
            if p < 6:
                break

    return power
