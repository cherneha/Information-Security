from bitarray import bitarray
import random as rn
from utils import multiply_binary, bitarray_to_str
import struct


f = bitarray('1' + '0' * 174 + "10111")
f_test = bitarray("1011")

class Field_2m:
    def __init__(self, irreducible_polynomial):
        self.f = irreducible_polynomial
        self.m = 179

    def add(self, a, b):
        if len(a) < len(b):
            a = bitarray('0' * (len(b) - len(a))) + a
        if len(a) > len(b):
            b = bitarray('0' * (len(a) - len(b))) + b
        # print("<-----------")
        # print(a)
        # print(b)
        # print("----------->")
        return a ^ b

    def divide_remainder(self, a, b):
        a_degree = len(a) - 1
        b_degree = len(self.f) - 1
        while a_degree > b_degree - 1:
            # print(b)
            # print("prod = ", a)
            b_ext = b
            if len(a) > len(b):
                b_ext = b + bitarray('0' * (len(a) - len(b)))
            a = a ^ b_ext
            i = 0
            while i < len(a) - 1 and a[i] == False:
                i += 1
            a = a[i:]
            a_degree = len(a) - 1
        return a

    def multiply(self, a, b):
        product = multiply_binary(a, b)
        return self.divide_remainder(product, self.f)

    def square(self, num):
        return self.multiply(num, num)

    def divide_quotient(self, num, numR):
        """Returns the quotient of the polynomial division num/numR"""
        num = bitarray_to_str(num)
        numR = bitarray_to_str(numR)
        P = int(num, 2)
        R = int(numR, 2)
        degP = len(num) - 1
        degR = len(numR) - 1
        Q = 0
        prevDegree = degP - degR
        for i in range(prevDegree, -1, -1):
            setDeg = degP - degR
            Q = Q << 1
            if i == setDeg:
                R_1 = R << setDeg
                P = P ^ R_1
                degP = len(bin(P)[2:]) - 1
                Q = Q ^ 1
        return bitarray(bin(Q)[2:])

    def inverse(self, a):
        t = bitarray('0')
        r = self.f
        new_t = bitarray('1')
        new_r = a
        count = 0
        while int(new_r.to01(), 2) != 0:
            # print("t = ", t)
            # print("new_t = ", new_t)
            # print("r = ", r)
            # print("new_r = ", new_r)
            quotient = self.divide_quotient(r, new_r)
            # print("quotient = ", quotient)
            # print("------------------------------")

            temp = new_r
            new_r = self.add(r, multiply_binary(quotient, new_r))
            r = temp

            temp = new_t
            new_t = self.add(t, multiply_binary(quotient, new_t))
            t = temp

            count += 1

        i = 0
        while i < len(r) - 1 and r[i] == False:
            i += 1
        r = r[i:]

        if len(r) > 1:
            print("Either f is not irreducible or a is a multiple of f")
            return -1
        return t

    def trace(self, x):
        t = x
        for i in range(1, self.m - 1):
            t = self.add(self.square(t), x)
        return t

    def half_trace(self, x):
        t = x
        for i in range(1, int((self.m - 1) / 2)):
            t = self.add(self.square(self.square(t)), x)
        return t

    def solve_quadratic(self, u, w):
        # print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        # print("u = ", u)
        # print("w = ", w)
        if int(u.to01(), 2) == 0:
            print("oh nooo, u = 0")
            return -1
        if int(w.to01(), 2) == 0:
            z = bitarray('0')
        else:
            # print("self.square(self.inverse(u)", self.square(self.inverse(u)))
            v = self.multiply(w, self.square(self.inverse(u)))
            tr = self.trace(v)
            # print("v = ", v)
            # print("tr = ", tr)
            if int(tr.to01(), 2) == 1:
                z = bitarray('0')
            else:
                t = self.half_trace(v)
                z = self.multiply(t, u)
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return z



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class EllipticCurve:

    def __init__(self):
        self.A = bitarray('1')
        self.B = bitarray(format(0x4A6E0856526436F2F88DD07A341E32D04184572BEB710, 'b'))
        self.m = 179
        self.n = 0x3FFFFFFFFFFFFFFFFFFFFFFB981960435FE5AB64236EF
        self.field = Field_2m(f)

    def get_rand_field_element(self,  m):
        return bitarray(format(rn.getrandbits(m), '010b'))

    def generate_point_on_curve(self):
        u = self.get_rand_field_element(self.m)
        w = self.field.add(
            self.field.multiply(self.field.square(u), u),
            self.field.multiply(self.field.square(u), self.A))
        w = self.field.add(w, self.B)
        z = self.field.solve_quadratic(u, w)
        print("u = ", u)
        print("z = ", z)
        return Point(u, z)

    def add_points(self, a, b):
        lambd = self.field.divide_quotient(self.field.add(a.y, b.y),
                                           self.field.add(a.x, b.x)
                                           )
        x3 = self.field.add(
            self.field.add(self.field.square(lambd),
                            lambd),
            self.field.add(a.x, self.field.add(b.x, self.A)))

        y3 = self.field.multiply(lambd,
                                 self.field.add(a.x, x3))
        y3 = self.field.add(self.field.add(x3, a.y),
                            y3)

        return Point(x3, y3)

    def double(self, x):
        x3 = self.field.add(self.field.square(x.x),
                            self.field.divide_quotient(self.B, self.field.square(x.x)))
        y3 = self.field.add(self.field.square(x.x),
                            self.field.multiply(self.field.add(x.x, self.field.divide_quotient(x.y, x.x)), x3))
        y3 = self.field.add(y3, x3)

        return Point(x3, y3)


if __name__ == '__main__':
    # a = bitarray('1010011')
    # p = bitarray('100011011')
    # b = bitarray('11001010')
    ec = EllipticCurve()
    a = ec.generate_point_on_curve()
    b = ec.generate_point_on_curve()
    double = ec.double(b)
    print("sum = ")
    print(double.x)
    print(double.y)
    # print(field.divide_quotient(bitarray('1010011'), bitarray('00000100')))
    # print(field.divide_remainder(bitarray('1001'), bitarray('1001')))
    # irreducible_polinomial = bitarray("100011011")
    # print(int(bitarray('0000').to01(), 2))

