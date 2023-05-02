enc = b'$&\xb1&+\xce\x02KVTy.4\xfb\xcc/\xc2\xc7`\xd6_\x9beA\t\xfaZ_O\xe9\x8f\x15PDt$h\x1b\x8be+c_vxoR\xf0S\x13\xd1|\xaa\x94\x1b\x8d\x80\xca\xf0\xb2P)I9\xde8\xa3\xb5B/r-\x89N\x00*dq\xe3\xfeM\xc7\x08\x8f23\xc8\x8a\xaa\x11\xdd\xc6\xae\x14\n\x88%=\xba\xdaz\xa8\x96\x1bej\xeb\x8d\xdc\xa4\xf9\x0e\xca\x0b\x9e\x1ec\xaf\x0e\xad\xb5\xbb\xf7T0"s\x8d'
p = 0xe74323831eb55c202607e606d73646dc3e76f8752857fcdb70dd5d3abda1fd21a502c7976ba87973d86921cd2f79465a14460c0b5855e88ad6bab4e885247e7b
g = 0x2cfeb783fcfb4f0b54afc487f7c956ec88f078875b4beb7be6c0adb51cf52531f62450a9374d1e7bab3915aa80190837baf8ca7504693873e259c6c91a73399b44c400228130b7d98aab9657aba6a9e3d8f6e67d60fe0685a47a3c2620c6b93da06aced36b3fa2754008d1918c0f88edcdef0830923e2cb1d63237d9820a56c4
y = 0xc1f678709ded6735f4d4f4246ceb9d9c00a39ee6f80a1440c523f2e444dea7eda367f706b20787724e21ed4047e8caaa97e7bb3f0819a51966d1908ebe471dfed24cef8706a8a3325f99bedcc9b521f232e318c877f43084db539eebcc26752f1176b684672da078c502e3685d97514b3dd43592392d7cdfb40b7cb812da416
m = 0xe8db2bdd27d0273cc3341bb2484ccb696093b161d10a92c35d5248c6e16c754d47a496c444c67ed0b20a1eae5dc09182e2124d623eec5faaccf31b1fe19c3a4c9384147eeea85f3e71cf6e515f64fc1afb634f9455c6ed0990fd618c042c9b9d8a4e3c790347e4f642cfae94ff238cc7b41f7e96196a606ea6fd9702eca8c11
r = 0x24a624219a6ceeab177e301cccd67a140ec457c2dc76f357f5baae089b066f8e09df7efe15375aa3f8f3c4ee83a349ea843d7c6979e1b16b931a65fb092fa96c6c45ceefada3558b9b1241ff64429f2f8d9c10fbd6f68a2cb4bd8f1fad3e4b7f706411410492ee4451e2609ccc30c151aacb9cac6529aa19bf4192d0398a8dc7
s = 0x30459e3728ad4f8a5901139230208ad4edc0158f0553cd43bf058f1602419d6e08c3f61a2537f0b91a7ed3c6980dcd9522c3b6aa5208cc445e01f54237a4b6ff0922876d9ea0abfb705ed7c0d7cabcab22671b51cf5a056b32a383eb863593b0808b5003eb5edd669451f5fab1418f2a34b49db5730934cecf5843140f67a5fb
phi = p*(p-1)//2

from Crypto.Util.number import long_to_bytes
from Crypto.Util.strxor import strxor

## attack idea:
# most common example. The "random and secure" variable k has been re-used for multiple messages

## y = pow(g, x, p²)
# the multiplicative group of Z mod p² is isomorphic to Z_p×Z_p* which has order p*(p-1)

def p_log(y):
    ## this is the p-adic logarithm
    # it solves the logarithm only for the subbgroup of size p^n and not (p-1)
    # p-1 still requires DLP
    x = pow(y, phi, p**3)//p**2
    return x

## x, k mod p. mod p-1 is unknown
x0 = p_log(y)*pow(p_log(g), -1, p) % p
k0 = p_log(r)*pow(p_log(g), -1, p) % p

## to get all of k from only k0 which is about half. We use that
## sha512(k_) + sha512(k_) == k == (2⁵¹² + 1)*k0
k_half = k0*pow(2**512+1, -1, p) % p

for i in range(1000):
    k = k_half + i*p ## since sha512 could be slightly larger than p
    k = (2**512 + 1)*k
    if r == pow(g, k, p**2):
        print("debug:", i)
        break
assert r == pow(g, k, p**2)

x = (s*k - m)*pow(r, -1, phi) % phi
assert y == pow(g, x, p**2)


## get flag with x
flag = strxor(enc, long_to_bytes(x)).strip(b'\0')
print(flag)
assert flag == open('flag.txt', 'rb').read()
