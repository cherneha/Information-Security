import unittest
from bitarray import bitarray
from elliptic_curve import Field_2m

class TestStringMethods(unittest.TestCase):

    def test_divisions(self):
        field = Field_2m(bitarray("1011"))
        self.assertEqual(field.divide_quotient(bitarray('10011'), bitarray('111')), bitarray('110'))
        self.assertEqual(field.divide_quotient(bitarray('11111111'), bitarray('1010')), bitarray('11001'))
        self.assertEqual(field.divide_quotient(bitarray('1001'), bitarray('1001')), bitarray('1'))

        self.assertEqual(field.divide_remainder(bitarray('10011'), bitarray('111')), bitarray('1'))
        self.assertEqual(field.divide_remainder(bitarray('11111111'), bitarray('1010')), bitarray('101'))
        self.assertEqual(field.divide_remainder(bitarray('1001'), bitarray('1001')), bitarray('0'))

    def test_multiplication(self):
        field = Field_2m(bitarray("100011011"))
        self.assertEqual(field.multiply(bitarray('11001010'), bitarray('1010011')), bitarray('1'))

        field = Field_2m(bitarray("1011"))
        self.assertEqual(field.multiply(bitarray('111'), bitarray('101')), bitarray('110'))

    def test_inverse(self):
        a = bitarray('1010011')
        p = bitarray('100011011')
        field = Field_2m(p)
        self.assertEqual(field.inverse(a), bitarray('11001010'))


if __name__ == '__main__':
    unittest.main()