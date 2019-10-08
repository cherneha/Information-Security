from unittest import TestCase
import sha256
from bitarray import bitarray


class TestPrep(TestCase):
    def test_get_K(self):
        self.assertEqual(sha256.get_K(28), 419)
        self.assertEqual(sha256.get_K(1128), 343)
        self.assertEqual(sha256.get_K(447), 0)


class TestModuloAddition(TestCase):
    def test_moduloAddition(self):
        self.assertEqual(sha256.moduloAddition(bitarray('1' * 32), bitarray('11111111')), bitarray('01010100'))
