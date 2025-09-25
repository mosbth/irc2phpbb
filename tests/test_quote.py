"""
Tests for the Marvin Quote action
"""

from unittest import mock

from test_action import ActionTest
from irc2phpbb import marvin_actions

class QuoteTest(ActionTest):
    """Tests for the Marvin Quote action"""
    def testQuote(self):
        """Test that marvin can quote The Hitchhikers Guide to the Galaxy"""
        with mock.patch("irc2phpbb.marvin_actions.random") as r:
            r.randint.return_value = 1
            self.assertStringsOutput(marvin_actions.marvinQuote, "ge os ett citat", "hitchhiker", 1)
            self.assertStringsOutput(marvin_actions.marvinQuote, "filosofi", "hitchhiker", 1)
            self.assertStringsOutput(marvin_actions.marvinQuote, "filosofera", "hitchhiker", 1)
            self.assertActionSilent(marvin_actions.marvinQuote, "noquote")

            for i,_ in enumerate(self.strings.get("hitchhiker")):
                r.randint.return_value = i
                self.assertStringsOutput(marvin_actions.marvinQuote, "quote", "hitchhiker", i)
