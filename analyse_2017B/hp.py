#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
# import ROOT as r
import sys
import os
import glob
# import math as m
# import datetime
# import numpy as np
# from array import array
# import re
# import matplotlib as ml
# import matplotlib.pyplot as plt
# from PIL import Image

# R.gSystem.Load('libRooFit')


def main():
    pat = sys.argv[1]
    names = glob.glob( pat )
    for name in names:
        run = name.split('/')[-1]
        cmd = '''time root 'hp.C+("BPM_ROOT/{run}", "hp/{run}")' -b -q'''.format( run = run )
        os.system( cmd )


if __name__ == '__main__':
    print 'Hi!'
    main()
