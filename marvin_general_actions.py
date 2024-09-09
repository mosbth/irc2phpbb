#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Make general actions for Marvin, one function for each action.
"""
import datetime
import json
import random

# Load all strings from file
with open("marvin_strings.json", encoding="utf-8") as f:
    STRINGS = json.load(f)

# Configuration loaded
CONFIG = None

lastDateGreeted = datetime.date.today()

def setConfig(config):
    """
    Keep reference to the loaded configuration.
    """
    global CONFIG
    CONFIG = config


def getString(key, key1=None):
    """
    Get a string from the string database.
    """
    data = STRINGS[key]
    if isinstance(data, list):
        res = data[random.randint(0, len(data) - 1)]
    elif isinstance(data, dict):
        if key1 is None:
            res = data
        else:
            res = data[key1]
            if isinstance(res, list):
                res = res[random.randint(0, len(res) - 1)]
    elif isinstance(data, str):
        res = data

    return res


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
