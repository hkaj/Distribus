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
	#app = QtGui.QApplication(sys.argv)
	#map = movingarea.MovingArea()
	#sys.exit(app.exec_())
    for i in range(30):
            x = random.randint(25, 525)
            y = random.randint(25, 425)
	    # the 20 first vehicles are cars
            if i < 20:
                vehicleList.append(car.Car(QPoint(x,y)))
	    # the 10 left are bus
            else:
                vehicleList.append(bus.Bus(QPoint(x,y)))
    for v in vehicleList:
        v.update(vehicleList)

def test_routing():
    vehicleList = [car.Car(QPoint(0, 0)), car.Car(QPoint(0, 99)), bus.Bus(QPoint(198, 0)), car.Car(QPoint(99, 0)), car.Car(QPoint(99, 99)), car.Car(QPoint(198, 99))]
    round = 0   
    while 1:
        print "============================================================="
        print "ROUND", round, "\n\n"
        round = round + 1
        for v in vehicleList:
            v.update(vehicleList)
        if round == 5:
            del vehicleList[2]
        sys.stdin.readline()

if __name__ == '__main__':
	test_routing()
    
