#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from vehicle import Vehicle
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QSize
from PyQt4.QtGui import QImage, QIcon, QPushButton


class Car(Vehicle):
    """Represents a car."""
    def __init__(self, position):
        super(Car, self).__init__(position)  
        self.img = QIcon('./car.png')
        #self.img.size = QSize(32,32)
