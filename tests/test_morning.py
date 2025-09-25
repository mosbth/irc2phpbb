"""
Tests for the Marvin Morning action
"""

from datetime import date
from unittest import mock

from test_action import ActionTest
from irc2phpbb import marvin_general_actions

class MorningTest(ActionTest):
    """Tests for the Marvin Morning action"""
    def testMorning(self):
        """Test that marvin wishes good morning, at most once per day"""
        marvin_general_actions.lastDateGreeted = None
        with mock.patch("irc2phpbb.marvin_general_actions.datetime") as d:
            d.date.today.return_value = date(2024, 5, 17)
            with mock.patch("irc2phpbb.marvin_general_actions.random") as r:
                r.choice.return_value = "Morgon"
                self.assertActionOutput(marvin_general_actions.marvinMorning, "morrn", "Morgon")
                # Should only greet once per day
                self.assertActionSilent(marvin_general_actions.marvinMorning, "morgon")
                # Should greet again tomorrow
                d.date.today.return_value = date(2024, 5, 18)
                self.assertActionOutput(marvin_general_actions.marvinMorning, "godmorgon", "Morgon")
