"""
Tests for the Marvin Video of the Day action
"""

from datetime import date, timedelta
from unittest import mock

from test_action import ActionTest
from irc2phpbb import marvin_actions

class VideoOfTodayTest(ActionTest):
    """Tests for the Marvin Video of the Day action"""
    def testVideoOfToday(self):
        """Test that marvin can link to a different video each day of the week"""
        with mock.patch("irc2phpbb.marvin_actions.datetime") as dt:
            for d in range(1, 8):
                day = date(2024, 11, 25) + timedelta(days=d)
                dt.date.today.return_value = day
                weekday = day.strftime("%A")
                weekdayPhrase = self.strings.get("video-of-today").get(weekday).get("message")
                videoPhrase = self.strings.get("video-of-today").get(weekday).get("url")
                response = f"{weekdayPhrase} En passande video är {videoPhrase}"
                self.assertActionOutput(marvin_actions.marvinVideoOfToday, "dagens video", response)
        self.assertActionSilent(marvin_actions.marvinVideoOfToday, "videoidag")
