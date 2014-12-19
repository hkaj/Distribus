#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import math
import sys
import uuid

from copy import deepcopy
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint
from PyQt4.QtGui import QImage

import globalvars


class Vehicle(object):
    """Base class for both cars and buses."""

    def __init__(self, position):
        self.user_id = uuid.uuid4()
        # array of arrays [[next_hop, number_hops_to_bus, ttl], ...]
        self.routing_table = []
        # dictionnary of downloaded files {"filename": "file_data", ...}
        self.file_table = {}
        # dictionnary of verified certificates {"certificate_name": "certificate_data", ...}
        self.certificate_table = {}
        # 2D position on the map
        self.position = position
        self.isBus = False
        # dictionnary for timeout management {"filename": [ticks_before_timeouts, frag_data_already_possessed]}
        self.timeouts = {}
        # messages sent to this vehicle this tick, which will be handled next round to emulate network speed
        # format: [ ["message_type", [data1, data2, data3]], ...]
        # a function like handle_message_type(data1, data2, data3) will be called on the recipient
        self.msg_fifo = []

    def update(self, vehicleList):
        """Called every clock tick in the system for each vehicle."""
        self.broadcast(vehicleList)
        # decrease TTL of each route
        if not self.isBus:
            for route in self.routing_table:
                route[2] -= 1
                if route[2] == 0:
                    self.routing_table.remove(route)
        # process the messages we have received...
        while self.msg_fifo:
            self.pop_msg_fifo()
        # ...and decrease timeouts of those we haven't
        for file_request in self.timeouts.keys():
            self.timeouts[file_request][0] -= 1
            if self.timeouts[file_request][0] < 0:
                print self, "Request for file timed out for:", file_request
                self.require_file(file_request, self.timeouts[file_request][1])

    def send_route_update_message(self, destination, self_routing_table):
        """Sends local routing table to neighbours"""
        # if the cost is "infinite" (>5) we consider the route down
        # this removes loops in the network after a certain amount
        # of time
        for route in self.routing_table:
            if route[1] > 5:
                self.routing_table.remove(route)
        self.send_to_vehicle(destination, "route_update", [self])

    def push_msg_fifo(self, message_type, args):
        """Adds a message in the FIFO for later processing (emulates network propagation time)"""
        self.msg_fifo.append([message_type, args])

    def send_to_vehicle(self, destination, message_type, message_args):
        destination.push_msg_fifo(message_type, message_args)

    def pop_msg_fifo(self):
        """Process next message in the local fifo"""
        message = self.msg_fifo[0]
        # check message type
        if message[0] == "route_update":
            self.receive_route_update_message(message[1][0])
        elif message[0] == "file_request":
            self.receive_file_request(message[1][0], message[1][1], message[1][2])
        elif message[0] == "file_response":
            self.receive_file_response(message[1][0], message[1][1], message[1][2])
        del self.msg_fifo[0]

    def receive_route_update_message(self, sender):
        """Process sender's route update message"""
        # buses don't need to update their table
        if not self.isBus:
            self.merge_routing_tables(sender)

    def require_file(self, filename, frag_data=None):
        """
        Tries to retrieve a file from given filename.
        May be called multiple times in case of timeouts or fragmentation

        """
        if not frag_data:
            frag_data = [None, [], []]
        # check if we actually need to download the file
        if filename in self.file_table:
            print "Already downloaded, aborting..."
            return
        # set a timeout for trying again if anything goes wrong
        self.timeouts[filename] = [globalvars.msg_timeout, frag_data]
        # is a bus reachable ?
        shortest_route = self.get_shortest_route()
        if not shortest_route:
            print self, "No bus is reachable, aborting download"
            return
        # setup file query protocol
        hop_list = [self, ]
        # frag_data is structured like this
        # frag_data[0] binary fragment data (simulated here)
        # frag_data[1] list of fragments already received, e.g. [1, 2, 3]
        # frag_data[2] array of information messages, written by the server for the client, can be "MORE_FRAGS" if more fragments expected, "CERTIFICATE" if the message is related to certificates
        # or "EOF" if this is the last fragment
        self.send_to_vehicle(shortest_route[0], "file_request", [filename, hop_list, frag_data])
        print self, "File requested:", filename

    def heuristic_choose(self, num_fragments, frag_data):
        """Tries to choose the best fragment to require from
        currently possessed ones and total number of fragments"""
        for i in range(1, num_fragments + 1):
            if i not in frag_data[1]:
                return i

    def receive_file_request(self, filename, hop_list, frag_data):
        """Routes a file request through the network"""
        if self.isBus:
            if "CERTIFICATE" in frag_data[2]:
                print self, "Received certificate request for", filename
                self.handle_certificate_request(filename, hop_list, frag_data)
            elif filename not in globalvars.file_table:
                print self, "Received request for", filename, "which doesn't exist!"
                return
            else:
                print self, "Received request for", filename
                # can we send the whole file at once ?
                if globalvars.file_table[filename]["size"] < globalvars.MTU:
                    frag_data[0] = filename
                    frag_data[2] = ["EOF"]
                else:
                    num_fragments = int(math.ceil( float(globalvars.file_table[filename]["size"]) / globalvars.MTU))
                    frag_to_send = self.heuristic_choose(num_fragments, frag_data)
                    frag_data[1].append(frag_to_send)
                    # is this the last fragment ?
                    if len(frag_data[1]) == num_fragments:
                        frag_data[2] = ["EOF"]
                    else:
                        frag_data[2] = ["MORE_FRAGS"]
                    frag_data[0] = filename + "_frag_" + str(frag_to_send)
                self.send_to_vehicle(hop_list[-1], "file_response", [filename, hop_list, frag_data])
        else:
            shortest_route = self.get_shortest_route()
            if not shortest_route:
                print self, "Dropped message (no route to bus)"
                return
            hop_list.append(self)
            self.send_to_vehicle(shortest_route[0], "file_request", [filename, hop_list, frag_data])

    def receive_file_response(self, filename, hop_list, frag_data):
        """Routes a file response to the sender"""
        del hop_list[-1]
        # still some routing needed
        if hop_list:
            self.send_to_vehicle(hop_list[-1], "file_response", [filename, hop_list, frag_data])
        # the message is for us !
        else:
            self.handle_file_received(filename, frag_data)

    def handle_file_received(self, filename, frag_data):
        """Handles data received from a file request"""
        print self, "File data received:", filename
        print frag_data
        if filename in self.timeouts:
            del self.timeouts[filename]
        # we have now the full file !
        if "EOF" in frag_data[2]:
            if "CERTIFICATE" in frag_data[2]:
                self.handle_certificate_response(filename, frag_data)
            else:
                self.file_table[filename] = globalvars.file_table[filename]["data"]
                print self.file_table
        # more fragments are needed...
        elif "MORE_FRAGS" in frag_data[2]:
            self.require_file(filename, frag_data)

    def get_percentage(self, filename):
        """Gets the percentage of the file already downloaded"""
        # file is partly downloaded
        if filename in self.timeouts and self.timeouts[filename][1]:
            return len(self.timeouts[filename][1][1]) / \
                   ( math.ceil( float(globalvars.file_table[filename]["size"]) / globalvars.MTU )) * 100
        # file is completely downloaded
        if filename in self.file_table:
            return 100
        # file download hasn't started yet
        return 0

    def is_vehicle_reachable(self, other):
        xDiff = self.position.x() - other.position.x()
        yDiff = self.position.y() - other.position.y()
        dist = math.sqrt(math.pow(xDiff, 2) + math.pow(yDiff, 2))
        if dist < globalvars.msg_distance:
            return True
        else:
            return False

    def broadcast(self, vehicleList):
        """Sends a route update message to each nearby vehicle"""
        for vehicle in vehicleList:
            if vehicle == self:
                continue
            else:
                if self.is_vehicle_reachable(vehicle):
                    self.send_route_update_message(vehicle, self.routing_table)

    def merge_routing_tables(self, sender):
        """Updates local routing table from information in the sender's routing table"""
        shortest_route = sender.get_shortest_route()
        # sender has some route to share and the route doesn't crosses us
        if shortest_route and shortest_route[0].user_id != self.user_id:
            updated = False
            # update the local route if exists
            for local_route in self.routing_table:
                if local_route[0].user_id == sender.user_id:
                    local_route[1] = shortest_route[1] + 1
                    local_route[2] = globalvars.max_ttl
                    updated = True
            # or add it if necessary
            if not updated:
                self.routing_table.append([sender, shortest_route[1] + 1, globalvars.max_ttl])

    def get_shortest_route(self):
        """Gets shortest route to a bus in the routing table"""
        shortest_route = None
        for route in self.routing_table:
            if not shortest_route or shortest_route[1] > route[1]:
                shortest_route = route
        return shortest_route

    def require_certificate(self, certificate):
        """Sends message to get the status of a certificate"""
        print self, "Certificate verification required for", certificate
        self.require_file(certificate, [None, [], ["CERTIFICATE"]])

    def handle_certificate_request(self, certificate_name, hop_list, frag_data):
        # internal routine of certificate checking
        frag_data[0] = globalvars.certificates[certificate_name]["status"]
        # normal response sending process
        frag_data[2].append("EOF")
        self.send_to_vehicle(hop_list[-1], "file_response", [certificate_name, hop_list, frag_data])

    def handle_certificate_response(self, certificate, frag_data):
        self.certificate_table[certificate] = {"status": frag_data[0]}
        print self, "Certificate for", certificate, "has state", frag_data[0]

    def get_certificate_status(self, certificate):
        if certificate in self.certificate_table:
            return self.certificate_table[certificate]["status"]
        else:
            return "  ?"

    def print_debug_info(self):
        """Prints useful debug information about a Vehicle"""
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
