import unittest
import prog

class TestSome(unittest.TestCase):

    def test_normal(self):
        self.assertEqual(prog.funct(1, 2), 1.5)

    def test_exception(self):
        with self.assertRaises(ZeroDivisionError):
            prog.funct(1, 0)

    def test_type_err(self):
        with self.assertRaises(TypeError):
            prog.funct(1, "0")

