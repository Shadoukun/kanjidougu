import os
import sys
import pytesseract
from PIL import Image, ImageGrab
from pytesseract import image_to_string
import ctypes
from PyQt4 import QtCore
from PyQt4 import QtGui
import win32api
import numpy as np
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()



def runtesseract(img):
    tesseractloc = os.getcwd() + '\\Tesseract-OCR\\tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = tesseractloc
    return image_to_string(img, lang='jpn')

#runtesseract()
#dc = windll.user32.GetDC(0)
#blah = ImageGrab.grab()
#blah.show()

#bbox = planar.BoundingBox.from_center((100, 100), width=10, height=10)
#bboxp = bbox.to_polygon()
#print int(bboxp[1])
#(x0, y0, x1, y1) = bboxp[0], bboxp[1], bboxp[2], bboxp[3]

#blah = ImageGrab.grab(bbox=(100,100,500,500))
#blah.show()

def bounding_box(height, width, x, y):
    h = height
    w = width
    minx = x - (w / 2)
    maxx = x + (w / 2)
    miny = y - (h / 2)
    maxy = y + (h / 2)
    return minx, miny, maxx, maxy

#print win32api.GetCursorPos()
#blah = ImageGrab.grab(bounding_box(50, 50, win32api.GetCursorPos()))
#print bounding_box(75, 75, *win32api.GetCursorPos())
##blah.show()
