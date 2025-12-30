#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import re

import popplerqt5
from PyQt5 import QtCore


def getDoiFromPdf(filename):
    print(filename)
    try:
        doc = popplerqt5.Poppler.Document.load(filename)
        if doc is None:
            print(f"Error: Failed to load PDF {filename}")
            return ""

        doc.setRenderHint(popplerqt5.Poppler.Document.Antialiasing)
        doc.setRenderHint(popplerqt5.Poppler.Document.TextAntialiasing)
        doc.setRenderHint(popplerqt5.Poppler.Document.ThinLineShape)
        doc.setRenderHint(popplerqt5.Poppler.Document.TextHinting)
        numpages = doc.numPages()

        rect = doc.page(0).pageSize()
        print(rect.height(), rect.width())
        min = 0
        try:
            layout = doc.page(0).RawOrderLayout
        except:
            layout = None

        page0_text = doc.page(0).text(
            QtCore.QRectF(min, min, rect.width(), rect.height())
        )
        regString = r"\b(10\.[0-9]{4,}(?:\.[0-9]+)*\/(?:(?![\"&\'])\S)+)\b"

        doi_match = re.search(regString, page0_text)
        doi = doi_match.group() if doi_match else ""

        print(doi)

        if numpages >= 2 and len(doi) < 4:
            page1_text = doc.page(1).text(
                QtCore.QRectF(min, min, rect.width(), rect.height())
            )
            doi_match = re.search(regString, page1_text)
            doi = doi_match.group() if doi_match else ""

        return doi
    except Exception as e:
        print(f"Error extracting DOI from {filename}: {e}")
        return ""


if __name__ == "__main__":
    getDoiFromPdf("sample.pdf")
