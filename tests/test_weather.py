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
                        "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/1/station/65090/period/latest-hour/data.json",
                        "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/3/station/65090/period/latest-hour/data.json",
                        "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/4/station/65090/period/latest-hour/data.json"]:
                self.assertTrue(mock.call(url, timeout=5) in r.get.call_args_list)

    def testWeatherResponse(self):
        """Test that marvin properly parses weather responses, and skips the observation
        sentence when nothing significant was observed"""
        responses = []
        for responseFile in ["station.json", "codes.json", "weather.json", "winddirection.json", "windspeed.json", "forecast.json"]:
            path = os.path.join(os.path.dirname(__file__), "resources", "weather", responseFile)
            with open(path, "r", encoding="UTF-8") as f:
                response = requests.models.Response()
                response._content = str.encode(json.dumps(json.load(f)))
                responses.append(response)

        with mock.patch("irc2phpbb.marvin_actions.requests") as r:
            r.get.side_effect = responses
            expected = ("Karlskrona just nu: 16.6 °C, vind 3.2 m/s från SV. "
                        "Kommande timmar: 00:00 15.8°C halvklart, vind 2.6 m/s från N, "
                        "01:00 15.2°C molnigt, vind 3.1 m/s från NV, "
                        "02:00 14.6°C mulet, vind 3.4 m/s från NV.")
            self.assertActionOutput(marvin_actions.marvinWeather, "väder", expected)

    def testWeatherResponseWithSignificantWeather(self):
        """Test that the observation sentence is kept when there actually is significant weather"""
        responses = []
        for responseFile in ["station_significant.json", "codes_significant.json", "weather.json",
                              "winddirection.json", "windspeed.json", "forecast.json"]:
            path = os.path.join(os.path.dirname(__file__), "resources", "weather", responseFile)
            with open(path, "r", encoding="UTF-8") as f:
                response = requests.models.Response()
                response._content = str.encode(json.dumps(json.load(f)))
                responses.append(response)

        with mock.patch("irc2phpbb.marvin_actions.requests") as r:
            r.get.side_effect = responses
            expected = ("Karlskrona just nu: 16.6 °C, vind 3.2 m/s från SV. Lätt regn. "
                        "Kommande timmar: 00:00 15.8°C halvklart, vind 2.6 m/s från N, "
                        "01:00 15.2°C molnigt, vind 3.1 m/s från NV, "
                        "02:00 14.6°C mulet, vind 3.4 m/s från NV.")
            self.assertActionOutput(marvin_actions.marvinWeather, "väder", expected)
