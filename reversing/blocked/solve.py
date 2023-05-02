import random
from dataclasses import dataclass

BLOCK_SIZE: int = 308

@dataclass
class Value:
    x1: int
    y1: int
    x2: int
    y2: int

def derive_values(k: int) -> Value:
    # enc = 'A'
    # y1 = random.randrange(ord(enc))
    # x1 = ord(enc) ^ y1
    #
    # z1 = x1 ^ y1
    # assert(enc == chr(z1))

    x2: int = random.randrange(k + 1, 128)
    y2: int = random.randrange(x2 - k)

    d:  int = x2 - y2 - k
    x1: int = random.randrange(d)
    y1: int = d - x1
    assert(k == (x2 - y2) - (x1 + y1))
    return Value(x1, y1, x2, y2)

def find_pointers(used: set[int]) -> Value:
    def rand_pointer() -> int:
        return random.randrange(int(BLOCK_SIZE / 2), BLOCK_SIZE) + BLOCK_SIZE

    p: Value = Value(rand_pointer(), 0, rand_pointer(), 0)

    while p.x1 in used:
        p.x1 = rand_pointer()
    used.add(p.x1)

    # while p.y1 in used:
        # p.y1 = rand_pointer()
    # used.add(p.y1)

    while p.x2 in used:
        p.x2 = rand_pointer()
    used.add(p.x2)

    # while p.y2 in used:
        # p.y2 = rand_pointer()
    # used.add(p.y2)

    return p

def encode(encode: str) -> list[int]:
    block: list[int] = [0] * BLOCK_SIZE * 2
    idx: int = 0
    used: set[int] = set()

    for _, val in enumerate(encode):
        v: Value = derive_values(ord(val))
        p: Value = find_pointers(used)

        block[idx] = p.x1
        block[idx + 1] = v.y1 # = p.y1
        block[idx + 2] = p.x2
        block[idx + 3] = v.y2 # = p.y2

        block[p.x1] = v.x1
        # block[p.y1] = v.y1
        block[p.x2] = v.x2
        # block[p.y2] = v.y2

        assert(Value(block[p.x1], block[idx+1], block[p.x2], block[idx+3]) == v) # assert(Value(block[p.x1], block[p.y1], block[p.x2], block[p.y2]) == v)
        idx += 4
    return block

def decode(decode: list[int]) -> str:
    s: str = ''
    idx: int = 0
    while True:
        p: Value = Value(decode[idx], decode[idx + 1], decode[idx + 2], decode[idx + 3])
        v: Value = Value(decode[p.x1], p.y1, decode[p.x2], p.y2) # Value(decode[p.x1], decode[p.y1], decode[p.x2], decode[p.y2])

        z2: int = v.x2 - v.y2
        z1: int = v.x1 + v.y1
        s += chr(z2 - z1)
        if s[-1] == '}':
            break
        idx += 4
    return s

if __name__ == '__main__':
    print(decode(encode(open('flag.txt').read())))
