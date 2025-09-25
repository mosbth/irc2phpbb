"""
Tests for the Marvin Help action
"""

from test_action import ActionTest
from irc2phpbb import marvin_actions

class HelpTest(ActionTest):
    """Tests for the Marvin Help action"""
    def testHelp(self):
        """Test that marvin can provide a help menu"""
        self.assertStringsOutput(marvin_actions.marvinHelp, "help", "menu")
        self.assertActionSilent(marvin_actions.marvinHelp, "halp")
