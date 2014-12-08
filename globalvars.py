#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""This module declares program-wide variables"""

#time to live of a route in a routing table
max_ttl = 2

#timeout after message failure
msg_timeout = 5

#maximum distance between 2 vehicles for a message to be sent
msg_distance = 100

#maximum size of a packet before fragmenting
MTU = 50

#file table: dict of dicts (key is filename)
file_table = {
    "bus_timetable.pdf": {"size": 45,
                          "data": "Bus times in the beautiful city of Compiègne, Picardie, France."},
}
