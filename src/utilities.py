#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint

__author__ = "Michel Llorens"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "mllorens@dcc.uchile.cl"


def roll_to_val(string_roll):
    change_sign = string_roll.replace('-', '+ -')
    parts = change_sign.split('+')
    counter = 0

    for part in parts:
        value = parse_unitary_roll(part)
        counter += value

    return counter


def parse_unitary_roll(string_roll):
    string_roll = string_roll.strip()
    d_location = string_roll.find('d')

    if string_roll.find('-') != -1:
        tail = string_roll.replace('-', '').strip()
        value = -1 * parse_unitary_roll(tail)
    elif d_location != -1:
        ponderer, dice_sides = string_roll.split("d")
        value = int(ponderer) * roll_dice(dice_sides)
    else:
        value = int(string_roll)
    return value


def roll_dice(sides):
    sides = int(sides)
    return randint(1, sides)


def valid_roll(string_roll):
    try:
        roll_to_val(string_roll)
    except ValueError:
        return False
    return True
