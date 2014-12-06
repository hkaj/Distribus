#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import uuid, math, sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint
from PyQt4.QtGui import QImage
from copy import deepcopy

class Vehicle(object):
    """Base class for both cars and buses."""

    def __init__(self, position):
        """set up globals"""
        self.user_id = uuid.uuid4()
        self.MAXTTL = 2
        self.timeout = 2
        self.routing_table = [] # list of list(node, cost, ttl)
        self.file_table = []
        self.position = position
        self.isBus = False

    def update(self, vehicleList):
        """called every clock tick in the system for each car."""
        print self.routing_table
        self.broadcast(vehicleList)
        if not self.isBus:
            for route in self.routing_table:
                route[2] -= 1
                if route[2] == 0:
                    self.routing_table.remove(route)

    def send_route_update_message(self, dest, self_routing_table):
        dest.receive_route_update_message(self, self_routing_table)

    def receive_route_update_message(self, sender, sender_routing_table):
        if not self.isBus:
            self.merge_routing_tables(sender)

    def is_vehicle_reachable(self, other):
        xDiff = self.position.x() - other.position.x()
        yDiff = self.position.y() - other.position.y()
        dist = math.sqrt( math.pow(xDiff, 2) + math.pow(yDiff, 2))                     
        if dist < 100:
            return True
        else:
            return False

    def broadcast(self, vehicleList):
        for vehicle in vehicleList:
            if vehicle == self:
                continue
            else:    
                if self.is_vehicle_reachable(vehicle):
                    self.send_route_update_message(vehicle, self.routing_table)

    def merge_routing_tables(self, sender):
        shortest_route = None
        for remote_route in sender.routing_table:
            if not shortest_route or remote_route[1] < shortest_route[1]:
                shortest_route = remote_route
        if shortest_route and shortest_route[0].user_id != self.user_id:
            updated = False
            for local_route in self.routing_table:
                if local_route[0].user_id == sender.user_id:
                    local_route[1] = shortest_route[1] + 1
                    local_route[2] = self.MAXTTL
                    updated = True
            if not updated:
                self.routing_table.append([sender, shortest_route[1] + 1, self.MAXTTL])
