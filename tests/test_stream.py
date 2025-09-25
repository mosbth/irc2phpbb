"""
Tests for the Marvin Stream action
"""

from test_action import ActionTest
from irc2phpbb import marvin_actions

class StreamTest(ActionTest):
    """Tests for the Marvin Stream action"""
    def testStream(self):
        """Test that marvin can provide the link to the stream"""
        self.assertStringsOutput(marvin_actions.marvinStream, "ska mos streama?", "stream", "info")
        self.assertActionSilent(marvin_actions.marvinStream, "är mos en streamer?")
