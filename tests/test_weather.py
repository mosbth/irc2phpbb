"""
Tests for the Marvin Weather action
"""

import json
import os

from unittest import mock

import requests

from test_action import ActionTest
from irc2phpbb import marvin_actions

class WeatherTest(ActionTest):
    """Tests for the Marvin Weather action"""
    def testWeatherRequest(self):
        """Test that marvin sends the expected requests for weather info"""
        with mock.patch("irc2phpbb.marvin_actions.requests") as r:
            self.executeAction(marvin_actions.marvinWeather, "väder")
            for url in ["https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/13/station/65090/period/latest-hour/data.json",
                        "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/13/codes.json",
                        "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/15.5890/lat/56.1500/data.json"]:
                self.assertTrue(mock.call(url, timeout=5) in r.get.call_args_list)

    def testWeatherResponse(self):
        """Test that marvin properly parses weather responses"""
        responses = []
        for responseFile in ["station.json", "codes.json", "weather.json"]:
            path = os.path.join(os.path.dirname(__file__), "resources", "weather", responseFile)
            with open(path, "r", encoding="UTF-8") as f:
                response = requests.models.Response()
                response._content = str.encode(json.dumps(json.load(f)))
                responses.append(response)

        with mock.patch("irc2phpbb.marvin_actions.requests") as r:
            r.get.side_effect = responses
            expected = "Karlskrona just nu: 11.7 °C. Inget signifikant väder observerat."
            self.assertActionOutput(marvin_actions.marvinWeather, "väder", expected)
