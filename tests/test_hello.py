"""
Tests for the Marvin Hello action
"""

from unittest import mock

from test_action import ActionTest
from irc2phpbb import marvin_actions

class HelloTest(ActionTest):
    """Tests for the Marvin Hello action"""
    def testSayHello(self):
        """Test that marvin responds to greetings"""
        with mock.patch("irc2phpbb.marvin_actions.random") as r:
            for skey, s in enumerate(self.strings.get("smile")):
                for hkey, h in enumerate(self.strings.get("hello")):
                    for fkey, f in enumerate(self.strings.get("friendly")):
                        r.randint.side_effect = [skey, hkey, fkey]
                        self.assertActionOutput(marvin_actions.marvinSayHi, "hej", f"{s} {h} {f}")
        self.assertActionSilent(marvin_actions.marvinSayHi, "korsning")
