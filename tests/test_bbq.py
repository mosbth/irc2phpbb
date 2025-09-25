"""
Tests for the Marvin BBQ action
"""

from unittest import mock

from datetime import date
from test_action import ActionTest
from irc2phpbb import marvin_actions

class BBQTest(ActionTest):
    """Tests for the Marvin BBQ action"""
    def assertBBQResponse(self, todaysDate, bbqDate, expectedMessageKey):
        """Assert that the proper bbq message is returned, given a date"""
        url = self.strings.get("barbecue").get("url")
        message = self.strings.get("barbecue").get(expectedMessageKey)
        if isinstance(message, list):
            message = message[1]
        if expectedMessageKey in ["base", "week", "eternity"]:
            message = message % bbqDate

        with mock.patch("irc2phpbb.marvin_actions.datetime") as d, mock.patch("irc2phpbb.marvin_actions.random") as r:
            d.date.today.return_value = todaysDate
            r.randint.return_value = 1
            expected = f"{url}. {message}"
            self.assertActionOutput(marvin_actions.marvinTimeToBBQ, "dags att grilla", expected)

    def testTimeToBBQSpring(self):
        """Test each different output possible for spring dates"""
        self.assertBBQResponse(date(2024, 5, 17), date(2024, 5, 17), "today")
        self.assertBBQResponse(date(2024, 5, 16), date(2024, 5, 17), "tomorrow")
        self.assertBBQResponse(date(2024, 5, 10), date(2024, 5, 17), "week")
        self.assertBBQResponse(date(2024, 5, 1), date(2024, 5, 17), "base")
        self.assertBBQResponse(date(2023, 10, 17), date(2024, 5, 17), "eternity")

    def testTimeToBBQAutumn(self):
        """Test each different output possible for autumn dates"""
        self.assertBBQResponse(date(2024, 9, 20), date(2024, 9, 20), "today")
        self.assertBBQResponse(date(2024, 9, 19), date(2024, 9, 20), "tomorrow")
        self.assertBBQResponse(date(2024, 9, 13), date(2024, 9, 20), "week")
        self.assertBBQResponse(date(2024, 9, 4), date(2024, 9, 20), "base")
