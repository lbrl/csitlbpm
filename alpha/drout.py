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


def main():
    fin = r.TFile( 'g4beamline.root' )
    tloss = fin.Get( 'NTuple/blnt' )
    c1 = getCanvas( 'c1', 300, 600 )
    c1.SetTopMargin( .05 )
    c1.SetBottomMargin( .05 )
    tloss.Draw( 'x:z>>h1(100,-5,45,100,-50,50' , 'PDGid>1e9', 'goff' )
    h1 = r.gDirectory.Get( 'h1' )
    h1.GetXaxis().SetLabelOffset( -.01 )
    h1.Draw()
    c1.Update()
    raw_input()


def main2():
    r.gStyle.SetOptStat( 0 )
    fin = r.TFile( 'g4beamline.root' )
    foil = fin.Get( 'Detector/foil' )
    c1 = getCanvas( 'c1', 600, 600 )
    c1.SetGrid()
    nx = ny = 48
    h1 = r.TH2D( 'h1', 'Visible energy deposition in 5 #mum CsI(Tl) by #alpha from ^{241}Am', nx, -60, 60, ny, -60, 60 )
    ax = h1.GetXaxis()
    ay = h1.GetYaxis()
    for eve in foil:
        i = ax.FindBin( eve.x )
        j = ay.FindBin( eve.y )
        bc = h1.GetBinContent( i, j )
        h1.SetBinContent( i, j, bc+eve.VisibleEdep )
    h1.Draw( 'colz' )
    zmax = h1.GetMaximum()
    print 'zmax', zmax
    r.gStyle.SetNumberContours( min( 50, int(zmax)) )
    az = h1.GetZaxis()
    ax.SetTitle( 'Horizontal coordinate x, mm' )
    ay.SetTitle( 'Horizontal coordinate y, mm' )
    bwx = ax.GetBinWidth( 5 )
    bwy = ay.GetBinWidth( 5 )
    az.SetTitle( 'Visible deposited energy E_{dep}^{vis}, MeV/(%.1f mm x %.1f mm)' % (bwx, bwy) )
    c1.Modified()
    c1.Update()
    pal = h1.GetListOfFunctions().FindObject("palette")
    pal.SetX1NDC( .875 )
    pal.SetX2NDC( .9 )
    ax.SetTitleOffset( 1.3 )
    ay.SetTitleOffset( 1.3 )
    az.SetTitleOffset( 1.3 )
    c1.Modified()
    c1.Update()
    raw_input()
    if 'save' in sys.argv:
        c1.SaveAs( '~/Downloads/am241_in_5um_csitl_VisEdep_xy.png' )


def main3():
    r.gStyle.SetOptStat( 0 )
    r.TGaxis.SetMaxDigits( 3 )
    fin = r.TFile( 'g4beamline.root' )
    foil = fin.Get( 'Detector/foil' )
    c1 = getCanvas( 'c1', 600, 600 )
    foil.Draw( 'Edep >> h1(100,.3,3)', 'PDGid>1e9', 'goff' )
    foil.Draw( 'VisibleEdep >> h2(100,.3,3)', 'PDGid>1e9', 'goff' )
    h1 = r.gDirectory.Get( 'h1' )
    h2 = r.gDirectory.Get( 'h2' )
    h2.Draw()
    h1.Draw( 'same' )
    #
    lat = r.TLatex()
    lat.SetTextFont( 12 )
    lat.SetTextSize( .03 )
    h1.SetLineColor( r.kRed )
    h2.SetLineColor( r.kBlue )
    h1.SetLineWidth( 2 )
    h2.SetLineWidth( 2 )
    lat.SetTextColor( r.kRed )
    lat.DrawLatexNDC( .50, .85, 'Actual deposited energy.' )
    lat.DrawLatexNDC( .55, .80, 'Mean = {:.3f} MeV'.format( h1.GetMean() ) )
    lat.DrawLatexNDC( .55, .75, 'RMS = {:.3f} MeV'.format( h1.GetRMS() ) )
    lat.SetTextColor( r.kBlue )
    lat.DrawLatexNDC( .50, .70, 'Visible deposited energy.' )
    lat.DrawLatexNDC( .55, .65, 'Mean = {:.3f} MeV'.format( h2.GetMean() ) )
    lat.DrawLatexNDC( .55, .60, 'RMS = {:.3f} MeV'.format( h2.GetRMS() ) )
    #
    h2.GetXaxis().SetTitle( 'E_{dep}, MeV' )
    h2.GetXaxis().SetTitleOffset( 1.3 )
    h2.GetYaxis().SetTitle( 'Events' )
    h2.GetYaxis().SetTitleOffset( 1.3 )
    h2.SetTitle( 'Deposited energy by #alpha particles in the 5 #mum CsI(Tl) foil' )
    #
    c1.Update()
    raw_input()
    if 'save' in sys.argv:
        c1.SaveAs( '~/Downloads/am241_in_5um_csitl_Edep_VisEdep.png' )

if __name__ == '__main__':
    # main()
    main2()
    main3()
