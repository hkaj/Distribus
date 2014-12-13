from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QSize
from PyQt4.QtGui import QImage, QIcon, QPushButton, QPixmap
from vehicle import Vehicle



class Bus(Vehicle):
    """Represents a bus."""
    def __init__(self, position):
        super(Bus, self).__init__(position)
        self.isBus = True
        self.routing_table = [[self, 0, 3]]
        self.img = QIcon(QPixmap('media/bus.png')) #quote this line if testing the NON gui version
