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
http_client.HTTPConnection.debuglevel = 1
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
    def  __init__(self,ifparent=None,email = ""):
        self.mailto = email
        self.arXivApi = "http://export.arxiv.org/api/query?id_list="

        self.crossrefApi = Crossref( mailto=self.mailto)
        self.metadata= {'doi':'', 'url':'', 'year':'',
            'journal':'', 'author':'', 'title':'','abstract':''}
    def getMetadata(self,filename ):
        time.sleep(1)
        self.filename=filename
        print (self.filename )
        self.doc = popplerqt5.Poppler.Document.load(self.filename)
        if  self.doc is not None :
            self.doc.setRenderHint(popplerqt5.Poppler.Document.Antialiasing)
            self.doc.setRenderHint(popplerqt5.Poppler.Document.TextAntialiasing)
            self.doc.setRenderHint(popplerqt5.Poppler.Document.ThinLineShape)
            self.doc.setRenderHint(popplerqt5.Poppler.Document.TextHinting)
            numpages=self.doc.numPages()

            rect = self.doc.page(0).pageSize ()

            min = 0
            layout=self.doc.page(0).PhysicalLayout
            page0_text = self.doc.page(0).text( QtCore.QRectF( min, min,
                rect.width(),rect.height()) )#.to_utf8()
            if numpages >= 2:
                page1_text = self.doc.page(1).text(  QtCore.QRectF( min, min,
                rect.width(),rect.height()) ,layout)
            # First page maye be not the Main page e.g.,IOP
            doiNo = self.parseDoi(page0_text)
            #check if it a arxiv article
            arxivNo=""
            if len(doiNo) < 8:
                arxivNo = self.parseArxiv(page0_text)
                #IF arxiv no found check the second page
                if len(arxivNo) < 8 and numpages >= 2:
                    doiNo = self.parseDoi(page1_text)

            if len(arxivNo) >8 :
                print(arxivNo)
            #If doi No found
            if len(doiNo) >  8  and len(arxivNo) <8:
                print(doiNo)
                self.getMetadataDoi(doiNo)

            #If both arxiv and doi not found get metadata by text queryself.
            #1/3 of of first page is send for text query.
            if len(doiNo)+ len(arxivNo) < 8 :
                qrtext = self.doc.page(0).text( QtCore.QRectF( min, min,
                    rect.width(),rect.height()/3) )
                self.getMetadataQuery(qrtext)
        return self.metadata
    def getMetadataDoi(self,doiNo):
        try :
            crdata = self.crossrefApi.works(ids = doiNo,  format="bibentry")
            tm1 = crdata['message']
            self.metadata['title'] = tm1['title'][0]
            self.metadata['doi'] = tm1['DOI']
            self.metadata['page'] = tm1['page']
            self.metadata['volumn'] = tm1['volume']
            self.metadata['author'] = " and ".join([i['given']+" " + i['family'] for i in tm1['author'] ])
            self.metadata['journal'] = tm1['publisher']
            self.metadata['url'] = "https://dx.doi.org/"+tm1['DOI']
            self.metadata['year']=tm1['published-online']['date-parts'][0][0]
        except:
            print("Failed ...... ")
    def getMetadataQuery(self,qr):
        print(qr )
        qrresult =  self.crossrefApi.works(query=qr,limit=1,sort="relevance",format="bibentry")
        try :
            tm1 = qrresult['message']
            tm1= tm1['items'][0]
            self.metadata['title'] = tm1['title'][0]
            self.metadata['doi'] = tm1['DOI']
            self.metadata['page'] = tm1['page']
            self.metadata['volumn'] = tm1['volume']
            self.metadata['author'] = " and ".join([i['given']+" " + i['family'] for i in tm1['author'] ])
            self.metadata['journal'] = tm1['publisher']
            self.metadata['url'] = "https://dx.doi.org/"+tm1['DOI']
            self.metadata['year']=tm1['published-online']['date-parts'][0][0]
        except :
            print("Failed " )
    def parseDoi(self,pageStr ):
        doi=""
        strAr= "doi:"
        pos1 = pageStr.find(strAr)
        if ( pos1 != -1 ):
            tm1 =  pageStr[pos1:pos1+40]
            tm1 = tm1.split()
            if ( len(tm1) >= 1 ):
                tm2 = tm1[0]
                doi = tm2[4: ]
        strUrl= "doi.org"
        pos1 = pageStr.find(strUrl)
        if ( pos1 != -1 and len(doi) < 8 ):
            tm1 =  pageStr[pos1:pos1+40]
            tm1 = tm1.split()
            if ( len(tm1[0]) > 8 ):
                    tm2 = tm1[0]
                    doi = tm2[8: ]

        strList = {"DOI","Doi","doi"}
        for str1  in strList:
            pos1 = pageStr.find(str1)
            if ( pos1 != -1 and len(doi) < 8):
                tm1 =  pageStr[pos1:pos1+100]
                tm1 = tm1.split()
                if ( len(tm1) >=3 and len(tm1[1]) > 8  ):
                    doi=tm1[1]
                    if(tm1[2][0].isdigit()):
                        doi = doi + r"_"+tm1[2]
                #Find in the next line incase there is two column layout
                else :
                    tm1 =  pageStr[pos1:pos1+250]
                    tm1 = tm1.split()
                    for i in tm1:
                        if(i[0].isdigit()):
                            doi = i

        #Find doi from url
        return doi

    def parseArxiv(self,pageStr ):
        arNo=""
        strAr= "arXiv"
        pos1 = pageStr.find(strAr)
        if ( pos1 != -1 ):
            tm1 =  pageStr[pos1:pos1+100]
            tm1 = tm1.split()
            arNo = tm1[0][6:-2]
            results = feedparser.parse(self.arXivApi+arNo )
            result  = results['entries'][0]
            try:
                self.metadata['title'] = result['title'].replace("\n"," ")
                self.metadata['author'] = " and ".join( [i['name'] for i  in
                    result['authors']])
                self.metadata['abstract'] = result['summary'].replace("\n"," ")
                self.metadata['url'] = 'https://arxiv.org/abs/'+arNo
                self.metadata['doi'] = result['arxiv_doi']
            except :
                print("Failed " )
        return arNo
