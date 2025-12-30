#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4


import urllib2
from bs4 import BeautifulSoup


hdr = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
    "Accept-Encoding": "none",
    "Accept-Language": "en-US,en;q=0.8",
    "Connection": "keep-alive",
}

# The request with the headers
req = urllib2.Request(url, headers=hdr)

# The request with the headers
req = urllib2.Request(url, headers=hdr)

# Get the text from the urllib request
html = urllib2.urlopen(req)
text = html.read()

# Parse the text as html
soup = BeautifulSoup(text, "html.parser")

# Get the divs for all the article titles
mydivs = soup.findAll("div", {"class": "phYMDf nDgy9d"})
