"""
Tests for the Marvin Joke action
"""

from unittest import mock

from test_action import ActionTest
from irc2phpbb import marvin_actions

class JokeTest(ActionTest):
    """Tests for the Marvin Joke action"""
    def assertJokeOutput(self, exampleFile, expectedOutput):
        """Assert that a joke is returned, given an input file"""
        response = self.createResponseFrom("joke", exampleFile)
        with mock.patch("irc2phpbb.marvin_actions.requests") as r:
            r.get.return_value = response
            self.assertActionOutput(marvin_actions.marvinJoke, "joke", expectedOutput)

    def testJokeRequest(self):
        """Test that marvin sends a proper request for a joke"""
        with mock.patch("irc2phpbb.marvin_actions.requests") as r:
            self.executeAction(marvin_actions.marvinJoke, "joke")
            self.assertEqual(
                r.get.call_args.args[0],
                "https://api.chucknorris.io/jokes/random?category=dev")

    def testJoke(self):
        """Test that marvin sends a joke when requested"""
        self.assertJokeOutput("joke", "There is no Esc key on Chuck Norris' keyboard, because no one escapes Chuck Norris.")

    def testJokeError(self):
        """Tests that marvin returns the proper error message when joke API is down"""
        with mock.patch("irc2phpbb.marvin_actions.requests.get", side_effect=Exception("API Down!")):
            self.assertStringsOutput(marvin_actions.marvinJoke, "kör ett skämt", "joke", "error")
