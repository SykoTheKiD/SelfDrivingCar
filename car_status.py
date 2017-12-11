import numpy as np
import os, time
from PIL import ImageOps, ImageGrab

def screenGrab():
    im = ImageGrab.grab(bbox=(0,40,800,640))
    return im


def grab():
    im = ImageOps.grayscale(ImageGrab.grab(bbox=(0,40,800,625)))
    a = np.array(im.getcolors())
    a = a.sum()
    # im.save(os.getcwd() + '\\Snap__' + str(int(time.time())) + '.png', 'PNG')
    print(a)
    return a