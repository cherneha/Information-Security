import SHA.sha256 as sha256
import math
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

def RSASP1(K, m):
    n, d = K
    s = (m ** d) % n
    return s

def RSAVP1(public_key, s):
    n, e = public_key
    m = (s ** e) % n
    return m

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

if __name__ == '__main__':
    key = RSA.generate(1024)
    privateKey = key.exportKey('DER')
    publicKey = key.publickey().exportKey('DER')
    n = key.n
    d = key.d
    e = key.e
    message = "happy kitty, sleepy kitty"
    signature = RSASSA_PKCS1_V1_5_SIGN((n, d), message)
    RSASSA_PKCS1_V1_5_VERIFY((n, e, 1024), message, signature)

