"""
Tests for the Marvin Lunch action
"""

from unittest import mock

from test_action import ActionTest
from irc2phpbb import marvin_actions

class LunchTest(ActionTest):
    """Tests for the Marvin Lunch action"""
    def testLunchLocations(self):
        """Test that marvin can provide lunch suggestions for certain places"""
        locations = ["karlskrona", "goteborg", "angelholm", "hassleholm", "malmo"]
        with mock.patch("irc2phpbb.marvin_actions.random") as r:
            for location in locations:
                for i, place in enumerate(self.strings.get("lunch").get("location").get(location)):
                    r.randint.side_effect = [0, i]
                    self.assertActionOutput(
                        marvin_actions.marvinLunch, f"mat {location}", f"Ska vi ta {place}?")
            r.randint.side_effect = [1, 2]
            self.assertActionOutput(
                marvin_actions.marvinLunch, "dags att luncha", "Jag är lite sugen på Indiska?")
        self.assertActionSilent(marvin_actions.marvinLunch, "matdags")
