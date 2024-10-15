#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make general actions for Marvin, one function for each action.
"""
import datetime
import random

lastDateGreeted = None


def getAllGeneralActions():
    """
    Return all general actions as an array.
    """
    return [
        marvinMorning
    ]


def marvinMorning(row):
    """
    Marvin says Good morning after someone else says it
    """
    msg = None
    phrases = [
        "morgon",
        "godmorgon",
        "god morgon",
        "morrn",
        "morn"
    ]

    morning_phrases = [
        "Godmorgon! :-)",
        "Morgon allesammans",
        "Morgon gott folk",
        "Guten morgen",
        "Morgon"
    ]

    global lastDateGreeted

    for phrase in phrases:
        if phrase in row:
            if lastDateGreeted != datetime.date.today():
                lastDateGreeted = datetime.date.today()
                msg = random.choice(morning_phrases)
    return msg
