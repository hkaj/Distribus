#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from vehicle import Vehicle


class Bus(Vehicle):
    """Represents a bus."""
    def __init__(self, arg):
        super(Bus, self).__init__(arg)
        self.isBus = True
