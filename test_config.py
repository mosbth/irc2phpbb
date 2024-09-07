#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for reading, merging and parsing config
"""

import os
from unittest import TestCase

from main import mergeOptionsWithConfigFile

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
