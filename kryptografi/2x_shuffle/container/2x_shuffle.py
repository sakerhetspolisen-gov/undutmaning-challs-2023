#! /usr/local/bin/python3
"""
# Party Rock
Do the shuffle 😎

[LMFAO](youtube.com/watch?v=KQ6zr6kCPj8)
"""

import random

def main():
    flag = open('/app/flag.txt', 'rb').read()
    a = list(range(len(flag)))
    random.shuffle(a)
    b = bytearray(list(range(256)))
    random.shuffle(b)

    enc_flag = bytearray(len(flag))
    for i in range(len(flag)):
        enc_flag[i] = b[flag[a[i]]]
    print('Encrypted flag:', enc_flag.hex())

    while True:
        text = input('Hex to encrypt: ')
        try:
                text = bytes.fromhex(text)
        except:
                print('Malformed hex input!')
                continue
        if len(text) != len(flag):
            print('Wrong length!')
            continue
        out = bytearray(len(text))
        for i in range(len(text)):
            out[i] = b[text[a[i]]]
        print(out.hex())

if __name__ == '__main__':
    main()
