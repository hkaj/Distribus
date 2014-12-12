#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import math
import random
import sys
import time

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QSize, SIGNAL, SLOT
from PyQt4.QtGui import QImage, QIcon, QPushButton

from vehicle import bus, car, guivehicle, vehicle


class MovingArea(QtGui.QWidget):
    def __init__(self, vehicleList):
        super(MovingArea, self).__init__()
        self.vehicleList = vehicleList
        self.vehicleImg = []
        self.size
        self.initVehicleNodes()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 550, 450)
        self.size = self.size()
        self.setWindowTitle('Distribus')
        self.show()

    def initVehicleNodes(self):
        for j in range(len(self.vehicleList)):
            self.vehicleImg.append(QPushButton(self))
            self.vehicleImg[j].setIcon(self.vehicleList[j].img)
            self.vehicleImg[j].setCheckable(True)
            self.vehicleImg[j].clicked.connect(self.handleButton)
            self.vehicleImg[j].setStyleSheet("QPushButton \
            {  background: rgba(255, 255, 255, 0);\
                border:none;\
                width:36px;\
                height:36px}")
            self.vehicleImg[j].move(self.vehicleList[j].position.x(), self.vehicleList[j].position.y())

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawNetwork(qp)
        qp.end()

    def drawNetwork(self, qp):
        # for each vehicle
        for j in range(30):
            # we check others vehicles
            for k in range(30):
                # if we are testing the current vehicle
                if j == k:
                    continue
                # if we are testing an other vehicle
                else:
                    # calculating the distance between the 2 vehicles
                    xDiff = self.vehicleList[k].position.x() - self.vehicleList[j].position.x()
                    yDiff = self.vehicleList[k].position.y() - self.vehicleList[j].position.y()
                    dist = math.sqrt(math.pow(xDiff, 2) + math.pow(yDiff, 2))
                    if dist < 70:
                        # creating a connection between the 2 vehicles
                        qp.drawLine(
                            self.vehicleList[j].position.x(),
                            self.vehicleList[j].position.y(),
                            self.vehicleList[k].position.x(),
                            self.vehicleList[k].position.y()
                        )

            # creating a random movement
            isPosX = bool(random.getrandbits(1))
            isPosY = bool(random.getrandbits(1))
            if isPosX:
                if self.vehicleList[j].position.x() != self.size.width() - 25:
                    self.vehicleList[j].position.setX(self.vehicleList[j].position.x() + 1)
            else:
                if self.vehicleList[j].position.x() != 25:
                    self.vehicleList[j].position.setX(self.vehicleList[j].position.x() - 1)

            if isPosY:
                if self.vehicleList[j].position.y() != self.size.height() - 25:
                    self.vehicleList[j].position.setY(self.vehicleList[j].position.y() + 1)
            else:
                if self.vehicleList[j].position.y() != 25:
                    self.vehicleList[j].position.setY(self.vehicleList[j].position.y() - 1)

            pos = QPoint(self.vehicleList[j].position.x() - (self.vehicleImg[j].size().width()/2),
                         self.vehicleList[j].position.y() - (self.vehicleImg[j].size().height()/2))
            self.vehicleImg[j].move(pos.x(), pos.y())

        time.sleep(0.001)
        # calling paintEvent
        self.update()

    def handleButton(self):
        # we search the object from the selected icon
        for i in range(len(self.vehicleImg)):
            if self.vehicleImg[i] == self.sender():
                index = i
                break

        global newguivehicle
        newguivehicle = guivehicle.GuiVehicle(self.vehicleList[index])
