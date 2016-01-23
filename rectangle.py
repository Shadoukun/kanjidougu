#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
#from PyQt4 import QtGui, QtCore
from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
import ctypes
import win32api
import test
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

class bbox():
    cursorx, cursory = win32api.GetCursorPos()
    height = 0
    width = 0
    cx = 0
    cy = 0


class Box(QtWidgets.QWidget):

    closep = QtCore.pyqtSignal()

    def __init__(self):
        super(Box, self).__init__()
        self.width = 0
        self.height = 0
        self.cx = 0
        self.cy = 0
        self.initUI()

    def initUI(self):
        #self.setGeometry(300, 300, 350, 100)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.showFullScreen()

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

    def drawRectangles(self, qp):

        color = QtGui.QColor(255, 25, 25)
        #color.setNamedColor('#d4d4d4')
        pen = QtGui.QPen()
        pen.setColor(color)
        pen.setWidth(2)

        qp.setPen(pen)

        qp.setBrush(QtGui.QColor(0, 0, 0, 0))
        qp.drawRect(self.cx, self.cy, self.width, self.height)

    def leaveEvent(self, event):
        print("Enter")
        self.closep.emit()

def main(height, width, parent):

    bbox.height = height
    bbox.width = width
    cx, cy = win32api.GetCursorPos()
    bbox.cx = cx - (bbox.width / 2)
    bbox.cy = cy - (bbox.width / 2)

if __name__ == '__main__':
    main(50, 50)
