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
        self.file_table = {} #downloaded files
        self.position = position
        self.isBus = False
        #dictionnary for timeout management (keys are file names we asked for, values number of
        #ticks left before asking them again
        self.timeouts = {}
        #messages sent to this vehicle this tick, which will be handled next round to emulate network speed
        #format: [ ["message_type", [data1, data2, data3]], ...]
        #a function like handle_message_type(data1, data2, data3) will be called on the recipient
        self.msg_fifo = []

    def update(self, vehicleList):
        """called every clock tick in the system for each vehicle."""
        #update neighbours' routing table
        self.broadcast(vehicleList)
        #decrease TTL of each route
        if not self.isBus:
            for route in self.routing_table:
                route[2] -= 1
                if route[2] == 0:
                    self.routing_table.remove(route)
        #process the messages we have received...
        while self.msg_fifo:
            self.pop_msg_fifo()
        #...and decrease timeouts of those we haven't
        for file_request in self.timeouts.keys():
            self.timeouts[file_request] -= 1
            if self.timeouts[file_request] < 0:
                print self, "Request for file timed out for:", file_request
                del self.timeouts[file_request]

    def send_route_update_message(self, destination, self_routing_table):
        """sends local routing table to neighbours"""
        #if the cost is "infinite" (>5) we consider the route down
        #this removes loops in the network after a certain amount
        #of time
        for route in self.routing_table:
            if route[1] > 5:
                self.routing_table.remove(route)
        destination.push_msg_fifo("route_update", [self])

    def push_msg_fifo(self, message_type, args):
        """adds a message to the buffer, all messages will be handled in next update"""
        self.msg_fifo.append([message_type, args])

    def pop_msg_fifo(self):
        """process next message in the local fifo"""
        message = self.msg_fifo[0]
        #check message type
        if message[0] == "route_update":
            self.receive_route_update_message(message[1][0])
        elif message[0] == "file_request":
            self.receive_file_request(message[1][0], message[1][1], message[1][2])
        elif message[0] == "file_response":
            self.receive_file_response(message[1][0], message[1][1], message[1][2])
        del self.msg_fifo[0]

    def receive_route_update_message(self, sender):
        #buses don't need to update their table
        if not self.isBus:
            self.merge_routing_tables(sender)

    def require_file(self, filename):
        """tries to retrieve a file from given filename"""
        #can we connect to a bus ?
        shortest_route = self.get_shortest_route()
        if not shortest_route:
            print self, "No bus is reachable, aborting download"
            return
        #setup file query protocol
        hop_list = [self,]
        frag_data = []
        shortest_route[0].push_msg_fifo("file_request", [filename, hop_list, frag_data])
        self.timeouts[filename] = globalvars.msg_timeout
        print self, "File requested:", filename

    def receive_file_request(self, filename, hop_list, frag_data):
        """routes a file request through the network"""
        if self.isBus:
            if not globalvars.file_table.has_key(filename):
                print self, "Received request for", filename, "which doesn't exist!"
                return
            print self, "Received request for", filename
            #can we send the whole file at once ?
            if globalvars.file_table[filename]["size"] < globalvars.MTU:
                frag_data.append(globalvars.file_table[filename]["data"])
                hop_list[-1].push_msg_fifo("file_response", [filename, hop_list, frag_data])
        else:
            shortest_route = self.get_shortest_route()
            if not shortest_route:
                return
            hop_list.append(self)
            shortest_route[0].push_msg_fifo("file_request", [filename, hop_list, frag_data])

    def receive_file_response(self, filename, hop_list, frag_data):
        """routes a file response to the sender"""
        del hop_list[-1]
        #still some routing needed
        if hop_list:
            hop_list[-1].push_msg_fifo("file_response", [filename, hop_list, frag_data])
        #the message is for us !
        else:
            self.handle_file_received(filename, frag_data)

    def handle_file_received(self, filename, frag_data):
        """handles data received from a file request"""
        print self, "File data received:", filename
        del self.timeouts[filename]
        #data was sent in one message
        if len(frag_data) == 1:
            self.file_table[filename] = frag_data[0]

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

    def print_debug_info(self):
        """prints useful debug information about a Vehicle"""
        print ""
        print self, "at", self.position
        print "fifo"
        print self.msg_fifo
        print "routing table:"
        print self.routing_table
        print "file table:"
        print self.file_table
        print "timeouts:"
        print self.timeouts