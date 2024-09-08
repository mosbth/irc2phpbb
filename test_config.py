#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for reading, merging and parsing config
"""

import os
from unittest import TestCase

from main import mergeOptionsWithConfigFile
from main import mergeOptionsWithConfigFile, parseOptions

class ConfigMergeTest(TestCase):
    """Test merging a config file with a dict"""

    def assertMergedConfig(self, config, fileName, expected):
        """Merge dict with file and assert the result matches expected"""
        configFile = os.path.join("testConfigs", f"{fileName}.json")
        actualConfig = mergeOptionsWithConfigFile(config, configFile)
        self.assertEqual(actualConfig, expected)


    def testEmpty(self):
        """Empty into empty should equal empty"""
        self.assertMergedConfig({}, "empty", {})

    def testAddSingleParameter(self):
        """Add a single parameter to an empty config"""
        new = {
            "single": "test"
        }
        expected = {
            "single": "test"
        }
        self.assertMergedConfig(new, "empty", expected)

    def testAddSingleParameterOverwrites(self):
        """Add a single parameter to a config that contains it already"""
        new = {
            "single": "test"
        }
        expected = {
            "single": "original"
        }
        self.assertMergedConfig(new, "single", expected)

    def testAddSingleParameterMerges(self):
        """Add a single parameter to a config that contains a different one"""
        new = {
            "new": "test"
        }
        expected = {
            "new" : "test",
            "single" : "original"
        }
        self.assertMergedConfig(new, "single", expected)

class ConfigParseTest(TestCase):
    """Test parsing options into a config"""

    SAMPLE_CONFIG = {
        "server": "localhost",
        "port": 6667,
        "channel": "#dbwebb",
        "nick": "marvin",
        "realname": "Marvin The All Mighty dbwebb-bot",
        "ident": "password"
    }

    CHANGED_CONFIG = {
        "server": "remotehost",
        "port": 1234,
        "channel": "#db-o-webb",
        "nick": "imposter",
        "realname": "where is marvin?",
        "ident": "identify"
    }

    def testOverrideHardcodedParameters(self):
        """Test that all the hard coded parameters can be overridden from commandline"""
        for parameter in ["server", "port", "channel", "nick", "realname", "ident"]:
            sys.argv = ["./main.py", f"--{parameter}", self.CHANGED_CONFIG.get(parameter)]
            actual = parseOptions(self.SAMPLE_CONFIG)
            self.assertEqual(actual.get(parameter), self.CHANGED_CONFIG.get(parameter))

    def testOverrideMultipleParameters(self):
        """Test that multiple parameters can be overridden from commandline"""
        sys.argv = ["./main.py", "--server", "dbwebb.se", "--port", "5432"]
        actual = parseOptions(self.SAMPLE_CONFIG)
        self.assertEqual(actual.get("server"), "dbwebb.se")
        self.assertEqual(actual.get("port"), "5432")

    def testOverrideWithFile(self):
        """Test that parameters can be overridden with the --config option"""
        configFile = os.path.join("testConfigs", "server.json")
        sys.argv = ["./main.py", "--config", configFile]
        actual = parseOptions(self.SAMPLE_CONFIG)
        self.assertEqual(actual.get("server"), "irc.dbwebb.se")

    def testOverridePrecedenceConfigFirst(self):
        """Test that proper precedence is considered. From most to least significant it should be:
        explicit parameter -> parameter in --config file -> default """

        configFile = os.path.join("testConfigs", "server.json")
        sys.argv = ["./main.py", "--config", configFile, "--server", "important.com"]
        actual = parseOptions(self.SAMPLE_CONFIG)
        self.assertEqual(actual.get("server"), "important.com")

