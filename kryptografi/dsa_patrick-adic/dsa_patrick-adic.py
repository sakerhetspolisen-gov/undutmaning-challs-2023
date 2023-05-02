from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes, isPrime
from Crypto.Util.strxor import strxor
from random import randrange
from hashlib import sha512

def gen_safe_prime(bits):
    count = 0
    while True:
        count += 1
        p = getPrime(bits)
        if isPrime(p//2):
            print("Number of iterations to find a safe prime:", count)
            return p

def sign(x, m):
    # we have fixed the last bug, using cryptographically secure and random k for every new message
    k = sha512(long_to_bytes(m) + long_to_bytes(x)).digest() ## deterministic and secret, fixes bug with bad PRNG
    k = bytes_to_long(k + k) # because we don't have a 1024-bit hash function, it is still 512-bit security

    r = pow(g, k, q)
    s = pow(k, -1, phi)*(m + r*x) % phi
    return (r, s)

def verify(y, r, s, m):
    return r == pow(g, m*pow(s, -1, phi), q) * pow(y, r*pow(s, -1, phi), q) % q

bits = 512
flag = open('flag.txt', 'rb').read()
flag = b'\0'*(bits//4 - len(flag)) + flag

p = gen_safe_prime(bits)
q = p**2
phi = p*(p-1)//2
x = randrange(phi)
enc = strxor(flag, long_to_bytes(x))
print('enc =', enc)

g = randrange(q)**2 % q
y = pow(g, x, q)
m = randrange(phi)

# generate signature
r, s = sign(x, m)
assert verify(y, r, s, m)


# output
print(f"p = {hex(p)}")
print(f"g = {hex(g)}")
print(f"y = {hex(y)}")
print(f"m = {hex(m)}")
print(f"r = {hex(r)}")
print(f"s = {hex(s)}")
