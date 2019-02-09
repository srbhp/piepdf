# PiePdf

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/35a5a955bd8a42d196129f5c9d975329)](https://app.codacy.com/app/pradhanphy/PiePdf?utm_source=github.com&utm_medium=referral&utm_content=srbhp/PiePdf&utm_campaign=Badge_Grade_Dashboard)

Manage Research Articles  and fetch metadata from the internet(currently crossref and arXiv is supported). 

Attempt to  make a opensource an alternative to Mendeley, Zotero.

![demonstration pic](https://github.com/srbhp/PiePdf/raw/master/Screenshot.png)
# Dependencies : 
python3-poppler-qt5, PyQt5 for python3, python3-feedparser, habanero

`pip3 install habanero PyQt5 python-poppler-qt5 feedparser`

# Instalation :
```
git clone https://github.com/srbhp/PiePdf.git
cd PiePdf
python3 mainwindow.py
```
By default it will create a folder `PiePdf`
 in your home directory. You can change this default directory to any `Path` from the settiing menu.
 You have keep all your pdfs in this directory. *PiePdf* will fetch metadata autometically 
 from crossref or arXiv for each pdf.

## You should know 
*PiePdf* configuration file is `~/.config/piepdf/piepdf.conf`

*PiePdf* database file is `~/.config/piepdf/piepdf_database/piepdf.db`

credit: Icons : http://openclipart.org/
