"""
Tests for the Marvin Power Price action
"""

import datetime

from datetime import date, time

from unittest import mock

from test_action import ActionTest
from irc2phpbb import marvin_actions

class PowerPriceTest(ActionTest):
    """Tests for the Marvin Power Price action"""
    def testPowerPriceRequest(self):
        """Test that marvin sends the expected request for power price info"""
        with mock.patch("irc2phpbb.marvin_actions.datetime", wraps=datetime) as d:
            d.datetime.today.return_value = date(2025, 1, 12)
            with mock.patch("irc2phpbb.marvin_actions.requests") as r:
                self.executeAction(marvin_actions.marvinPowerPrice, "elpris")
                expectedUrl = self.strings.get("powerprice").get("url").format("2025-01-12")
                self.assertEqual(r.get.call_args.args[0], expectedUrl)

    def testPowerPriceResponse(self):
        """Test that marvin properly parses weather responses"""
        with mock.patch("irc2phpbb.marvin_actions.random") as r:
            r.randint.return_value = 0
            self.assertPowerPriceOutput("singleAreaResponse", time(12, 1, 0, 0), "Just nu kostar en kWh 1.4007 SEK i SE4.")
            self.assertPowerPriceOutput("singleAreaResponse", time(15, 0, 1, 0), "Just nu kostar en kWh 1.5130 SEK i SE4. Huvva!")


    def testPowerPriceReaction(self):
        """Test that marvin only reacts to power price requests when asked"""
        self.assertActionSilent(marvin_actions.marvinPowerPrice, "strömmen är dyr idag!")

    def assertPowerPriceOutput(self, exampleFile, timeOfDay,  expectedOutput):
        """Assert that marvin knows the current power price, given an input file and a time (in UTC)"""
        response = self.createResponseFrom("powerPriceFiles", exampleFile)
        with mock.patch("irc2phpbb.marvin_actions.datetime", wraps=datetime) as d:
            d.datetime.utcnow.return_value = timeOfDay
            with mock.patch("irc2phpbb.marvin_actions.requests") as r:
                r.get.return_value = response
                self.assertActionOutput(marvin_actions.marvinPowerPrice, "elpris", expectedOutput)
