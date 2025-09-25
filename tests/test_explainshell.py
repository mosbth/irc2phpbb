"""
Tests for the Marvin Explain Shell action
"""

from test_action import ActionTest
from irc2phpbb import marvin_actions

class ExplainShellTest(ActionTest):
    """Tests for the Marvin Explain Shell action"""
    def testExplainShell(self):
        """Test that marvin can explain shell commands"""
        url = "https://explainshell.com/explain?cmd=pwd"
        self.assertActionOutput(marvin_actions.marvinExplainShell, "explain pwd", url)
        self.assertActionOutput(marvin_actions.marvinExplainShell, "can you explain pwd", url)
        self.assertActionOutput(
            marvin_actions.marvinExplainShell,
            "förklara pwd|grep -o $user",
            f"{url}%7Cgrep+-o+%24user")

        self.assertActionSilent(marvin_actions.marvinExplainShell, "explains")
