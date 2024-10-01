#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for the common base class for all Bots
"""

import re

class Bot():
    """Base class for things common between different protocols"""
    def __init__(self):
        self.CONFIG = {}
        self.ACTIONS = []
        self.GENERAL_ACTIONS = []

    def getConfig(self):
        """Return the current configuration"""
        return self.CONFIG

    def setConfig(self, config):
        """Set the current configuration"""
        self.CONFIG = config

    def registerActions(self, actions):
        """Register actions to use"""
        print("Adding actions:")
        for action in actions:
            print(" - " + action.__name__)
        self.ACTIONS.extend(actions)

    def registerGeneralActions(self, actions):
        """Register general actions to use"""
        print("Adding general actions:")
        for action in actions:
            print(" - " + action.__name__)
        self.GENERAL_ACTIONS.extend(actions)

    @staticmethod
    def tokenize(message):
        """Split a message into normalized tokens"""
        return re.sub("[,.?:]", " ", message).strip().lower().split()
