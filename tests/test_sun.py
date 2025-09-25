"""
Tests for the Marvin Sun action
"""

from unittest import mock

from test_action import ActionTest
from irc2phpbb import marvin_actions

class sunTest(ActionTest):
    """Tests for the Marvin Sun action"""
    def assertSunOutput(self, expectedOutput):
        """Test that marvin knows when the sun comes up, given an input file"""
        response = self.createResponseFrom("sun", "sun")
        with mock.patch("irc2phpbb.marvin_actions.requests") as r:
            r.get.return_value = response
            self.assertActionOutput(marvin_actions.marvinSun, "sol", expectedOutput)

    def testSun(self):
        """Test that marvin sends the sunrise and sunset times """
        self.assertSunOutput(
            "Idag går solen upp 7:12 och ner 18:21. Iallafall i trakterna kring BTH.")

    def testSunError(self):
        """Tests that marvin returns the proper error message when joke API is down"""
        with mock.patch("irc2phpbb.marvin_actions.requests.get", side_effect=Exception("API Down!")):
            self.assertStringsOutput(marvin_actions.marvinSun, "när går solen ner?", "sun", "error")
