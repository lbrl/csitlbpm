#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
import ROOT as r
import sys
import os
# import glob
# import math as m
# import datetime
# import numpy as np
# from array import array
# import re
# import matplotlib as ml
# import matplotlib.pyplot as plt
# from PIL import Image

# R.gSystem.Load('libRooFit')


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def main():
    finname = '150501_Dline_00.root'
    fin = r.TFile( finname )
    t = fin.Get( 'VirtualDetector/det8' )
    print t.GetEntries()
    i = 0
    for eve in t:
        if i > 50:
            pass
        # x y z Px Py Pz t PDGid EvNum TrkId Parent weight
        out = '{:>10.4f}{:>10.4f}{:>10.4f}'.format( eve.x-100, eve.y, eve.z-24024.4 )
        out += '{:>10.4f}{:>10.4f}{:>10.4f}'.format( eve.Px, eve.Py, eve.Pz )
        out += '{:>10.4f}{:>10.0f}{:>10.0f}{:>10.0f}'.format( eve.t, eve.PDGid, eve.EventID, eve.TrackID )
        out += '{:>10.0f}{:>10.0f}'.format( eve.ParentID, eve.Weight )
        print out
        i += 1


if __name__ == '__main__':
    print 'Hi!'
    main()
