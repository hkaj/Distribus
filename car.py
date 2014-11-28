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

    def receive_route_update(self, msg):
        self.merge_routes(msg['routes'])

    def merge_routes(self, routes):
        for route in routes:
            if route[0] in self.routing_table.keys():
                self.routing_table[route[0]][0] = self.MAXTTL
            else:
                self.routing_table[route[0]] = route[1]
                # sort the routing table according to the cost of each route
                sorted(self.routing_table, key=lambda route: route[1][1])
