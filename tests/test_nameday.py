"""
Tests for the Marvin NameDay action
"""

from unittest import mock

from datetime import date
from test_action import ActionTest
from irc2phpbb import marvin_actions

class NameDayTest(ActionTest):
    """Tests for the Marvin Joke action"""
    def assertNameDayOutput(self, exampleFile, expectedOutput):
        """Assert that the proper nameday message is returned, given an inputfile"""
        response = self.createResponseFrom("nameday", exampleFile)
        with mock.patch("irc2phpbb.marvin_actions.requests") as r:
            r.get.return_value = response
            self.assertActionOutput(marvin_actions.marvinNameday, "nameday", expectedOutput)

    def testNameDayReaction(self):
        """Test that marvin only responds to nameday when asked"""
        self.assertActionSilent(marvin_actions.marvinNameday, "anything")

    def testNameDayRequest(self):
        """Test that marvin sends a proper request for nameday info"""
        with mock.patch("irc2phpbb.marvin_actions.requests") as r, mock.patch("irc2phpbb.marvin_actions.datetime") as d:
            d.datetime.now.return_value = date(2024, 1, 2)
            self.executeAction(marvin_actions.marvinNameday, "namnsdag")
            self.assertEqual(r.get.call_args.args[0], "https://api.dryg.net/dagar/v2.1/2024/1/2")

    def testNameDayResponse(self):
        """Test that marvin properly parses nameday responses"""
        self.assertNameDayOutput("single", "Idag har Svea namnsdag")
        self.assertNameDayOutput("double", "Idag har Alfred och Alfrida namnsdag")
        self.assertNameDayOutput("triple", "Idag har Kasper, Melker och Baltsar namnsdag")
        self.assertNameDayOutput("nobody", "Ingen har namnsdag idag")

    def testNameDayError(self):
        """Tests that marvin returns the proper error message when nameday API is down"""
        with mock.patch("irc2phpbb.marvin_actions.requests.get", side_effect=Exception("API Down!")):
            self.assertStringsOutput(
                marvin_actions.marvinNameday,
                "har någon namnsdag idag?",
                "nameday",
                "error")


