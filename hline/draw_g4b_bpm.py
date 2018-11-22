#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
import ROOT as r
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


def main(tname='bpm1', title='BPM is between HB2 and HBB1-1'):
    fin = r.TFile( 'Yamazaki_20180405/optics/g4beamline.root' )
    t1 = fin.Get( 'VirtualDetector/{}'.format( tname ) )
    c1 = getCanvas( 'c1', 600, 600 )
    #
    # t1.Draw('x:y>>h1(40,-200,200,40,-200,200)', '', 'goff')
    t1.Draw('x:y>>h1(30,-150,150,30,-150,150)', '', 'goff')
    h1 = r.gDirectory.Get( 'h1' )
    h1.Draw( 'colz' )
    h1.SetTitle( title )
    ax, ay = h1.GetXaxis(), h1.GetYaxis()
    ax.SetTitle( 'X position, mm' )
    ay.SetTitle( 'Y position, mm' )
    ax.SetTitleOffset( 1.3 )
    ay.SetTitleOffset( 1.3 )
    #
    r.gStyle.SetStatX( .9 )
    r.gStyle.SetStatY( .9 )
    r.gStyle.SetStatW( .3 )
    #
    ell = r.TEllipse()
    ell.SetFillStyle( 0 )
    ell.SetLineWidth( 4 )
    ell.SetLineColor( r.kBlue )
    ell.DrawEllipse( 0, 0, 60, 60, 0, 360, 0 )
    ell.SetLineColor( r.kCyan )
    ell.DrawEllipse( 0, 0, 60/2**.5, 60, 0, 360, 0 )
    #
    lat = r.TLatex()
    lat.SetTextSize( .045 )
    lat.SetTextFont( 12 )
    lat.SetTextColor( r.kBlue )
    lat.DrawLatexNDC( .15, .85, '12 cm diameter, 90 degree' )
    lat.SetTextColor( r.kCyan+2 )
    lat.DrawLatexNDC( .15, .80, '12 cm diameter, 45 degree' )
    #
    c1.Update()
    if not '-b' in sys.argv:
        raw_input()
    if 'save' in sys.argv:
        c1.SaveAs( '~/Downloads/{}_xy.png'.format( tname ) )


if __name__ == '__main__':
    print 'Hi!'
    main()
    main('bpm2', 'BPM is between HBB1-1 and HQ1')
    main('bpm3', 'BPM is 1 m after HQ3')
