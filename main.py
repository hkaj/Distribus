#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import bus
import car
import vehicle

#initialize our dynamic nodes
vehicles = [bus.Bus(None), car.Car(None)]

def __main__():
    """Starts the environment"""
    while True:
        for v in vehicles:
            v.update()
