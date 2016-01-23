import sys
import os, os.path
import subprocess
from tempfile import NamedTemporaryFile
from subprocess import PIPE
from PIL import Image
import string
import jdict

print(os.environ['PYTHONIOENCODING'])
os.environ['NHOCR_DICDIR'] = os.path.abspath('./nhocr/Dic')
os.environ['CYGWIN'] = 'nodosfilewarning'
imgfile = os.path.join(os.getcwd() + '/screenshots/JsRUKkp.png')



def run_nhocr(img):
    tempimg = NamedTemporaryFile()
    img.save(tempimg, 'PPM')
    DEVNULL = open(os.devnull, 'wb')
    nhocr = os.path.abspath('./nhocr/nhocr.exe')
    line = subprocess.check_output([nhocr, '-line', tempimg.name, '-o', '-'], stderr=DEVNULL).decode('utf-8').rstrip()
    line = line
    blacklist = string.punctuation + string.ascii_letters
    return line  #.decode('utf-8')
