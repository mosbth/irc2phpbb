"""
Tests for the Marvin Commit action
"""

from unittest import mock

import requests

from test_action import ActionTest
from irc2phpbb import marvin_actions

class CommitTest(ActionTest):
    """Tests for the Marvin Commit action"""
    def testCommitRequest(self):
        """Test that marvin sends proper requests when generating commit messages"""
        with mock.patch("irc2phpbb.marvin_actions.requests") as r:
            self.executeAction(marvin_actions.marvinCommit, "vad skriver man efter commit -m?")
            self.assertEqual(r.get.call_args.args[0], "https://whatthecommit.com/index.txt")

    def testCommitResponse(self):
        """Test that marvin properly handles responses when generating commit messages"""
        message = "Secret sauce #9"
        response = requests.models.Response()
        response._content = str.encode(message)
        with mock.patch("irc2phpbb.marvin_actions.requests") as r:
            r.get.return_value = response
            expected = f"Använd detta meddelandet: '{message}'"
            self.assertActionOutput(marvin_actions.marvinCommit, "commit", expected)

    def testCommitReaction(self):
        """Test that marvin only generates commit messages when asked"""
        self.assertActionSilent(marvin_actions.marvinCommit, "nocommit")


    def testCommitError(self):
        """Tests that marvin sends the proper message when get commit fails"""
        with mock.patch("irc2phpbb.marvin_actions.requests.get", side_effect=Exception('API Down!')):
            self.assertStringsOutput(
                marvin_actions.marvinCommit,
                "vad skriver man efter commit -m?",
                "commit",
                "error")
