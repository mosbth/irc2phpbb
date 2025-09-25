"""
Tests for the Marvin Source action
"""

from test_action import ActionTest
from irc2phpbb import marvin_actions

class SourceTest(ActionTest):
    """Tests for the Marvin Source action"""
    def testSource(self):
        """Test that marvin responds to questions about source code"""
        self.assertStringsOutput(marvin_actions.marvinSource, "source", "source")
        self.assertStringsOutput(marvin_actions.marvinSource, "källkod", "source")
        self.assertActionSilent(marvin_actions.marvinSource, "opensource")
