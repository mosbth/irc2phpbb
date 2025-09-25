"""
Tests for the Marvin Whois action
"""

from test_action import ActionTest
from irc2phpbb import marvin_actions

class WhoisTest(ActionTest):
    """Tests for the Marvin Whois action"""
    def testWhois(self):
        """Test that marvin responds to whois"""
        self.assertStringsOutput(marvin_actions.marvinWhoIs, "vem är marvin?", "whois")
        self.assertActionSilent(marvin_actions.marvinWhoIs, "vemär")
