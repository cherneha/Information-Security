from SHA.sha256 import sha256
from SHA.sha3 import Keccak
from bitarray import bitarray

def hmac(K, message):
    m = bitarray()
    m.frombytes(message.encode('utf-8'))
    H_outside = Keccak().SHA3_256
    H_inside = sha256

    if len(K) > 256:
        K = sha256(K)
    elif len(K) < 256:
        K = K + bitarray('0' * (256 - len(K)))

    opad = bitarray(format(0x5c, '0>8b') * 32)
    ipad = bitarray(format(0x36, '0>8b') * 32)

    hmac = H_outside((K ^ opad) + H_inside((K ^ ipad) + m, True), True)
    return hmac

if __name__ == '__main__':
    print(hmac(bitarray('0101010101'), "little ball of fur"))