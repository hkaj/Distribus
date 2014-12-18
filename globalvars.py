#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""This module declares program-wide variables"""

# time to live of a route in a routing table
max_ttl = 2

# timeout after message failure
msg_timeout = 5

# maximum distance between 2 vehicles for a message to be sent
msg_distance = 70

# maximum size of a packet before fragmenting
MTU = 5

# file table: dict of dicts (key is filename)
file_table = {
    "bus_timetable.pdf": {"size": 45,
                          "data": "Bus times in the beautiful city of Compiègne, Picardie, France."},
    "weather.txt": {"size": 2,
                    "data": "20C, partly cloudy"},
    "really_big_archive.zip": {"size": 450,
                               "data": "aWYgeW91IHJlYWQgdGhpcyB5b3UncmUgYSBnZWVrCg=="},
}

certificates = {
    "la_banque": {"name": "la_banque",
                  "id": 1,
                  "public_key": "01234567890123456789",
                  "status": "VALID"},
    "la_rnaque": {"name": "la_rnaque",
                  "id":2,
                  "public_key": "FFFFFFFFFFFFFFFFFFFF",
                  "status": "REVOKED"},
    "la_bstention": {"name": "la_bstention",
                  "id":3,
                  "public_key": "00000000000000000000",
                  "status": "UNKNOWN"},
}
