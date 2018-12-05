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


def getCanvas( name, cw=600, ch=600 ):
    c1 = r.TCanvas( name, name, cw, ch )
    if not '-b' in sys.argv:
        c1.SetWindowSize(cw + (cw - c1.GetWw()), ch + (ch - c1.GetWh()));
    else:
        c1.SetCanvasSize(cw, ch)
    return c1


def dr_xz():
    finname = 'g4bl_beam_evolultion_det8.root'
    fin = r.TFile( finname )
    t = []
    zz = [1, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
    for i in zz:
        x = fin.Get( 'VirtualDetector/det{}'.format(i) )
        if type(x) == r.TNtuple:
            t.append( x )
    h = []
    cut = 'PDGid==-13'
    hopt = '(30, 500, 1100, 20, -100, 100)'
    for i, x in enumerate(t):
        x.Draw( 'x : z >> h{}{}'.format( i, hopt ), cut, 'goff' )
        h.append( r.gDirectory.Get( 'h{}'.format( i ) ) )
        print h[-1]
    for x in h[1:]:
        h[0].Add( x )
    c1 = getCanvas( 'c1' )
    h[0].Draw( 'lego20' )
    c1.Update()
    raw_input()


def main(
        finname = 'g4beamline.root'
        ):
    r.gStyle.SetStatX( .9 )
    r.gStyle.SetStatY( .9 )
    r.gStyle.SetStatW( .3 )
    fin = r.TFile( finname )
    t = []
    zz = [1, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
    for i in zz:
        x = fin.Get( 'VirtualDetector/det{}'.format(i) )
        if type(x) == r.TNtuple:
            t.append( x )
    c1 = getCanvas( 'c1', 4*250, 3*250 )
    c1.Divide( 4, 3 )
    hopt = '(40,-100,100,40,-100,100)'
    hh = []
    for i, x in enumerate(t):
        c1.cd(i+1)
        x.Draw( 'y : x >> h{}{}'.format( i+1, hopt ), 'PDGid==-13', 'goff' )
        hh.append( r.gDirectory.Get( 'h{}'.format( i+1 ) ) )
        hh[-1].Draw( 'colz' )
        hh[-1].SetContour( 15 )
        hh[-1].SetMaximum( 150 )
        hh[-1].SetTitle( 'Distance from det8 is {} mm'.format( zz[i] ) )
        hh[-1].GetXaxis().SetTitle( 'x, mm' )
        hh[-1].GetXaxis().SetTitleOffset( 1.3 )
        hh[-1].GetYaxis().SetTitle( 'y, mm' )
        hh[-1].GetYaxis().SetTitleOffset( 1.3 )
    c1.Update()
    ####
    if not '-b' in sys.argv:
        raw_input()
    if 'save' in sys.argv:
        c1.SaveAs( '~/Downloads/d2_beam_evolution_{}.png'.format(
            finname.split('.')[0].split('evolution_')[-1] ) )


if __name__ == '__main__':
    dr_xz()
    # main( 'g4bl_beam_evolultion_det8_dq13-15.root' )
    # main( 'g4bl_beam_evolultion_det8.root' )
