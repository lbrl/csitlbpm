#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
import ROOT as r
import sys
import os
import glob
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


def getCanvas( name, cw=600, ch=600, margins=-1 ):
    c1 = r.TCanvas( name, name, cw, ch )
    if not '-b' in sys.argv:
        c1.SetWindowSize(cw + (cw - c1.GetWw()), ch + (ch - c1.GetWh()));
    else:
        c1.SetCanvasSize(cw, ch)
    if margins != -1:
        c1.SetLeftMargin( margins[0] )
        c1.SetBottomMargin( margins[1] )
        c1.SetRightMargin( margins[2] )
        c1.SetTopMargin( margins[3] )
    return c1


def get_gr( finname, c=r.kBlack ):
    fin = open( finname )
    x, y = [], []
    for line in fin:
        lin = line.replace(',', '').split()
        x.append( float( lin[0] ) )
        y.append( abs( float( lin[1] ) ) )
    g = r.TGraph( len(x), np.array(x), np.array(y) )
    g.SetLineColor( c )
    g.SetMarkerColor( c )
    return g


def get_fz():
    fin = open( 'FZ.dat' )
    res = []
    for line in fin:
        lin = line.rstrip('\n').replace(' ', '').split('=')
        # res[ lin[0][:-3] ] = float( lin[1] )/1000.
        res.append( [ lin[0][:-3], float( lin[1] )/1000.] )
    res = sorted(res, key=lambda x: x[1])
    fin.close()
    return res


def get_len():
    fin = open( 'Len.dat' )
    res = {}
    for line in fin:
        if len(line) < 3:
            continue
        if line[0] == '#':
            continue
        lin = line.rstrip('\n').replace(' ', '').split('=')
        if '_Len' in lin[0]:
            res[ lin[0][:-4] ] = float( lin[1] )/1000.
        elif '_bl' in lin[0]:
            res[ lin[0][:-3] ] = float( lin[1] )/1000.
        else:
            print WARNING+"get_len : Can't process the line"+ENDC
            print '\t', line
    fin.close()
    return res


def main(tname='bpm1', title='H- and H1-line beam envelope'):
    t = r.TTree( 't', '' )
    #Z N meanX sigmaX meanY sigmaY emitX emitY emitTrans betaX betaY betaTrans alphaX alphaY alphaTrans meanP
    t.ReadFile( 'Yamazaki_20180405/optics/h2_profile_m100.txt',
            'z/F:n/I:mx/F:sx:my:sy:ex:ey:et:bx:by:bt:ax:ay:at:mp' )
    #
    c1 = getCanvas( 'c1', 1200, 600, margins=[.05, .1, .05, .1])
    frame1 = c1.DrawFrame( 0, 0, 26, 500, title )
    c1.SetGridy()
    #
    n = t.Draw('3*sx:z/1000.:3*sy', '', 'goff')
    z = t.GetV2()
    sx = t.GetV1()
    sy = t.GetV3()
    z.SetSize( n )
    sx.SetSize( n )
    sy.SetSize( n )
    h1 = r.TGraph( n, np.array(z), np.array(sx) )
    h2 = r.TGraph( n, np.array(z), np.array(sy) )
    h1.SetLineColor( r.kBlue )
    h1.SetMarkerColor( r.kBlue )
    h2.SetLineColor( r.kRed )
    h2.SetMarkerColor( r.kRed )
    #
    gx = get_gr( 'H-line_envelope_3sigmax.dat', c=r.kBlue+2 )
    gy = get_gr( 'H-line_envelope_3sigmay.dat', c=r.kRed+2 )
    #
    h1.Draw( 'lp' )
    h2.Draw( 'lp' )
    gx.Draw( 'lp' )
    gy.Draw( 'lp' )
    h1.SetTitle( title )
    # ax, ay = h1.GetXaxis(), h1.GetYaxis()
    ax, ay = frame1.GetXaxis(), frame1.GetYaxis()
    ax.SetTitle( 'z coordinate, m' )
    ay.SetTitle( '3#times#sigma, mm' )
    ax.SetTitleOffset( 1.4/2. )
    ay.SetTitleOffset( 1.4/2. )
    #
    r.gStyle.SetStatX( .9 )
    r.gStyle.SetStatY( .9 )
    r.gStyle.SetStatW( .3 )
    #
    lat = r.TLatex()
    lat.SetTextSize( .045 )
    lat.SetTextFont( 12 )
    lat.SetTextColor( r.kBlue )
    lat.DrawLatexNDC( .15, .85, '#sigma_{x}, G4beamline' )
    lat.SetTextColor( r.kBlue+2 )
    lat.DrawLatexNDC( .15, .80, '#sigma_{x}, paper' )
    lat.SetTextColor( r.kRed )
    lat.DrawLatexNDC( .50, .85, '#sigma_{y}, G4beamline' )
    lat.SetTextColor( r.kRed+2 )
    lat.DrawLatexNDC( .50, .80, '#sigma_{y}, paper' )
    #
    line = r.TLine()
    line.SetLineColor( r.kViolet )
    lat.SetTextColor( r.kViolet )
    lat.SetTextSize( .03 )
    lat.SetTextAlign( 22 )
    fz = get_fz()
    Len = get_len()
    i = 0
    for v in fz:
        if not v[0] in Len:
            line.DrawLine( v[1], 0, v[1], 100 )
        else:
            dx = Len[ v[0] ] / 2.
            line.DrawLine( v[1]-dx, 0, v[1]-dx, 100 )
            line.DrawLine( v[1]-dx, 100, v[1]+dx, 100 )
            line.DrawLine( v[1]+dx, 0, v[1]+dx, 100 )
        lat.DrawLatex( v[1], -25-15*(i%2), v[0] )
        i += 1
    #
    c1.Update()
    if not '-b' in sys.argv:
        raw_input()
    if 'save' in sys.argv:
        c1.SaveAs( '~/Downloads/h1_line_envelope.png' )


if __name__ == '__main__':
    print 'Hi!'
    main()
