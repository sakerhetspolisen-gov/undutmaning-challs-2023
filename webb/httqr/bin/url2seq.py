import qrcode


def url2bitmap(url):
    encoder = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=1,
            border=1)
    encoder.add_data(url)
    encoder.make()
    bitmap = [[int(e) for e in r] for r in encoder.modules]
    row_count = len(bitmap)
    column_count = len(bitmap[0])
    return bitmap, (row_count, column_count)


def bitmap2bitseq(bitmap):
    bitseq = []
    for row in bitmap:
        bitseq.extend(row)
    return bitseq


def bitseq2byteseq(bitseq):
    octets = []
    offset = 0
    bitseq = list(reversed(bitseq))
    while offset < len(bitseq):
        octets.append(int(''.join(['01'[i] for i in reversed(bitseq[offset:min(offset+8, len(bitseq))])]), 2))
        offset += 8
    octets.reverse()
    return octets


def byteseq2str(byteseq):
    """
    Converts the byte sequence to a string in the same format as is used in the
    common way of presenting X509 files, so that it useful for setting string
    values, such as a subjectAltName DNS value.
    """
    seqstr = ':'.join(['%02x' % e for e in byteseq])
    return seqstr


def byteseq2int(byteseq):
    """
    Converts the byte sequence to a (very large) integer value, suitable for use
    as certificate sequence number.
    """
    val = 0
    for b in byteseq:
        val = (val << 8) | b
    return val


def url2seq(url):
    bitmap,mapsize = url2bitmap(url)
    bitseq = bitmap2bitseq(bitmap)
    byteseq = bitseq2byteseq(bitseq)
    strseq = byteseq2str(byteseq)
    intseq = byteseq2int(byteseq)
    return strseq,intseq,mapsize


# A typical URL value would be
# url = 'abcdetap7o7pux6fxpnxrbqvto6dypr3tx3befc7bpon6gn5m4tsftqd.onion/java'
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='URL to byte sequence transformer')
    parser.add_argument('-u', '--url', required=True, metavar='<url>', help='URL to transform')
    parser.add_argument('-c', '--size', action='store_true', help='Print the size of the bitmap (initially intended to be 33x33). Overrides other output requests.')
    parser.add_argument('-s', '--str', action='store_true', help='Output the sequence as a X509 hex value string. Overrides request for integer value output.')
    parser.add_argument('-i', '--int', action='store_true', help='Output the sequence as a single integer value.')
    args = parser.parse_args()

    seq,val,sz = url2seq(args.url)

    if args.size:
        print('%dx%d' % sz)
    elif args.str:
        print(seq)
    elif args.int:
        print(val)

