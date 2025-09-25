"""
Tests for the Marvin Comic Strip action
"""

from unittest import mock

from test_action import ActionTest
from irc2phpbb import marvin_actions

class StripTest(ActionTest):
    """Tests for the Marvin Comic Strip action"""
    def testStrip(self):
        """Test that marvin can recommend comics"""
        messageFormat = self.strings.get("commitstrip").get("message")
        expected = messageFormat.format(url=self.strings.get("commitstrip").get("url"))
        self.assertActionOutput(marvin_actions.marvinStrip, "lite strip kanske?", expected)
        self.assertActionSilent(marvin_actions.marvinStrip, "nostrip")

    def testRandomStrip(self):
        """Test that marvin can recommend random comics"""
        messageFormat = self.strings.get("commitstrip").get("message")
        expected = messageFormat.format(url=self.strings.get("commitstrip").get("urlPage") + "123")
        with mock.patch("irc2phpbb.marvin_actions.random") as r:
            r.randint.return_value = 123
            self.assertActionOutput(marvin_actions.marvinStrip, "random strip kanske?", expected)
