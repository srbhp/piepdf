"""
This file implements metadata extraction function
"""

import logging
import re
import time

import feedparser
import popplerqt5
from habanero import Crossref
from PyQt6 import QtCore

# import httplib2 as http_client
# http_client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


class GetPdfInfo:
    """
    Extract metadata
    """

    def __init__(self, email=""):
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
        """
        Get Metadata
        """
        try:
            time.sleep(1)
            doiNo = self.getDoiFromPdf(filename)
            # check if it a arxiv article
            arxivNo = ""
            if len(doiNo) < 8:
                try:
                    arxivNo = self.parseArxiv(self.page0_text)
                except:
                    arxivNo = ""
            # If doi No found
            if len(doiNo) > 8 and len(arxivNo) < 8:
                print(doiNo)
                try:
                    self.getMetadataByDoi(doiNo)
                except Exception as e:
                    print(f"Error getting metadata by DOI: {e}")
            # If both arxiv and doi not found get metadata by text queryself.
            # 1/3 of of first page is send for text query.
            if len(doiNo) + len(arxivNo) < 8:
                try:
                    qrtext = self.page0_text[0:200] if self.page0_text else ""
                    if qrtext:
                        self.getMetadataByQuery(qrtext)
                except Exception as e:
                    print(f"Error getting metadata by query: {e}")
            return self.metadata
        except Exception as e:
            print(f"Error in getMetadata: {e}")
            return self.metadata

    def getDoiFromPdf(self, filename):
        try:
            doc = popplerqt5.Poppler.Document.load(filename)
            doi = ""
            if doc is not None:
                try:
                    doc.setRenderHint(popplerqt5.Poppler.Document.Antialiasing)
                    doc.setRenderHint(popplerqt5.Poppler.Document.TextAntialiasing)
                    doc.setRenderHint(popplerqt5.Poppler.Document.ThinLineShape)
                    doc.setRenderHint(popplerqt5.Poppler.Document.TextHinting)
                except:
                    pass

                try:
                    numpages = doc.numPages()
                    if numpages <= 0:
                        return ""

                    page0 = doc.page(0)
                    if page0 is None:
                        return ""

                    rect = page0.pageSize()
                    min = 0
                    try:
                        layout = page0.RawOrderLayout
                    except:
                        pass

                    self.page0_text = page0.text(
                        QtCore.QRectF(min, min, rect.width(), rect.height())
                    )
                    doi = re.findall(self.regString, self.page0_text)

                    # First page maye be not the Main page e.g.,IOP
                    if numpages >= 2 and len(doi) < 4:
                        page1 = doc.page(1)
                        if page1 is not None:
                            page1_text = page1.text(
                                QtCore.QRectF(min, min, rect.width(), rect.height())
                            )
                            doi = re.findall(self.regString, page1_text)
                    print("Doi:", doi)
                except Exception as e:
                    print(f"Error extracting text from PDF: {e}")
            return doi
        except Exception as e:
            print(f"Error loading PDF {filename}: {e}")
            return ""
        # check if it a arxiv article

    def getMetadataByDoi(self, doiNo):
        try:
            crdata = self.crossrefApi.works(ids=doiNo, format="bibentry")
            print(crdata)
            tm1 = crdata["message"]
            try:
                self.metadata["title"] = tm1["title"][0]
            except:
                pass
            try:
                self.metadata["doi"] = tm1["DOI"]
            except:
                pass
            try:
                self.metadata["volumn"] = tm1["volume"]
            except:
                pass
            try:
                self.metadata["author"] = " and ".join(
                    [i["given"] + " " + i["family"] for i in tm1["author"]]
                )
            except:
                pass
            try:
                self.metadata["journal"] = tm1["publisher"]
            except:
                pass
            try:
                self.metadata["url"] = "https://dx.doi.org/" + tm1["DOI"]
            except:
                pass
            try:
                self.metadata["year"] = tm1["created"]["date-parts"][0][0]
            except:
                pass
            try:
                self.metadata["page"] = tm1["page"]
            except:
                pass
        except:
            print("Failed ...... getMetadataDoi")
            pass

    def getMetadataByQuery(self, qr):
        print(qr)
        try:
            qrresult = self.crossrefApi.works(
                query=qr, limit=1, sort="relevance", format="bibentry"
            )
            tm1 = qrresult["message"]
            tm1 = tm1["items"][0]
            try:
                self.metadata["title"] = tm1["title"][0]
            except:
                pass
            try:
                self.metadata["doi"] = tm1["DOI"]
            except:
                pass
            try:
                self.metadata["volumn"] = tm1["volume"]
            except:
                pass
            try:
                self.metadata["author"] = " and ".join(
                    [i["given"] + " " + i["family"] for i in tm1["author"]]
                )
            except:
                pass
            try:
                self.metadata["journal"] = tm1["publisher"]
            except:
                pass
            try:
                self.metadata["url"] = "https://dx.doi.org/" + tm1["DOI"]
            except:
                pass
            try:
                self.metadata["page"] = tm1["page"]
            except:
                pass
            try:
                self.metadata["year"] = tm1["published-online"]["date-parts"][0][0]
            except:
                pass
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
            try:
                result = results["entries"][0]
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
