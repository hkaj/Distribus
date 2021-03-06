#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from vehicle import Vehicle
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QSize
from PyQt4.QtGui import QImage, QIcon, QPushButton, QPixmap


class Car(Vehicle):
    """Represents a car."""
    def __init__(self, position):
        super(Car, self).__init__(position)  
        self.img = QIcon(QPixmap('media/car.png')) #quote this line if testing the NON gui version

