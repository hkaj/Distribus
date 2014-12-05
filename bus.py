#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from vehicle import Vehicle
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QSize
from PyQt4.QtGui import QImage, QIcon, QPushButton

class Bus(Vehicle):
    """Represents a bus."""
    def __init__(self, position):
        super(Bus, self).__init__(position)
        self.isBus = True
        self.routing_table = [[self, 0, 3]]
        self.img = QIcon('./bus.png')  #QPushButton()
        self.img.size = QSize(32,32)  #QPushButton()

        #self.img.setIcon( QIcon('./bus.png')) 

