#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import uuid, math
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint
from PyQt4.QtGui import QImage

class Vehicle(object):
    """Base class for both cars and buses."""

    def __init__(self, position):
        """set up globaals"""
        self.user_id = uuid.uuid4()
        self.MAXTTL = 3
        timeout = 2
        self.routing_table = list(list()) # list of list(node, cost, ttl)
        file_table = []
        self.position = position

    def update(self, vehicleList):
        """called every clock tick in the system for each car."""
        if hasattr(self, 'isBus') == False:
            self.broadcast(vehicleList)
            for route in self.routing_table:
                route[2] -= 1
                if route[2] == 0:
                    self.routing_table.remove(route)

    def send_route_update_message(self, dest, self_routing_table):
        dest.receive_route_update_message(self, self_routing_table)
 

    def receive_route_update_message(self, sender, sender_routing_table):
        
        sender.routing_table = merge_routing_tables(sender_routing_table, self, self.routing_table)
        print 'sender:  ',sender,' tr: ',sender.routing_table,'\n'


    


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

def merge_routing_tables(sender_routing_table, self_vehicle, self_routing_table):
    #don't delete duplicated entries yet
     
    for route in self_routing_table:
        route[0] = self_vehicle
        route[1] += 1
        route[2] = 3

    if sender_routing_table:
        mergedList = self_routing_table + sender_routing_table #list(sender_routing_table - self_routing_table) 
    else:
        mergedList = self_routing_table

    return mergedList 