"""Tests for MOOD server."""

import multiprocessing
import socket
import time
import unittest

from mood.server.__main__ import serve


class TestServer(unittest.TestCase):
    """Test server."""

    def setUp(self):
        """Start server and connect client."""
        self.server = multiprocessing.Process(target=serve)
        self.server.start()
        time.sleep(1)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(1)
        self.sock.connect(("localhost", 1337))

        self.sock.sendall(b"test\n")
        self.read_until("OK")

        self.sock.sendall(b"movemonsters off\n")
        self.read_until("Moving monsters: off")

    def tearDown(self):
        """Stop server."""
        self.sock.close()
        self.server.terminate()
        self.server.join()

    def read_until(self, text):
        """Read socket until text appears."""
        answer = ""

        while text not in answer:
            answer += self.sock.recv(4096).decode()

        return answer

    def test_addmon(self):
        """Test addmon command."""
        self.sock.sendall(
            b'addmon dragon hp 30 hello "I am dragon" coords 1 0\n'
        )
        answer = self.read_until("test added monster dragon")

        self.assertIn("test added monster dragon to (1, 0) with 30 hp", answer)

    def test_encounter(self):
        """Test encounter with monster."""
        self.sock.sendall(
            b'addmon dragon hp 30 hello "I am dragon" coords 1 0\n'
        )
        self.read_until("test added monster dragon")

        self.sock.sendall(b"right\n")
        answer = self.read_until("Moved to (1, 0)")

        self.assertIn("I am dragon", answer)
        self.assertIn("Moved to (1, 0)", answer)

    def test_attack(self):
        """Test attack command."""
        self.sock.sendall(
            b'addmon dragon hp 30 hello "I am dragon" coords 1 0\n'
        )
        self.read_until("test added monster dragon")

        self.sock.sendall(b"right\n")
        self.read_until("Moved to (1, 0)")

        self.sock.sendall(b"attack dragon with sword\n")
        answer = self.read_until("20 hp left")

        self.assertIn("test attacked dragon with sword", answer)
        self.assertIn("damage 10", answer)
        self.assertIn("20 hp left", answer)


if __name__ == "__main__":
    unittest.main()