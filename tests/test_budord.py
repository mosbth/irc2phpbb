"""
Tests for the Marvin Budord action
"""

from test_action import ActionTest
from irc2phpbb import marvin_actions

class BudordTest(ActionTest):
    """Tests for the Marvin Budord action"""
    def testBudord(self):
        """Test that marvin knows all the commandments"""
        for n, _ in enumerate(self.strings.get("budord"), 1):
            self.assertStringsOutput(marvin_actions.marvinBudord, f"budord #{n}", "budord", f"{n}")

        self.assertStringsOutput(marvin_actions.marvinBudord,"visa stentavla 1", "budord", "1")
        self.assertActionSilent(marvin_actions.marvinBudord, "var är stentavlan?")
