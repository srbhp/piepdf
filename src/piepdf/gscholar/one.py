#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import urllib.request
import urllib

try:
    url = "https://scholar.google.de/scholar?hl=de&as_sdt=0%2C5&"
    values = {
        "q": "Langevin approach to lattice dynamics in a charge-ordered polaronic system "
    }
    data = urllib.parse.urlencode(values)
    data = data.encode("utf-8")  # data should be bytes

    # now, with the below headers, we defined ourselves as a simpleton who is
    # still using internet explorer.
    headers = {}
    headers["User-Agent"] = (
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    )
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    respData = resp.read()

    saveFile = open("withHeaders.txt", "w")
    saveFile.write(str(respData))
    saveFile.close()
except Exception as e:
    print(str(e))
