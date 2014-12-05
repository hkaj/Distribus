#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import vehicle
import car
import bus
import movingarea

import sys, random
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint

def main():

    vehicleList = []
    app = QtGui.QApplication(sys.argv)
    map = movingarea.MovingArea()
    sys.exit(app.exec_())
'''    for i in range(30):
            x = random.randint(25, 525)
            y = random.randint(25, 425)
        # the 20 first vehicles are cars
            if i < 20:
                vehicleList.append(car.Car(QPoint(x,y)))
        # the 10 left are bus
            else:
                vehicleList.append(bus.Bus(QPoint(x,y)))

    for v in vehicleList:
        v.update(vehicleList)'''


if __name__ == '__main__':
    main()
