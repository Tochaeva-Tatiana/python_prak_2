import unittest
import prog2
import time
import service
import multiprocessing

class TestSome(unittest.TestCase):

    def test_normal(self):
        self.assertEqual(prog2.sqroots("1 0 -1"), "1.0 -1.0")
        self.assertEqual(prog2.sqroots("1 0 1"), "")
        self.assertEqual(prog2.sqroots("1 -2 1"), "1.0")

    def  test_exeption(self):
        with self.assertRaises(ValueError):
            prog2.sqroots("2 4")

@classmethod
def setUpClass(cls):
    cls.proc = multiprocessing.Process(target=service.serve)
    cls.proc.start()
    time.sleep(1)

