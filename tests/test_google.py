"""
Tests for the Marvin Google action
"""

from unittest import mock

from test_action import ActionTest
from irc2phpbb import marvin_actions

class GoogleTest(ActionTest):
    """Tests for the Marvin Google action"""
    def testGoogle(self):
        """Test that marvin can help google stuff"""
        with mock.patch("irc2phpbb.marvin_actions.random") as r:
            r.randint.return_value = 1
            self.assertActionOutput(
                marvin_actions.marvinGoogle,
                "kan du googla mos",
                "LMGTFY https://www.google.se/search?q=mos")
            self.assertActionOutput(
                marvin_actions.marvinGoogle,
                "kan du googla google mos",
                "LMGTFY https://www.google.se/search?q=google+mos")
        self.assertActionSilent(marvin_actions.marvinGoogle, "du kan googla")
        self.assertActionSilent(marvin_actions.marvinGoogle, "gogool")
