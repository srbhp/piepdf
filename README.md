# PiePdf

Manage Research Articles  and fetch metadata from the internet(currently crossref and arXiv is supported). 

Attempt to  make a opensource an alternative to Mendeley, Zotero.

![demonstration pic](https://github.com/srbhp/PiePdf/raw/master/Screenshot.png)
## Dependencies 
python3-poppler-qt5, PyQt5 for python3, python3-feedparser, habanero

### fedora

`pip3 install habanero PyQt5 python-poppler-qt5 feedparser`

### openseuse

```
pip3 install habanero 
zypper in python3-poppler-qt5 python3-feedparser python3-qt5
```

## Instalation 
```
git clone https://github.com/srbhp/PiePdf.git
cd PiePdf
python3 piepdf/mainwindow.py
```
By default it will create a folder `PiePdf`
 in your home directory. You can change this default directory to any `Path` from the settiing menu.
 You have keep all your pdfs in this directory. *PiePdf* will fetch metadata autometically 
 from crossref or arXiv for each pdf.

## You should know 
*PiePdf* configuration file is `~/.config/piepdf/piepdf.conf`

*PiePdf* database file is `~/.config/piepdf/piepdf_database/piepdf.db`

credit: Icons :( http://openclipart.org/ )
