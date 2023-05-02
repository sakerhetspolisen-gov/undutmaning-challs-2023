from .flag import Flag
import uuid
import random
import time


def get_entries(nxtix, do_reset, count, include_flag, response):
    if include_flag:
        do_reset = True
        count = 1
    else:
        try:
            count = int(count)
            count = max(count, 1)
            count = min(count, 50)
        except:
            count = 10
    if do_reset:
        start = 1
    else:
        try:
            start = int(nxtix)
            start = max(start, 1)
        except:
            start = 1
    nxtix = start + count
    if response:
        response.set_cookie(key='nxtix', value=nxtix)
    if not include_flag:
        data = [{'index':i, 'contents': uuid.uuid4().hex} for i in range(start, nxtix)]
        if len(data):
            max_index = len(data) - 1
            base = min(3, max_index)
            max_offset = max_index - base
            offset = random.randint(0, max_offset)
            data[base + offset]['contents'] = 'q3e8!checkthejavascriptfile!7d7q'
        if start > 1:
            time.sleep(3)
    else:
        data = [{'index':'Flag', 'contents':'base64 urlsafe: %s' % str(Flag())}]
    return data


__all__ = ['get_entries']


if __name__ == '__main__':
    import pprint
    pprint.pprint(get_entries(0, False, 20, False, None))

