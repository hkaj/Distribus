Distribus
=========

Distribus allows to share data over a highly dynamic network.

## Installing PyQT

For the GUI, we use PyQT, to download and use it, just follow the link: http://pyqt.sourceforge.net/Docs/PyQt4/installation.html
Basically (on a Linux environment), the steps are:
- Downloading SIP
- Extracting SIP
- cd to the new extracted SIP directory
- "python configure.py" (assuming python in the PATH)
- "make"
- "make install"
- Downloading PyQt
- Extracting PyQt
- cd to the new extracted PyQt directory
- "python configure.py" You may need to add the path to qmake-qt4 (usually adding "-q usr/bin/qmake-qt4")
- "make"
- "make install"
