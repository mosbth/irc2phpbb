"""
Tests for the Marvin Principle action
"""

from unittest import mock

from test_action import ActionTest
from irc2phpbb import marvin_actions

class PrincipleTest(ActionTest):
    """Tests for the Marvin Principle action"""
    def testPrinciple(self):
        """Test that marvin can recite some software principles"""
        principles = self.strings.get("principle")
        for key, value in principles.items():
            self.assertActionOutput(marvin_actions.marvinPrinciple, f"princip {key}", value)
        with mock.patch("irc2phpbb.marvin_actions.random") as r:
            r.choice.return_value = "dry"
            self.assertStringsOutput(marvin_actions.marvinPrinciple, "princip", "principle", "dry")
        self.assertActionSilent(marvin_actions.marvinPrinciple, "principlös")
