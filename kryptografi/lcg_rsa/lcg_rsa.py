from os import urandom
from Crypto.Util.number import isPrime, bytes_to_long

nbits = 512
mask = (1 << nbits) - 1
state = bytes_to_long(urandom(nbits//8)) | 1
a = 0xc370fa2b2e80908dd1de805a016a3c2f81d9e9072ce6f342adf77c6e60f07d85aee387ec93f2788e20356aa402d45c21a01cafbb550f10fbf07945d03e9824cf
b = 0xd95193db2057dc835c42000f00c039eb89f4078a4290d98618858d3eca968dce530df230c2d67e0d9ef5681b50aa077360a2a2156cc04637ebf517a2a356fe74
def rng():
    global state
    state = (state*a + b) & mask
    return state

def gen_key():
    while True:
        p, q = rng(), rng()
        if isPrime(p) and isPrime(q):
            n = p*q
            e = 65537
            phi = (p - 1)*(q - 1)
            d = pow(e, -1, phi)
            return (n, e), (n, d)

(n, e), priv = gen_key()
print(f'n = 0x{n:x}')
m = bytes_to_long(open('flag.txt', 'rb').read())
c = pow(m, e, n)
print(f'c = 0x{c:x}')