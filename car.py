#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from vehicle import Vehicle
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint
from PyQt4.QtGui import QImage


class Car(Vehicle):
    """Represents a car."""
    def __init__(self, position):
        super(Car, self).__init__(position)
        self.img = QImage('./car.png')
