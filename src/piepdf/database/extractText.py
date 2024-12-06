#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import popplerqt5
import re
from PyQt5 import QtCore, QtGui, QtWidgets

def getDoiFromPdf(filename ):
    print (filename )
    doc = popplerqt5.Poppler.Document.load(filename)
    if  doc is not None :
        doc.setRenderHint(popplerqt5.Poppler.Document.Antialiasing)
        doc.setRenderHint(popplerqt5.Poppler.Document.TextAntialiasing)
        doc.setRenderHint(popplerqt5.Poppler.Document.ThinLineShape)
        doc.setRenderHint(popplerqt5.Poppler.Document.TextHinting)
        numpages=doc.numPages()

        rect = doc.page(0).pageSize()
        print(rect.height() ,rect.width())
        min = 0
        layout=doc.page(0).RawOrderLayout
        #layout=doc.page(0).PhysicalLayout
        page0_text = doc.page(0).text(  QtCore.QRectF( min, min,
            rect.width(),rect.height()) ,)#.to_utf8()
        regString =  r"\b(10\.[0-9]{4,}(?:\.[0-9]+)*\/(?:(?![\"&\'])\S)+)\b"
        doi = re.search(regString ,page0_text ).group()
        print(doi )
        if numpages >= 2 and len(doi) < 4:
            page1_text = doc.page(1).text(  QtCore.QRectF( min, min,
            rect.width(),rect.height()) , )
            doi = re.search(regString ,page1_text ).group()
 
        # First page maye be not the Main page e.g.,IOP
        #check if it a arxiv article
if __name__ == "__main__":
    getDoiFromPdf("sample.pdf")
