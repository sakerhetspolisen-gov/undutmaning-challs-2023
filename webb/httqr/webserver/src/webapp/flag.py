import io
import zipfile
import base64

class Flag:

    _DATA = """
    THISISALLJUSTGARBAGEOFNOSPECIALINTERESTTOYOUHEREGOESNOFLAG
    <HERE GOES THE FLAG>
    ANDHEREGOESEVENMOREUNNECESSARYINFORMATIONYOUCOULD
    JUSTASWELLIGNORE
    """

    def __init__(self, urlsafe=True):
        self._urlsafe = urlsafe

    def __str__(self):
        return self._encode(self._compress(self._DATA))

    def _compress(self, data):
        output = io.BytesIO()
        with zipfile.ZipFile(output, mode='w', compression=zipfile.ZIP_BZIP2) as compressor:
            compressor.writestr('-', data.encode('ascii'))
        return output.getvalue()

    def _encode(self, data):
        # The character '>' must be at index 3*n to ensure that the
        # specific Base64 character for URL-safe encoding is actually
        # used in the flag.
        data = b'<file-contents>:' + data
        if self._urlsafe:
            encoded = base64.urlsafe_b64encode(data)
        else:
            encoded = base64.b64encode(data)
        flagstr = encoded.decode('ascii')
        linelen = 64
        wrapped = ' \n'.join([flagstr[linelen*i:linelen*(i+1)] for i in range(1+int(len(flagstr)/linelen))])
        return wrapped


__all__ = ['Flag']


if __name__ == '__main__':
    test_flag = str(Flag(False))
    print('\nThe flag in non-URL safe encoding:\n')
    print(test_flag)
    flag = str(Flag())
    print('\nThe complate flag:\n')
    print(flag)
    try:
        decoded = base64.b64decode(flag.encode('ascii'))
        print('\nFlag decoded with ordinary base64 alphabet:\n')
        print(decoded)
        print('\nFlag can be decoded with ordinary base64 alphabet.\n')
    except:
        decoded = base64.urlsafe_b64decode(flag.encode('ascii'))
        print('\nFlag decoded with URL-safe base64 alphabet:\n')
        print(decoded)
        print('\nUnable to decode flag with ordinary base64 alphabet.\n')
        raise

