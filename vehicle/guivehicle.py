
import vehicle
import bus
import car
import globalvars
import threading
import time
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class GuiVehicle(QtGui.QWidget):

    def __init__(self, vehicle):
        super(GuiVehicle, self).__init__()
        self.vehicle = vehicle
        layout = QGridLayout(self)

        # routing table [Next hop, Jump nb to reach a bus, TTL]
        table = QTableWidget(len(vehicle.routing_table),3)
        table.setColumnWidth(0, 290)
        table.setHorizontalHeaderLabels ( ("Next hop", "Cost", "TTL"))
        table.setColumnWidth(1, 40)
        table.setColumnWidth(2, 40)

        # filling (gui) table
        for i in xrange(len(vehicle.routing_table)):
            table.setCellWidget(i,0,QLabel(str(vehicle.routing_table[i][0].user_id)))
            table.setCellWidget(i,1,QLabel(str(vehicle.routing_table[i][1])))
            table.setCellWidget(i,2,QLabel(str(vehicle.routing_table[i][2])))

        # index of files
        self.index = QTableWidget(len(globalvars.file_table),3)
        self.index.setHorizontalHeaderLabels ( ("File", "Dl", "Progress"))
        self.dlButtonList = []
        self.progressList = [] 

        # filling index table
        for file, value in globalvars.file_table.iteritems():
            j = len(self.dlButtonList)
            self.index.setCellWidget(j,0,QLabel(file))
            self.dlButtonList.append(QPushButton("Download", self.index))
            self.dlButtonList[j].clicked.connect(self.dlFile)
            self.dlButtonList[j].setCheckable(True)
            self.index.setCellWidget(j,1, self.dlButtonList[j])
            self.progressList.append(QProgressBar(self.index))
            if self.vehicle.file_table.has_key(file):
                self.progressList[j].setValue(100)
            self.index.setCellWidget(j,2, self.progressList[j])

        # draw icon of the selected vehicle
        vehicleImg = QLabel()
        vehicleImg.setPixmap(vehicle.img.pixmap(QSize(36,36)))
        vehicleImg.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(vehicleImg, 1,0)

        # write the id of the select vehicle
        layout.addWidget(QLabel(str(vehicle.user_id)), 1,1)
        layout.addWidget(table,2,0)
        layout.addWidget(self.index,2,1)
        self.setLayout(layout)
        self.initUI()

        
    def initUI(self):
        self.setGeometry(300, 100, 800, 400)
        self.setWindowTitle('Vehicule')
        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.refreshPercentage(qp)
        qp.end()

    def refreshPercentage(self, qp):
        for i in xrange(len(globalvars.file_table)):
            filename = str(self.index.cellWidget(i, 0).text())
            self.progressList[i].setValue(self.vehicle.get_percentage(filename))
        self.update()

    def dlFile(self):

        # finding the sender of the signal
        for i in range(len(self.dlButtonList)):
            if self.dlButtonList[i] == self.sender():
                ind = i
                break

        filename = str(self.index.cellWidget(ind, 0).text())
        # send the file request
        self.vehicle.require_file(filename)
        
