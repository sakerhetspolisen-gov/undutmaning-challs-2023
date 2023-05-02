import sys
import math


IMAGE_IS_SQUARE = False
SET_MEANS_WHITE = True


def usage():
    print("""
    Usage:

        $ python3 transformer.py <hex-sequence>

    E.g:

        $ python3 transformer.py '7a:23:45:23:21'
    """)

def parse_seq(seq):
    return [int(e, 16) for e in seq.split(':')]

def calculate_size(byteseq):
    if not IMAGE_IS_SQUARE:
        return 0, 8*len(byteseq)
    columns = int(math.sqrt(8*len(byteseq)))
    padding = 8*len(byteseq) - columns * columns
    return padding,columns

def get_bits(byteseq):
    for b in byteseq:
        for bit in reversed(range(8)):
            yield (b >> bit) & 1

if SET_MEANS_WHITE: pxcodes = (219,255)
else: pxcodes = (255,219)
pixel = [bytes((cp,cp)).decode('cp437') for cp in pxcodes]

def bit_to_ascii_pixel(bit):
    return pixel[bit]

def transform(seq):
    byteseq = parse_seq(seq)
    padding,columns = calculate_size(byteseq)
    col_ix = 0
    for bit in get_bits(byteseq):
        if padding:
            padding -= 1
            continue
        sys.stdout.write(bit_to_ascii_pixel(bit))
        col_ix += 1
        if col_ix >= columns:
            sys.stdout.write('\n')
            col_ix = 0
    if col_ix:
        sys.stdout.write('\n')

if len(sys.argv) != 2:
    usage()
else:
    transform(sys.argv[1])

