from unittest import TestCase
import sha256

class TestPrep(TestCase):
    def test_get_K(self):
        self.assertEqual(sha256.get_K(28), 419)
        self.assertEqual(sha256.get_K(1128), 343)
        self.assertEqual(sha256.get_K(447), 0)