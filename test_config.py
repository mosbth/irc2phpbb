#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for reading, merging and parsing config
"""

import contextlib
import io
import os
import sys
from unittest import TestCase

from main import mergeOptionsWithConfigFile, parseOptions, MSG_VERSION


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
            sys.argv = ["./main.py", f"--{parameter}", str(self.CHANGED_CONFIG.get(parameter))]
            actual = parseOptions(self.SAMPLE_CONFIG)
            self.assertEqual(actual.get(parameter), self.CHANGED_CONFIG.get(parameter))

    def testOverrideMultipleParameters(self):
        """Test that multiple parameters can be overridden from commandline"""
        sys.argv = ["./main.py", "--server", "dbwebb.se", "--port", "5432"]
        actual = parseOptions(self.SAMPLE_CONFIG)
        self.assertEqual(actual.get("server"), "dbwebb.se")
        self.assertEqual(actual.get("port"), 5432)

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

    def testOverridePrecedenceParameterFirst(self):
        """Test that proper precedence is considered. From most to least significant it should be:
        explicit parameter -> parameter in --config file -> default """

        configFile = os.path.join("testConfigs", "server.json")
        sys.argv = ["./main.py", "--server", "important.com", "--config", configFile]
        actual = parseOptions(self.SAMPLE_CONFIG)
        self.assertEqual(actual.get("server"), "important.com")

class FormattingTest(TestCase):
    """Test the parameters that cause printouts"""

    USAGE = ("usage: main.py [-h] [-v] [--config CONFIG] [--server SERVER] [--port PORT] "
             "[--channel CHANNEL] [--nick NICK] [--realname REALNAME] [--ident IDENT]\n")
    OPTIONS = ("options:\n"
               "  -h, --help           show this help message and exit\n"
               "  -v, --version\n"
               "  --config CONFIG\n"
               "  --server SERVER\n"
               "  --port PORT\n"
               "  --channel CHANNEL\n"
               "  --nick NICK\n"
               "  --realname REALNAME\n"
               "  --ident IDENT")

    def assertPrintOption(self, options, returnCode, output):
        """Assert that parseOptions returns a certain code and prints a certain output"""
        with self.assertRaises(SystemExit) as e:
            s = io.StringIO()
            with contextlib.redirect_stdout(s):
                sys.argv = ["./main.py"] + [options]
                parseOptions({})
        self.assertEqual(e.exception.code, returnCode)
        self.assertEqual(s.getvalue(), output+"\n") # extra newline added by print()


    def testHelpPrintout(self):
        """Test that a help is printed when providing the --help flag"""
        self.assertPrintOption("--help", 0, f"{self.USAGE}\n{self.OPTIONS}")

    def testHelpPrintoutShort(self):
        """Test that a help is printed when providing the -h flag"""
        self.assertPrintOption("-h", 0, f"{self.USAGE}\n{self.OPTIONS}")

    def testVersionPrintout(self):
        """Test that the version is printed when provided the --version flag"""
        self.assertPrintOption("--version", 0, MSG_VERSION)

    def testVersionPrintoutShort(self):
        """Test that the version is printed when provided the -v flag"""
        self.assertPrintOption("-v", 0, MSG_VERSION)

    def testUnhandledOption(self):
        """Test that unknown options gives an error"""
        with self.assertRaises(SystemExit) as e:
            s = io.StringIO()
            expectedError = f"{self.USAGE}main.py: error: unrecognized arguments: -g\n"
            with contextlib.redirect_stderr(s):
                sys.argv = ["./main.py", "-g"]
                parseOptions({})
        self.assertEqual(e.exception.code, 2)
        self.assertEqual(s.getvalue(), expectedError)

    def testUnhandledArgument(self):
        """Test that any argument gives an error"""
        with self.assertRaises(SystemExit) as e:
            s = io.StringIO()
            expectedError = f"{self.USAGE}main.py: error: unrecognized arguments: arg\n"
            with contextlib.redirect_stderr(s):
                sys.argv = ["./main.py", "arg"]
                parseOptions({})
        self.assertEqual(e.exception.code, 2)
        self.assertEqual(s.getvalue(), expectedError)
