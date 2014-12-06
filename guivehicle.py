import vehicle
import bus
import car
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class GuiVehicle(QtGui.QWidget):
    
    def __init__(self, vehicle):
        super(GuiVehicle, self).__init__()
        layout = QVBoxLayout(self)
        self.vehicle = vehicle
        layout.addWidget(QLabel(str(vehicle.user_id)))#QLabel(QString(vehicle.user_id)))
        for r in vehicle.routing_table:
            #print r
            string = str(r[0])+" "+str(r[1])+" "+str(r[2])
            layout.addWidget(QLabel(string))
            layout.addWidget(QLabel(string))
            layout.addWidget(QLabel(string))
        self.initUI()

        
    def initUI(self):    
        self.setGeometry(300, 100, 200, 50+(30*3))#len(self.vehicle.routing_table)))
        self.setWindowTitle('Vehicule')
        self.show()