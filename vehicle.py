#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import uuid
import math
import sys
from copy import deepcopy

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint
from PyQt4.QtGui import QImage

import globalvars

class Vehicle(object):
    """Base class for both cars and buses."""

    def __init__(self, position):
        self.user_id = uuid.uuid4()
        self.routing_table = [] #array of arrays [next_hop, number_hops_to_bus, ttl]
        self.file_table = []
        self.position = position
        self.isBus = False

    def update(self, vehicleList):
        """called every clock tick in the system for each vehicle."""
        print '\nRouting table of vehicle at:', self.position
        print self.routing_table
        #update neighbours' routing table
        self.broadcast(vehicleList)
        #decrease TTL of the route
        if not self.isBus:
            for route in self.routing_table:
                route[2] -= 1
                if route[2] == 0:
                    self.routing_table.remove(route)

    def send_route_update_message(self, dest, self_routing_table):
        """sends local routing table to neighbours"""
        #if the cost is "infinte" (=5) we consider the route down
        #this removes loops in the network after a certain amount
        #of time
        for route in self.routing_table:
            if route[1] > 5:
                self.routing_table.remove(route)
        dest.receive_route_update_message(self, self_routing_table)

    def receive_route_update_message(self, sender, sender_routing_table):
        #buses don't need to update their table
        if not self.isBus:
            self.merge_routing_tables(sender)

    def is_vehicle_reachable(self, other):
        xDiff = self.position.x() - other.position.x()
        yDiff = self.position.y() - other.position.y()
        dist = math.sqrt(math.pow(xDiff, 2) + math.pow(yDiff, 2))
        if dist < globalvars.msg_distance:
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
        """updates local routing table from information in the sender's routing table"""
        shortest_route = sender.get_shortest_route()
        #sender has some route to share and the route doesn't crosses us
        if shortest_route and shortest_route[0].user_id != self.user_id:
            updated = False
            #update the local route if exists
            for local_route in self.routing_table:
                if local_route[0].user_id == sender.user_id:
                    local_route[1] = shortest_route[1] + 1
                    local_route[2] = globalvars.max_ttl
                    updated = True
            #or add it if necessary
            if not updated:
                self.routing_table.append([sender, shortest_route[1] + 1, globalvars.max_ttl])

    def get_shortest_route(self):
        """get shortest route to a bus in the routing table"""
        shortest_route = None
        for route in self.routing_table:
            if not shortest_route or shortest_route[1] > route[1]:
                shortest_route = route
        return shortest_route
