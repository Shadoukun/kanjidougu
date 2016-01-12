from pytesseract import image_to_string
import PIL
from PIL import Image
import subprocess

import os
print os.environ['COMSPEC']
print os.listdir(os.getcwd())

blah = os.getcwd() + '\large.png'
img = Image.open(blah)
with Image.open('large.png') as img:
    print(image_to_string(img))
