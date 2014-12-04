#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from vehicle import Vehicle
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint
from PyQt4.QtGui import QImage

class Bus(Vehicle):
    """Represents a bus."""
    def __init__(self, position):
        super(Bus, self).__init__(position)
        self.isBus = True
        self.routing_table = [[self, 0, 3]]
        self.img = QImage('./bus.png')
