#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from vehicle import Vehicle


class Car(Vehicle):
    """Represent a car."""
    def __init__(self, arg):
        super(Vehicle, self).__init__()

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
