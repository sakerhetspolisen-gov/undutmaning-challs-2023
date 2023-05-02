n = 0x586b9ccedd9cf4377e5c5bfa55e914c08664df576ad93c7d5daa2f126b9ca18bd2d752350d47433f7c046a197ce873526291480d21068a0d29b46a1c4b0c8933d0122215fa42915c68809d0e2a851e3fc0d77fa5bcf8e82c8b7c8a1815b6778c9606e47ef19da1aa7909a9b2b273bab42481fec9962cec52a25263c2f4290e2b
c = 0x33ef96cc957970c704a712fdefbd92f468dbaeed06c1f4aa1b31e6a956e5aac73b0582cab4fc3fd7ca277064b0a8a2a8dd586d7f3016b46810ef0ebc1c552bfaf302aedd6e6650c0780b5fa967a38d367d12215446f20cbac1611fc7872a61b814dfb5e60779c72fd8653d085eb67fecd542ce9d5beb24255a2397e992d993cb
e = 65537
nbits = 512
a = 0xc370fa2b2e80908dd1de805a016a3c2f81d9e9072ce6f342adf77c6e60f07d85aee387ec93f2788e20356aa402d45c21a01cafbb550f10fbf07945d03e9824cf
b = 0xd95193db2057dc835c42000f00c039eb89f4078a4290d98618858d3eca968dce530df230c2d67e0d9ef5681b50aa077360a2a2156cc04637ebf517a2a356fe74

# notice that the rng is a linear congruential generator where each output will be the seed for the next
# if the first output is p, then p will be the seed for q = p*a + b mod 2^nbits
# n = p*q = p*(p*a + b) mod 2^nbits which only has one unknown variable
# the equations are also true for all smaller powers of 2
# can use BFS/DFS on bits in 2-adics to solve for p
# could also use Hensel's lemma for p-adics but in this case 2 is a small enough prime and is fast enough to brute force each digit

# BFS implementation
queue0 = [0]
for i in range(nbits):
    queue1 = []
    if len(queue0) > 1000: # queue0 has at most 4 elements in practice
        print(i, len(queue0))
    for guess0 in queue0:
        for digit in range(2): # test all combinations for this digit in base 2
            guess1 = digit * 2**i + guess0
            if (n - guess1*(guess1*a + b)) % 2**(i+1) == 0: # discard all dead branches and store satisfying solutions
                queue1.append(guess1)
    queue0 = queue1
print(f'{len(queue0) = }')

# find correct solution
for guess in queue0:
    if (n//guess)*guess == n:
        print('Found prime!')
        p = guess

# generate private key and decrypt message
print(f'{p = :0{nbits//4}x}')
q = n//p
phi = (p-1)*(q-1)
d = pow(e, -1, phi)
m = pow(c, d, n)
from Crypto.Util.number import long_to_bytes
m = long_to_bytes(m)
print(m)
