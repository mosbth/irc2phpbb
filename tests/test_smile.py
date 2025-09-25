"""
Tests for the Marvin Smile action
"""

from unittest import mock

from test_action import ActionTest
from irc2phpbb import marvin_actions

class SmileTest(ActionTest):
    """Tests for the Marvin Smile action"""
    def testSmile(self):
        """Test that marvin can smile"""
        with mock.patch("irc2phpbb.marvin_actions.random") as r:
            r.randint.return_value = 1
            self.assertStringsOutput(marvin_actions.marvinSmile, "le lite?", "smile", 1)
        self.assertActionSilent(marvin_actions.marvinSmile, "sur idag?")
