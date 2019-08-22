import popplerqt5
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import re
import feedparser
from habanero import Crossref
import time

import requests
import logging
import httplib2 as http_client

# http_client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

import requests
import logging

logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


class GetPdfInfo(object):
    def __init__(self, ifparent=None, email=""):
        self.mailto = email
        self.arXivApi = "http://export.arxiv.org/api/query?id_list="

        self.crossrefApi = Crossref(mailto=self.mailto)
        self.regString = r"\b(10\.[0-9]{4,}(?:\.[0-9]+)*\/(?:(?![\"&\'])\S)+)\b"
        self.metadata = {
            "doi": "",
            "url": "",
            "year": "",
            "journal": "",
            "author": "",
            "title": "",
            "abstract": "",
        }
        self.page0_text = ""

    def getMetadata(self, filename):
        time.sleep(1)
        doiNo = self.getDoiFromPdf(filename)
        # check if it a arxiv article
        arxivNo = ""
        if len(doiNo) < 8:
            arxivNo = self.parseArxiv(self.page0_text)
            # IF arxiv no found check the second page

        # If doi No found
        if len(doiNo) > 8 and len(arxivNo) < 8:
            print(doiNo)
            self.getMetadataByDoi(doiNo)
        # If both arxiv and doi not found get metadata by text queryself.
        # 1/3 of of first page is send for text query.
        if len(doiNo) + len(arxivNo) < 8:
            qrtext = self.page0_text[0:200]
            self.getMetadataByQuery(qrtext)
        return self.metadata

    def getDoiFromPdf(self, filename):
        doc = popplerqt5.Poppler.Document.load(filename)
        if doc is not None:
            doc.setRenderHint(popplerqt5.Poppler.Document.Antialiasing)
            doc.setRenderHint(popplerqt5.Poppler.Document.TextAntialiasing)
            doc.setRenderHint(popplerqt5.Poppler.Document.ThinLineShape)
            doc.setRenderHint(popplerqt5.Poppler.Document.TextHinting)
            numpages = doc.numPages()

            rect = doc.page(0).pageSize()
            min = 0
            layout = doc.page(0).RawOrderLayout
            # layout=doc.page(0).PhysicalLayout
            self.page0_text = doc.page(0).text(
                QtCore.QRectF(min, min, rect.width(), rect.height())
            )  # .to_utf8()
            doi = re.findall(self.regString, self.page0_text)
            # First page maye be not the Main page e.g.,IOP
            if numpages >= 2 and len(doi) < 4:
                page1_text = doc.page(1).text(
                    QtCore.QRectF(min, min, rect.width(), rect.height())
                )
                doi = re.findall(self.regString, page1_text)
            print("Doi:", doi)
        return doi
        # check if it a arxiv article

    def getMetadataByDoi(self, doiNo):
        try:
            crdata = self.crossrefApi.works(ids=doiNo, format="bibentry")
            print(crdata)
            tm1 = crdata["message"]
            self.metadata["title"] = tm1["title"][0]
            self.metadata["doi"] = tm1["DOI"]
            self.metadata["volumn"] = tm1["volume"]
            self.metadata["author"] = " and ".join(
                [i["given"] + " " + i["family"] for i in tm1["author"]]
            )
            self.metadata["journal"] = tm1["publisher"]
            self.metadata["url"] = "https://dx.doi.org/" + tm1["DOI"]
            self.metadata["year"] = tm1["created"]["date-parts"][0][0]
            self.metadata["page"] = tm1["page"]
        except:
            print("Failed ...... getMetadataDoi")
            pass

    def getMetadataByQuery(self, qr):
        print(qr)
        qrresult = self.crossrefApi.works(
            query=qr, limit=1, sort="relevance", format="bibentry"
        )
        try:
            tm1 = qrresult["message"]
            tm1 = tm1["items"][0]
            self.metadata["title"] = tm1["title"][0]
            self.metadata["doi"] = tm1["DOI"]
            self.metadata["volumn"] = tm1["volume"]
            self.metadata["author"] = " and ".join(
                [i["given"] + " " + i["family"] for i in tm1["author"]]
            )
            self.metadata["journal"] = tm1["publisher"]
            self.metadata["url"] = "https://dx.doi.org/" + tm1["DOI"]
            self.metadata["page"] = tm1["page"]
            self.metadata["year"] = tm1["published-online"]["date-parts"][0][0]
        except:
            print("Failed ")
            pass

    def parseDoi(self, pageStr):
        doi = re.findall(self.regString, pageStr)
        return doi

    def parseArxiv(self, pageStr):
        arNo = ""
        strAr = "arXiv"
        pos1 = pageStr.find(strAr)
        if pos1 != -1:
            tm1 = pageStr[pos1 : pos1 + 100]
            tm1 = tm1.split()
            arNo = tm1[0][6:-2]
            results = feedparser.parse(self.arXivApi + arNo)
            result = results["entries"][0]
            try:
                self.metadata["title"] = result["title"].replace("\n", " ")
                self.metadata["author"] = " and ".join(
                    [i["name"] for i in result["authors"]]
                )
                self.metadata["abstract"] = result["summary"].replace("\n", " ")
                self.metadata["url"] = "https://arxiv.org/abs/" + arNo
                self.metadata["doi"] = result["arxiv_doi"]
            except:
                print("Failed to get metadata from arxiv  ")
                pass
        return arNo
