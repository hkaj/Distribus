#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import vehicle
import car
import bus
import movingarea

import threading 
import sys
import random
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint


def main():
    vehicleList = []
    app = QtGui.QApplication(sys.argv)
    
    for i in range(30):
            x = random.randint(25, 525)
            y = random.randint(25, 425)
        # the 20 first vehicles are cars
            if i < 20:
                vehicleList.append(car.Car(QPoint(x, y)))
        # the 10 left are bus
            else:
                vehicleList.append(bus.Bus(QPoint(x, y)))

    map = movingarea.MovingArea(vehicleList)

    a = threading.Thread(None, loop, "infinite loop", vehicleList, None) 
    a.start()   
    
    sys.exit(app.exec_())

def loop(vehicleList):
    while 1:
        for v in vehicleList:
            v.update(vehicleList)

if __name__ == '__main__':
    main()
