#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from vehicle import Vehicle


class Bus(Vehicle):
    """Represent a bus."""
    def __init__(self, arg):
        super(Vehicle, self).__init__()
        self.isBus = True