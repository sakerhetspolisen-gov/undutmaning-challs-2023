def parse_seq(seq):
    return [int(e, 16) for e in seq.split(':')]

def get_bits(byteseq):
    for b in byteseq:
        for bit in reversed(range(8)):
            yield (b >> bit) & 1

pixel = [bytes((cp,cp)).decode('cp437') for cp in (255,219)]
def bit_to_ascii_pixel(bit):
    return pixel[bit]

