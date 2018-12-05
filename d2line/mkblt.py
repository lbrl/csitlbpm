#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
import ROOT as r
import sys
import os
# import glob
import math
# import datetime
# import numpy as np
# from array import array
# import re
# import matplotlib as ml
# import matplotlib.pyplot as plt
# from PIL import Image
import random

# R.gSystem.Load('libRooFit')


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def getCanvas( name, cw=600, ch=600 ):
    c1 = r.TCanvas( name, name, cw, ch )
    if not '-b' in sys.argv:
        c1.SetWindowSize(cw + (cw - c1.GetWw()), ch + (ch - c1.GetWh()));
    else:
        c1.SetCanvasSize(cw, ch)
    return c1


def totP( xx, pp ):
    p = xx[0]
    pmax = pp[0]
    res = 0.
    if p < pmax:
        res = 3.6 * p**2.6 / pmax**3.6
    return res


def main():
    pmax = 30.
    fp = r.TF1( 'fp', totP, 0, pmax, 1 )
    fp.SetParameter( 0, pmax )
    tau = 1.2
    weight = 1.
    pdgid = -13
    parent = 0
    trkid = 1
    z = 0.
    fout = open( 'myblt.BLTrackFile', 'w' )
    fout.write( "# BLTrackFile\n" )
    fout.write( "# generated by mkblt.py\n" )
    fout.write( "#\n" )
    fout.write( "# x y z Px Py Pz t PDGid EvNum TrkId Parent weight\n" )
    fout.write( "# mm mm mm MeV/c MeV/c MeV/c ns - - - - -\n" )
    #
    for i in xrange( 100000 ):
        pxpz = random.uniform( -.25, .25 )
        pypz = random.uniform( -.25, .25 )
        ptot = fp.GetRandom( 0, pmax )
        px = pxpz * ptot
        py = pypz * ptot
        pz = (ptot**2 - px**2 - py**2)**.5
        x = random.gauss( pxpz/.005, 4 )
        y = random.gauss( pypz/.005, 4 )
        t = random.expovariate( 1/tau ) + random.gauss( 2.55, 0.03 )
        out = ''
        for v in [x, y, z, px, py, pz, t, pdgid, i, trkid, parent, weight]:
            if type(v) == int:
                out += '{:>10} '.format(v)
            else:
                out += '  {:>8.6} '.format(v)
        out = out[:-1] + '\n'
        fout.write( out )
    fout.close()


if __name__ == '__main__':
    print 'Hi!'
    main()
