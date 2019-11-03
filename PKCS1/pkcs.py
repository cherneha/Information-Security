import SHA.sha256 as sha256
import math
import time
import random as rn
from bitarray import bitarray
from Crypto.PublicKey import RSA

SHA256_octets = [0x30, 0x31, 0x30, 0x0d, 0x06, 0x09, 0x60, 0x86, 0x48, 0x01,
                 0x65, 0x03, 0x04, 0x02, 0x01, 0x05, 0x00, 0x04, 0x20]

def bitarray_to_str(bitarr):
    bitstr = ''
    for i in range(0, len(bitarr)):
        bitstr += str(int(bitarr[i]))
    return bitstr

def RSASSA_PKCS1_V1_5_SIGN(K, message):
    k = 128
    EM = EMSA_PKCS1_v1_5_ENCODE(message, k)
    m = OS2IP(EM)
    s = RSASP1(K, m)
    S = I2OSP(s, k)
    return S

def EMSA_PKCS1_v1_5_ENCODE(message, emLen):
    h = sha256.sha256(message)
    tLen = len(SHA256_octets) + int(len(h) / 8)
    if emLen < tLen + 11:
        print("intended encoded message length too short")
        return None
    DER = bitarray()
    for octet in SHA256_octets:
        octet_decimal = bitarray(format(octet, '0>8b'))
        DER = DER + octet_decimal
    T = DER + h
    PS = bitarray('1' * 8 * (emLen - tLen - 3))
    EM = bitarray('0' * 8) + bitarray('0' * 7 + '1') + PS + bitarray('0' * 8) + T
    return EM

def OS2IP(X):
    xLen = math.ceil(len(X) / 8)
    p = 1
    x = 0
    for i in range(0, xLen):
        octet = bitarray_to_str(X[i * 8 : (i + 1) * 8])
        dec = int(octet, 2)
        x += dec * (256 ** (xLen - p))
        p += 1
    return (x)

def I2OSP(x, xLen):
    if x >= 256 ** xLen:
        print("integer too large")
        return None
    X = bitarray(format(x, 'b'))
    if len(X) < xLen * 8:
        X = bitarray('0' * (xLen * 8 - len(X))) + X
    return X


def power(x, y, p):
    res = 1
    x = x % p
    while y > 0:
        if (y & 1) == 1:
            res = (res * x) % p
        y = y >> 1
        x = (x * x) % p

    return res


def RSASP1(K, m):
    n, d = K
    s = power(m, d, n)
    return s


def RSAVP1(public_key, s):
    n, e = public_key
    m = power(s, e, n)
    return m


def extended_euclid(a, b):
    if (b == 0):
        return a, 1, 0
    d, x, y = extended_euclid(b, a % b)
    return d, y, x - (a // b) * y
    # if b == 0:
    #     return (a, 1, 0)
    # else:
    #     d, x, y = extended_euclid(b, a % b)
    #     return (d, y, x - math.floor(a / b) * y)

def is_prime(n):
    if n % 2 == 0:
        return False
    for i in range(3, math.floor(math.sqrt(n)), 2):
        if n % i == 0:
            return False
    return True


def miller_rabin(n):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2

    for i in range(0, 1500):
        a = rn.randrange(2, n - 1)
        x = power(a, r, n)
        if x != 1 and x != n - 1:
            for j in range(0, s):
                x = power(x, 2, n)
                if x != n - 1:
                    return False
    return True

def generate_prime_candidate(length):
    x = rn.getrandbits(length)
    x |= (1 << length - 1) | 1
    return x

def generate_prime(length=512):
    i = 0
    while True:
        p = generate_prime_candidate(length)
        i += 1
        if miller_rabin(p):
            # if is_prime(p):
            return p

def RSASSA_PKCS1_V1_5_VERIFY(public_key, M, S):
    n, e, modBits = public_key
    k = int(len(S) / 8)
    s = OS2IP(S)
    m = RSAVP1((n, e), s)
    EM = I2OSP(m, math.ceil((modBits - 1) / 8))
    EM2 = EMSA_PKCS1_v1_5_ENCODE(M, k)
    if EM == EM2:
        print("Valid signature")
    else:
        print("Invalid signature")

def gen_keys():
    n = 0
    while len(bitarray(format(n, 'b'))) != 1024:
        p = generate_prime(510)
        q = generate_prime(514)
        n = p * q
    print("p = ", p)
    print("q = ", q)
    fi_n = (p - 1) * (q - 1)
    print("fi(n) = ", fi_n)
    print("n = ", n)
    e = 65537
    res = extended_euclid(e, fi_n)
    print(res)
    d = res[1]
    if d < 0:
        d = d + n
    print("d = ", d)
    print("n len = ", len(bitarray(format(n, 'b'))))
    return (e, d, n)


if __name__ == '__main__':
    start = time.time()
    e, d, n = gen_keys()
    message = "happy kitty, sleepy kitty"
    signature = RSASSA_PKCS1_V1_5_SIGN((n, d), message)
    RSASSA_PKCS1_V1_5_VERIFY((n, e, 1024), message, signature)
    end = time.time()
    print("time elapsed = ", end - start)
