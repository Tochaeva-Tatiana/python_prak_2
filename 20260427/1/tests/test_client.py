"""Tests for MOOD client."""

import unittest
from unittest.mock import Mock, patch
from mood.client.__main__ import CmdCow


class TestClientCommands(unittest.TestCase):
    """Test client command conversion."""

    def setUp(self):
        """Create fake client."""
        self.writer = Mock()
        self.client = CmdCow("test", None, self.writer)

    def test_addmon_dragon(self):
        """Test addmon command with dragon."""
        self.client.onecmd('addmon dragon hp 30 hello "I am dragon" coords 1 0')

        self.writer.write.assert_called_with(
            b'addmon dragon hp 30 hello "I am dragon" coords 1 0\n'
        )

    def test_addmon_sheep(self):
        """Test addmon command with sheep."""
        self.client.onecmd('addmon sheep hp 10 hello "Baa" coords 2 3')

        self.writer.write.assert_called_with(
            b'addmon sheep hp 10 hello "Baa" coords 2 3\n'
        )

    def test_attack_sword(self):
        """Test attack command with sword."""
        self.client.onecmd("attack dragon with sword")

        self.writer.write.assert_called_with(
            b"attack dragon with sword\n"
        )

    def test_attack_axe(self):
        """Test attack command with axe."""
        self.client.onecmd("attack dragon with axe")

        self.writer.write.assert_called_with(
            b"attack dragon with axe\n"
        )

    def test_wrong_move_arguments(self):
        """Test wrong move arguments."""
        with patch("builtins.print") as mocked_print:
            self.client.onecmd("up bad")

        mocked_print.assert_called_with("Invalid arguments")
        self.writer.write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
