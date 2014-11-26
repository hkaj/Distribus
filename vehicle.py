#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import uuid


class Vehicle(object):
    """Base class for both cars and buses."""
    def __init__(self, args):
        user_id = uuid.uuid4()  # will be replaced by local MAC address
        MAXTTL = 3
        timeout = 2
        routing_table = {}  # next_node: (TTL, cost)
        file_table = []

    def update(self):
        """called every clock tick in the system for each element."""
        if len(self.routing_table) > 0 or hasattr(self, isBus):
            broadcast([ROUTE_UPDATE])
        for route in self.routing_table.items():
            route[1][0] -= 1
            if route[1][0] == 0:
                del(self.routing_table[route[0]])
