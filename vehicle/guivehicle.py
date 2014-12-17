
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
        layout.setColumnMinimumWidth(0,400)

        # routing table [Next hop, Jump nb to reach a bus, TTL]
        self.table = QTableWidget(len(vehicle.routing_table),3)
        self.table.setColumnWidth(0, 290)
        self.table.setHorizontalHeaderLabels ( ("Next hop", "Cost", "TTL"))
        self.table.setColumnWidth(1, 40)
        self.table.setColumnWidth(2, 40)

        # filling (gui) table
        for i in xrange(len(vehicle.routing_table)):
            self.table.setCellWidget(i,0,QLabel(str(vehicle.routing_table[i][0].user_id)))
            self.table.setCellWidget(i,1,QLabel(str(vehicle.routing_table[i][1])))
            self.table.setCellWidget(i,2,QLabel(str(vehicle.routing_table[i][2])))

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
            if self.vehicle.isBus:
                self.dlButtonList[j].setEnabled(False)
            else:
                self.dlButtonList[j].setEnabled(True)       
            self.index.setCellWidget(j,1, self.dlButtonList[j])
            self.progressList.append(QProgressBar(self.index))
            if self.vehicle.file_table.has_key(file) or self.vehicle.isBus:
                self.progressList[j].setValue(100)
            self.index.setCellWidget(j,2, self.progressList[j])

        # draw icon of the selected vehicle
        vehicleImg = QLabel()
        vehicleImg.setPixmap(vehicle.img.pixmap(QSize(36,36)))
        vehicleImg.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(vehicleImg, 1,0)

        # write the id of the select vehicle
        layout.addWidget(QLabel(str(vehicle.user_id)), 1,1)
        layout.addWidget(self.table,2,0)
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
        self.refreshView(qp)
        qp.end()

    def refreshView(self, qp):

        self.table.setRowCount(0)

        rout_tab_len = len(self.vehicle.routing_table)
        self.table.setRowCount(rout_tab_len)
        try:
            for i in range(rout_tab_len):
                self.table.setCellWidget(i,0,QLabel(str(self.vehicle.routing_table[i][0].user_id)))
                self.table.setCellWidget(i,1,QLabel(str(self.vehicle.routing_table[i][1])))
                self.table.setCellWidget(i,2,QLabel(str(self.vehicle.routing_table[i][2])))
        except IndexError:
            pass



        for j in range(len(globalvars.file_table)):
            filename = str(self.index.cellWidget(j, 0).text())
            if not self.vehicle.isBus:
                self.progressList[j].setValue(self.vehicle.get_percentage(filename))
        time.sleep(0.001)
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
        
