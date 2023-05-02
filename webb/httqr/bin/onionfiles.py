import hashlib
import base64


class PrivateKey:

    def __init__(self, key):
        self._key = key
        self._calculate_hashsum()

    def format(self):
        return b'== ed25519v1-secret: type0 ==\x00\x00\x00' + self._hashsum

    def _calculate_hashsum(self):
        hashsum = hashlib.sha512(self._key).digest()
        hashlist = [c for c in hashsum]
        hashlist[0] &= 248
        hashlist[31] &= 127
        hashlist[31] |= 64
        self._hashsum = ''.join([chr(i) for i in hashlist]).encode('latin1')


class PublicKey:

    def __init__(self, key):
        self._key = key
        self._calculate_address()

    def format(self):
        return b'== ed25519v1-public: type0 ==\x00\x00\x00' + self._key

    def address(self):
        return self._address

    def _calculate_address(self):
        checksum = self._calculate_checksum()
        version = b'\x03'
        address_string = self._key + checksum + version
        address = base64.b32encode(address_string).decode('ascii').lower() + '.onion'
        self._address = address

    def _calculate_checksum(self):
        salt = b'.onion checksum'
        version = b'\x03'
        check_string = salt + self._key + version
        hashsum = hashlib.sha3_256(check_string).digest()
        checksum = hashsum[:2]
        return checksum


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser('Converts binary format private and public ED25519 keys to TOR service data files.')
    parser.add_argument('-s', '--secret', metavar='<filename>', required=True, help='32 byte file containing binary version of ED25519 secret key.')
    parser.add_argument('-p', '--public', metavar='<filename>', required=True, help='32 byte file containing binary version of ED25519 public key.')
    args = parser.parse_args()

    private_key_file = 'hs_ed25519_secret_key'
    public_key_file = 'hs_ed25519_public_key'
    address_file = 'hostname'

    with open(args.secret, 'rb') as infile:
        private_key = PrivateKey(infile.read())
    with open(args.public, 'rb') as infile:
        public_key = PublicKey(infile.read())

    with open(private_key_file, 'wb') as outfile:
        outfile.write(private_key.format())
    with open(public_key_file, 'wb') as outfile:
        outfile.write(public_key.format())
    with open(address_file, 'w') as outfile:
        outfile.write('%s\n' % public_key.address())

