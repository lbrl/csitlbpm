#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
import ROOT as r
import sys
import os
# import glob
# import math as m
# import datetime
import numpy as np
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


def getCanvas( name, cw=600, ch=600, tm=.1, rm=.1 ):
    c1 = r.TCanvas( name, name, cw, ch )
    if not '-b' in sys.argv:
        c1.SetWindowSize(cw + (cw - c1.GetWw()), ch + (ch - c1.GetWh()));
    else:
        c1.SetCanvasSize(cw, ch)
    c1.SetTopMargin( tm )
    c1.SetRightMargin( rm )
    return c1


def get_graph(t, sel, cut, c=r.kBlack, ms=6):
    n = t.Draw(sel, cut, 'goff')
    x = t.GetV2()
    y = t.GetV1()
    x.SetSize( n )
    y.SetSize( n )
    x = np.array( x )
    y = np.array( y )
    g = r.TGraph( n, x, y )
    g.SetMarkerStyle( ms )
    g.SetMarkerColor( c )
    return g


def main():
    finname = 'rs.root'
    fin = r.TFile( finname )
    t = fin.Get( 't' )
    c1 = getCanvas( 'c1', 600, 600, tm=.05, rm=.05 )
    ####
    g5 = get_graph(t, '2.1 * S/(texp*25*npulse/nclock) : slit', 'thickness==5e-6',
            ms=24, c=r.kRed)
    g3 = get_graph(t, '2.1 * S/(texp*25*npulse/nclock) : slit', 'thickness==3e-6',
            ms=22, c=r.kBlue)
    ####
    g5.Draw( 'ap' )
    g3.Draw( 'p' )
    ####
    ax = g5.GetXaxis()
    ay = g5.GetYaxis()
    ax.SetTitle( 'Slit size, mm' )
    ay.SetTitle( 'Signal intensity, ph.e./pulse' )
    ax.SetTitleOffset( 1.3 )
    ay.SetTitleOffset( 1.3 )
    g5.SetTitle( '' )
    ####
    lat = r.TLatex()
    lat.SetTextSize( .04 )
    lat.SetTextFont( 12 )
    lat.SetTextColor( r.kRed )
    lat.DrawLatexNDC( .20, .90, '5 #mum, 45 deg.' )
    lat.SetTextColor( r.kBlue )
    lat.DrawLatexNDC( .20, .85, '3 #mum, 45 deg.' )
    ####
    c1.Update()
    ####
    if not '-b' in sys.argv:
        raw_input()
    if 'save' in sys.argv:
        c1.SaveAs( '~/Downloads/robust.png' )


if __name__ == '__main__':
    print 'Hi!'
    if 'trace' in sys.argv:
        trace()
    elif 'loss' in sys.argv:
        loss()
    else:
        main()
