#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import movingarea

import sys
from PyQt4 import QtGui


def main():
		
	app = QtGui.QApplication(sys.argv)
	map = movingarea.MovingArea()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
