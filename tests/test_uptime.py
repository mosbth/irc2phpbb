"""
Tests for the Marvin Uptime action
"""

from test_action import ActionTest
from irc2phpbb import marvin_actions

class UptimeTest(ActionTest):
    """Tests for the Marvin Uptime action"""
    def testUptime(self):
        """Test that marvin can provide the link to the uptime tournament"""
        self.assertStringsOutput(marvin_actions.marvinUptime, "visa lite uptime", "uptime", "info")
        self.assertActionSilent(marvin_actions.marvinUptime, "uptimetävling")
