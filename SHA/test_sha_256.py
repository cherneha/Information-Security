from unittest import TestCase
import sha256
from bitarray import bitarray


class TestPrep(TestCase):
    def test_get_K(self):
        self.assertEqual(sha256.get_K(28), 419)
        self.assertEqual(sha256.get_K(1128), 343)
        self.assertEqual(sha256.get_K(447), 0)


class TestRight_shift(TestCase):
    def test_right_shift(self):
        self.assertEqual(sha256.right_shift(bitarray('00000'), 2), bitarray('00000'))
        self.assertEqual(sha256.right_shift(bitarray('111111'), 6), bitarray('000000'))
        self.assertEqual(sha256.right_shift(bitarray('100000'), 2), bitarray('001000'))
        self.assertEqual(sha256.right_shift(bitarray('100000'), 3), bitarray('000100'))
        self.assertEqual(sha256.right_shift(bitarray('100000'), 4), bitarray('000010'))


class TestRight_rotate(TestCase):
    def test_right_rotate(self):
        self.assertEqual(sha256.right_rotate(bitarray('00001111'), 1), bitarray('10000111'))
        self.assertEqual(sha256.right_rotate(bitarray('00001111'), 2), bitarray('11000011'))
        self.assertEqual(sha256.right_rotate(bitarray('00001111'), 3), bitarray('11100001'))
        self.assertEqual(sha256.right_rotate(bitarray('00001111'), 4), bitarray('11110000'))


class TestSha256(TestCase):
    def test_sha256(self):
        self.assertEqual(sha256.sha256('abc'), 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad')
        self.assertEqual(sha256.sha256(''), 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
        self.assertEqual(sha256.sha256('abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq'),
                         '248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1')
