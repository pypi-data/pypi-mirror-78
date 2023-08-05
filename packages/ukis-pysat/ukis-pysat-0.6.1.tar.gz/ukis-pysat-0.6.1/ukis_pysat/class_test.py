import os
import numpy as np
from ukis_pysat import raster as pysat_raster

class Stuff:
    def __init__(self, path):
        self.path_to_img = os.path.join(path, 'source.tif')
        self.img = pysat_raster.Image(self.path_to_img)
        self.new_img = None

    def alter(self):
        self.img.arr = self.img.arr * 10

if __name__ == '__main__':
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'tests', 'testfiles', 'vrt'))

    stuff = Stuff(root_dir)
    print(stuff.img.arr)
    stuff.alter()
    print(stuff.img.arr)
    #print(stuff.new_img.arr)
