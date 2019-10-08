import numpy as np
import math
from bitarray import bitarray

constants = np.array([ 0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
                       0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
                       0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
                       0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
                       0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
                       0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
                       0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
                       0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2],
                       dtype=np.uint32)



def leftshift(ba, count):
    return ba[count:] + (bitarray('0') * count)

def rightshift(ba, count):
    return (bitarray('0') * count) + ba[:-count]

def moduloAddition(self, *args):
    
    for


def get_K(L):
    rest = (L + 1 + 64) % 512
    floor = math.floor((L + 1 + 64) / 512)
    K = ((floor + 1) * 512 - floor * 512 -  rest) % 512
    return K

def prepare(message):
    m = bitarray()
    m.frombytes(message.encode('utf-8'))
    L = len(m)
    m.append(True)
    m.extend([False] * get_K(L))
    end = bitarray(format(L, 'b'), endian='big')
    print(end)
    p = bitarray(64 - len(end))
    end = p + end
    print(p)
    print(end)
    m = m + end
    return m

def process_in_chunks(m):
    h0 = np.uint32(0x6A09E667)
    h1 = np.uint32(0xBB67AE85)
    h2 = np.uint32(0x3C6EF372)
    h3 = np.uint32(0xA54FF53A)
    h4 = np.uint32(0x510E527F)
    h5 = np.uint32(0x9B05688C)
    h6 = np.uint32(0x1F83D9AB)
    h7 = np.uint32(0x5BE0CD19)

    n = math.floor(len(m) / 512)
    w = [bytearray(False * 32)] * 64
    for i in range (0, n):
        chunk = m[i * 512 : (i + 1) * 512]
        for j in range(0, 16):
            slice = chunk[j * 32 : (j + 1) * 32]
            w[j] = slice
        for j in range (16, 64):
            r1 = rightshift(w[j - 15], 7)
            r2 = rightshift(w[j - 15], 18)
            r3 = rightshift(w[j - 15], 3)
            s0 = r1 ^ r2 ^ r3
            s1 = rightshift(w[j - 2], 17) ^ rightshift(w[j - 2], 19) ^ rightshift(w[j - 2], 10)
            w[j] = moduloAddition(w[j - 16],  s0, w[j - 7] + s1)

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7

        for i in range(0, 64):
            S1 = rightshift(e, 6) ^ rightshift(e, 11) ^ rightshift(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = moduloAddition(h, S1, ch, constants[i], w[i])
            S0 = rightshift(a, 2) ^ rightshift(a, 13) ^ rightshift(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = moduloAddition(S0, maj)

            h = g
            g = f
            f = e
            e = moduloAddition(d, temp1)
            d = c
            c = b
            b = a
            a = moduloAddition(temp1, temp2)

        h0 = moduloAddition(h0, a)
        h1 = moduloAddition(h1, b)
        h2 = moduloAddition(h2, c)
        h3 = moduloAddition(h3, d)
        h4 = moduloAddition(h4, e)
        h5 = moduloAddition(h5, f)
        h6 = moduloAddition(h6, g)
        h7 = moduloAddition(h7, h)

    hash = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7
    return hash

if __name__ == '__main__':
    m = prepare("")
    hash = process_in_chunks(m)
    print(hash)