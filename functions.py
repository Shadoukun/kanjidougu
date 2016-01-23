import os
from PIL import Image, ImageGrab
from tempfile import NamedTemporaryFile
from nhocr import run_nhocr
import copy
import cv2
import numpy as np
import win32api


def bounding_box(height, width, x, y):
    """Returns 4 corners of a rectangle"""
    h, w = height, width
    minx = x - (w / 2)
    maxx = x + (w / 2)
    miny = y - (h / 2)
    maxy = y + (h / 2)
    return minx, miny, maxx, maxy


def imageOCR(h, w):
    # using win32api because Qt mousetracking frustrates me.
    cx, cy = win32api.GetCursorPos()
    # hides box and popup to prevent getting in image
#    if self.box.isVisible() is True:
#        self.box.setHidden(True)
#    if self.dialog.isVisible() is True:
#        self.dialog.setHidden(True)

    # grab image(with bounding_box), gets contours, runs nhOCR
    img = ImageGrab.grab(bbox=bounding_box(h, w, cx, cy))
    # returns resulting image and test/preview image
    result, preview = contourbox(img)
    # convert back to PIL image
    result = Image.fromarray(result)
    preview = Image.fromarray(preview)
    # Run OCR
    text = run_nhocr(result)

    return text, result, preview

def contourbox(img):
    temp = NamedTemporaryFile(delete=False)
    img.save(temp, 'png')
    im = cv2.imread(temp.name, cv2.IMREAD_UNCHANGED)
    img2gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img2gray, 0, 255, cv2.THRESH_OTSU)
    mask_inv = cv2.bitwise_not(thresh)

    # Dilate the image. Ideally the character is the largest contour.
    kernel = np.ones((1, 3), np.uint8)
    dilate = cv2.dilate(mask_inv, kernel, iterations=2)
    close = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)
    dilate2 = copy.copy(dilate)
    contours, _ = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(dilate, contours, -1, (127, 255, 0), -1)
    # Find the index of the largest contour
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    cnt = contours[max_index]
    x, y, w, h = cv2.boundingRect(cnt)
    boxpreview = copy.copy(im)
    crop_img = im[y: y+h, x: x+w]
    cv2.rectangle(boxpreview, (x, y), (x+w, y+h), (0, 0, 255), 1)
    temp.close()
    os.unlink(temp.name)
    # returns cropped image, and preview with rectangle
    return crop_img, boxpreview #, dilate, dilate2
