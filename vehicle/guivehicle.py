
import vehicle
import bus
import car
import globalvars
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class GuiVehicle(QtGui.QWidget):

    def __init__(self, vehicle):
        super(GuiVehicle, self).__init__()
        self.vehicle = vehicle
        layout = QGridLayout(self)
        table = QTableWidget(len(vehicle.routing_table),3)
        table.setColumnWidth(0, 290)
        table.setHorizontalHeaderLabels ( ("Next hop", "Nb.", "TTL"))
        table.setColumnWidth(1, 40)
        table.setColumnWidth(2, 40)

        for i in xrange(len(vehicle.routing_table)):
            table.setCellWidget(i,0,QLabel(str(vehicle.routing_table[i][0].user_id)))
            table.setCellWidget(i,1,QLabel(str(vehicle.routing_table[i][1])))
            table.setCellWidget(i,2,QLabel(str(vehicle.routing_table[i][2])))

        index = QTableWidget(len(globalvars.file_table),3)
        self.dlButtonList = []
        self.progressList = [] 

        for file, value in globalvars.file_table.iteritems():
            j = len(self.dlButtonList)
            print file
            index.setCellWidget(j,0,QLabel(file))
            self.dlButtonList.append(QPushButton("Download", index))
            index.setCellWidget(j,1, self.dlButtonList[j])
            self.progressList.append(QProgressBar(index))
            index.setCellWidget(j,2, self.progressList[j])
        vehicleImg = QLabel()
        vehicleImg.setPixmap(vehicle.img.pixmap(QSize(36,36)))
        vehicleImg.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(vehicleImg, 1,0)
        layout.addWidget(QLabel(str(vehicle.user_id)), 1,1)
        layout.addWidget(table,2,0)
        layout.addWidget(index,2,1)
        self.setLayout(layout)
        self.initUI()

        
    def initUI(self):
        self.setGeometry(300, 100, 800, 400)
        self.setWindowTitle('Vehicule')
        self.show()
