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

def right_shift(bin, count):
    return (bitarray('0') * count) + bin[:-count]

def right_rotate(bin, n):
    return bin[-n:] + bin[:-n]

def add_mod_2(*args):
    sum = bitarray(32 * '0')
    for arg in args:
        shift = 0
        for i in range(31, -1, -1):
            bit_sum = int(arg[i]) + int(sum[i]) + shift
            sum[i] = bool(bit_sum % 2)
            if bit_sum > 1:
                shift = 1
            else:
                shift = 0
    return sum

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
    # pad with zeros
    m.extend([False] * get_K(L))

    # append 64-bit message length
    end = bitarray(format(L, '0>64b'), endian='big')
    m = m + end
    return m

def process_in_chunks(m):
    h0 = bitarray(format(0x6A09E667, '0>32b'))
    h1 = bitarray(format(0xBB67AE85, '0>32b'))
    h2 = bitarray(format(0x3C6EF372, '0>32b'))
    h3 = bitarray(format(0xA54FF53A, '0>32b'))
    h4 = bitarray(format(0x510E527F, '0>32b'))
    h5 = bitarray(format(0x9B05688C, '0>32b'))
    h6 = bitarray(format(0x1F83D9AB, '0>32b'))
    h7 = bitarray(format(0x5BE0CD19, '0>32b'))

    n = math.floor(len(m) / 512)
    w = [bitarray(False * 32)] * 64
    for i in range (0, n):
        chunk = m[i * 512 : (i + 1) * 512]
        for j in range(0, 16):
            slice = chunk[j * 32 : (j + 1) * 32]
            w[j] = slice

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7

        for j in range (16, 64):
            s0 = right_rotate(w[j - 15], 7) ^ right_rotate(w[j - 15], 18) ^ right_shift(w[j - 15], 3)
            s1 = right_rotate(w[j - 2], 17) ^ right_rotate(w[j - 2], 19) ^ right_shift(w[j - 2], 10)
            w[j] = add_mod_2(w[j - 16], s0, w[j - 7], s1)

        for j in range(0, 64):
            S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = add_mod_2(h, S1, ch, bitarray(format(constants[j], '0>32b')), w[j])
            S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = add_mod_2(S0, maj)

            h = g
            g = f
            f = e
            e = add_mod_2(d, temp1)
            d = c
            c = b
            b = a
            a = add_mod_2(temp1, temp2)

        h0 = add_mod_2(h0, a)
        h1 = add_mod_2(h1, b)
        h2 = add_mod_2(h2, c)
        h3 = add_mod_2(h3, d)
        h4 = add_mod_2(h4, e)
        h5 = add_mod_2(h5, f)
        h6 = add_mod_2(h6, g)
        h7 = add_mod_2(h7, h)

    hash = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7
    return hash

def to_hex(bin):
    hex = ""
    for i in range(0, int(len(bin)/4)):
        block = bin[i * 4: (i + 1) * 4]
        num = block[0] * 8 + block[1] * 4 + block[2] * 2 + block[3] * 1
        hex += str(format(num, 'x'))
    return hex

def sha256(text):
    m = prepare(text)
    hash = process_in_chunks(m)
    hex = to_hex(hash)
    return hash

if __name__ == '__main__':
    sha256("")
