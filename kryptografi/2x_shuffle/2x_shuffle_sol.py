from pwn import remote
r = remote("ip", 1337)

def recvline():
    data = r.recvline()
    # strip Hex to encrypt: \n
    return bytes.fromhex(data[16:-1].decode())

enc = recvline()
length = len(enc)

flag = [None]*length

m = b"\0"*length
r.sendline(m.hex())
byte0 = recvline()[0]
for i in range(length):
    print("i:", i) # position of byte in plaintext
    m = bytearray(b"\0"*length)
    m[i] = b"\1"[0]
    r.sendline(m.hex())
    data = recvline()
    for j in range(length): # get position of byte in ciphertext
        if data[j] != byte0:
            break
    else:
        print("error?", i, j)
        exit(1)

    for byte in range(32, 126): # loop over all printable ASCII chars
        m = bytearray(b"\0"*length)
        m[i] = byte
        r.sendline(m.hex())
        data = recvline()
        if data[j] == enc[j]:
            flag[i] = byte
            break
    else:
        print("error!", i, j)
        exit(1)

flag = bytes(flag)
print(flag)
