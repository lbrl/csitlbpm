#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
import ROOT as r
import sys
import os
# import glob
import math
# import datetime
import numpy as np
# from array import array
# import re
# import matplotlib as ml
# import matplotlib.pyplot as plt
# from PIL import Image

# R.gSystem.Load('libRooFit')

# from wr_neutron import wrn


def getCanvas( name, cw=600, ch=600 ):
    c1 = r.TCanvas( name, name, cw, ch )
    if not '-b' in sys.argv:
        c1.SetWindowSize(cw + (cw - c1.GetWw()), ch + (ch - c1.GetWh()));
    else:
        c1.SetCanvasSize(cw, ch)
    return c1


def get_gr():
    finname = 'flux_BPMs.dat'
    fin = open( finname )
    lines = fin.readlines()
    #  e-lower      e-upper      neutron     r.err    photon      r.err
    xl, xu = [], []
    x, y, ye = [], [], []
    xe = []
    x1, y1 = [], []
    for i in xrange(51, 151):
        lin = lines[i].split()
        xl.append( float(lin[0]) )
        xu.append( float(lin[1]) )
        y.append( float(lin[2]) )
        ye.append( float(lin[3]) )
        #
        x.append( (xl[-1]+xu[-1])/2. )
        xe.append( (xu[-1]-xl[-1])/2. )
        #
        x1.extend( [xl[-1], xu[-1]] )
        y1.extend( [y[-1], y[-1]] )
    # Make a histogram.
    g1 = r.TGraph( len(x1), np.array(x1), np.array(y1) )
    w = xu[0]-xl[0]
    n = int( (xu[-1] - xl[0])/w )
    print 'w', w
    print 'n', n
    h = r.TH1D( 'h', 'h', n, xl[0], xu[-1] )
    j = 0
    for i in xrange(1, n+1):
        bcen = h.GetBinCenter( i )
        while not (xl[j] <= bcen and bcen <= xu[j]):
            j += 1
        h.SetBinContent( i, y[j] )
    #
    n = len(x)
    g = r.TGraphErrors( n, np.array(x), np.array(y), np.array(xe), np.array(ye) )
    g.SetMarkerStyle( 6 )
    clr = r.kViolet
    g.SetMarkerColor( clr )
    g.SetLineColor( clr )
    return [g, h, g1]


def main():
    c1 = getCanvas( 'c1' )
    c1.SetLogx()
    c1.SetLogy()
    gh = get_gr()
    # g.Draw( 'al' )
    gh[0].Draw( 'ap' )
    gh[1].Draw( 'same' )
    gh[2].Draw( 'l' )
    c1.Update()
    raw_input()


if __name__ == '__main__':
    main()
