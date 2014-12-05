import bus
import car
import vehicle

import sys, random, math, time
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QSize, SIGNAL, SLOT
from PyQt4.QtGui import QImage, QIcon, QPushButton

class MovingArea(QtGui.QWidget):

    def __init__(self):
        super(MovingArea, self).__init__()
        self.vehicleList = []
        self.vehicleImg = []
        self.size
        self.initUI()
        self.initVehicleNodes()    
        self.show()

        
    def initUI(self):    
        self.setGeometry(100, 100, 550, 450)
        self.size = self.size()
        self.setWindowTitle('Distribus')

    def initVehicleNodes(self):
    #instantiate vehicles at various random spots
        for i in xrange(30):
            x = random.randint(25, self.size.width()-25)
            y = random.randint(25, self.size.height()-25)
        # the 20 first vehicles are cars
            if i < 20:
                self.vehicleList.append(car.Car(QPoint(x,y)))
        # the 10 left are bus
            else:
                self.vehicleList.append(bus.Bus(QPoint(x,y)))
            
            self.vehicleImg.append(QPushButton(self))
            self.vehicleImg[i].setIcon(self.vehicleList[i].img)
            #self.vehicleImg[i].setIconSize(QSize(32,32))

        for j in range(30):
            self.vehicleImg[j].setCheckable(True)
            self.vehicleImg[j].clicked.connect(self.handleButton)
            self.vehicleImg[j].move(self.vehicleList[j].position.x(), self.vehicleList[j].position.y())


    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawNetwork(qp)
        qp.end()

    def drawNetwork(self, qp):
    #for each vehicle
        for j in range(30):
        #we check others vehicles
            for k in range(30):
        #if we are testing the current vehicle
                if j == k:

                    continue
        #if we are testing an other vehicle
                else:
                    #calculating the distance between the 2 vehicles
                    xDiff = self.vehicleList[k].position.x() - self.vehicleList[j].position.x()
                    yDiff = self.vehicleList[k].position.y() - self.vehicleList[j].position.y()
                    dist = math.sqrt( math.pow(xDiff, 2) + math.pow(yDiff, 2))                     
                        
                    #if the distance is under 70
                    if dist < 70:
                    #creating a connection between the 2 vehicles
                        qp.drawLine(self.vehicleList[j].position.x(), self.vehicleList[j].position.y(), self.vehicleList[k].position.x(), self.vehicleList[k].position.y())
                
            #creating a random movement
            isPosX = bool(random.getrandbits(1))
            isPosY = bool(random.getrandbits(1))
            if isPosX == True:
                if self.vehicleList[j].position.x() != self.size.width() - 25:
                    self.vehicleList[j].position.setX(self.vehicleList[j].position.x() + 1)
            else:
                if self.vehicleList[j].position.x() != 25:
                    self.vehicleList[j].position.setX(self.vehicleList[j].position.x() - 1)

            if isPosY == True:
                if self.vehicleList[j].position.y() != self.size.height() - 25:
                    self.vehicleList[j].position.setY(self.vehicleList[j].position.y() + 1) 
            else:
                if self.vehicleList[j].position.y() != 25:
                    self.vehicleList[j].position.setY(self.vehicleList[j].position.y() - 1)

            
            pos = QPoint(self.vehicleList[j].position.x() - (self.vehicleImg[j].size().width()/2), self.vehicleList[j].position.y() - (self.vehicleImg[j].size().height()/2))
            self.vehicleImg[j].move(pos.x(), pos.y())
            #self.vehicleList[j].img.move(pos.x(), pos.y())
            #qp.drawImage(pos, self.vehicleList[j].img)
            
        time.sleep(0.001)
        #calling paintEvent 
        self.update()

    def handleButton(self):
        print 'lol'