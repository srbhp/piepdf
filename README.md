# PiePdf

Manage Research Articles  and fetch metadata from the internet (currently crossref and arXiv is supported). 

Trying to  make an opensource alternative to Mendeley, Zotero.

<!-- ![demonstration pic](https://github.com/srbhp/PiePdf/raw/master/Screenshot.webm) -->
![demonstration pic](https://github.com/srbhp/PiePdf/raw/master/Screencast.mp4)
## Dependencies 
python3-poppler-qt5, PyQt5 for python3, python3-feedparser, habanero

### Fedora

`pip3 install habanero PyQt5 python-poppler-qt5 feedparser` and `dnf install python3-httplib2`


### Openseuse

```
pip3 install habanero 
zypper in python3-poppler-qt5 python3-feedparser python3-qt5 python3-httplib2
```

## Installation 
```
git clone https://github.com/srbhp/PiePdf.git
cd PiePdf
python3 piepdf/mainwindow.py
```
By default it create a folder `PiePdf`
 in your home directory. You can change this default directory to any `Path` from the setiing menu.
 You have keep all your pdfs in this directory. *PiePdf* fetch metadata automatically 
 from crossref or arXiv for each pdf.

## You should know 
*PiePdf* configuration file  `~/.config/piepdf/piepdf.conf`

*PiePdf* database file  `~/.config/piepdf/piepdf_database/piepdf.db`


## TODO

- [ ] Add support for custom metadata providers 
- [ ] Fix Pdf reader performance 
- [ ] Fix info widget (title, tags, open URL)
- [ ] Fix tab title 
- [ ] Add icon to reload/sync folder
