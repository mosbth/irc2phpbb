#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for all Marvin actions
"""

import json
import re
import unittest

from unittest import mock

import marvin_actions

class ActionTest(unittest.TestCase):
    """Test Marvin actions"""
    strings = {}

    @classmethod
    def setUpClass(cls):
        with open("marvin_strings.json", encoding="utf-8") as f:
            cls.strings = json.load(f)


    def assertActionOutput(self, action, message, expectedOutput):
        """Call an action on message and assert expected output"""
        row = re.sub('[,.?:]', ' ', message).strip().lower().split()

        actualOutput = action(set(row), row, message)

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


    def testWhois(self):
        """Test that marvin responds to whois"""
        self.assertStringsOutput(marvin_actions.marvinWhoIs, "vem är marvin?", "whois")
        self.assertActionSilent(marvin_actions.marvinWhoIs, "vemär")

    def testExplainShell(self):
        """Test that marvin can explain shell commands"""
        url = "http://explainshell.com/explain?cmd=pwd"
        self.assertActionOutput(marvin_actions.marvinExplainShell, "explain pwd", url)
        self.assertActionOutput(marvin_actions.marvinExplainShell, "can you explain pwd", url)
        self.assertActionOutput(
            marvin_actions.marvinExplainShell,
            "förklara pwd|grep -o $user",
            f"{url}%7Cgrep+-o+%24user")

        self.assertActionSilent(marvin_actions.marvinExplainShell, "explains")

    def testSource(self):
        """Test that marvin responds to questions about source code"""
        self.assertStringsOutput(marvin_actions.marvinSource, "source", "source")
        self.assertStringsOutput(marvin_actions.marvinSource, "källkod", "source")
        self.assertActionSilent(marvin_actions.marvinSource, "opensource")

    def testBudord(self):
        """Test that marvin knows all the commandments"""
        for n in range(1, 5):
            self.assertStringsOutput(marvin_actions.marvinBudord, f"budord #{n}", "budord", f"#{n}")

        self.assertStringsOutput(marvin_actions.marvinBudord,"visa stentavla 1", "budord", "#1")
        self.assertActionSilent(marvin_actions.marvinBudord, "var är stentavlan?")

    def testQuote(self):
        """Test that marvin can quote The Hitchhikers Guide to the Galaxy"""
        with mock.patch("marvin_actions.random") as r:
            r.randint.return_value = 1
            self.assertStringsOutput(marvin_actions.marvinQuote, "ge os ett citat", "hitchhiker", 1)
            self.assertStringsOutput(marvin_actions.marvinQuote, "filosofi", "hitchhiker", 1)
            self.assertStringsOutput(marvin_actions.marvinQuote, "filosofera", "hitchhiker", 1)
            self.assertActionSilent(marvin_actions.marvinQuote, "noquote")

            for i,_ in enumerate(self.strings.get("hitchhiker")):
                r.randint.return_value = i
                self.assertStringsOutput(marvin_actions.marvinQuote, "quote", "hitchhiker", i)

    def testVideoOfToday(self):
        """Test that marvin can link to a different video each day of the week"""
        with mock.patch("marvin_actions.datetime") as dt:
            for d in range(1, 8):
                dt.date.weekday.return_value = d - 1
                day =  self.strings.get("weekdays").get(str(d))
                video = self.strings.get("video-of-today").get(str(d))
                response = f"{day} En passande video är {video}"
                self.assertActionOutput(marvin_actions.marvinVideoOfToday, "dagens video", response)
        self.assertActionSilent(marvin_actions.marvinVideoOfToday, "videoidag")

    def testHelp(self):
        """Test that marvin can provide a help menu"""
        self.assertStringsOutput(marvin_actions.marvinHelp, "help", "menu")
        self.assertActionSilent(marvin_actions.marvinHelp, "halp")
