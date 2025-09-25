
"""
Module containing common code for testing Marvin actions
"""

import json
import os

from unittest import TestCase

import requests

from irc2phpbb.bot import Bot


class ActionTest(TestCase):
    """Base class with utility functions for testing marvin actions"""
    strings = {}

    @classmethod
    def setUpClass(cls):
        with open("irc2phpbb/data/marvin_strings.json", encoding="utf-8") as f:
            cls.strings = json.load(f)

    def executeAction(self, action, message):
        """Execute an action for a message and return the response"""
        return action(Bot.tokenize(message))

    def assertActionOutput(self, action, message, expectedOutput):
        """Call an action on message and assert expected output"""
        actualOutput = self.executeAction(action, message)
        self.assertEqual(actualOutput, expectedOutput)

    def assertActionSilent(self, action, message):
        """Call an action with provided message and assert no output"""
        self.assertActionOutput(action, message, None)

    def assertStringsOutput(self, action, message, expectedoutputKey, subkey=None):
        """Call an action with provided message and assert the output is equal to DB"""
        expectedOutput = self.strings.get(expectedoutputKey)
        if subkey is not None:
            if isinstance(expectedOutput, list):
                expectedOutput = expectedOutput[subkey]
            else:
                expectedOutput = expectedOutput.get(subkey)
        self.assertActionOutput(action, message, expectedOutput)


    def createResponseFrom(self, directory, filename):
        """Create a response object with contect as contained in the specified file"""
        path = os.path.join(os.path.dirname(__file__), "resources", directory, f"{filename}.json")
        with open(path, "r", encoding="UTF-8") as f:
            response = requests.models.Response()
            response._content = str.encode(json.dumps(json.load(f)))
            return response
