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


def dr_pipe(z, y, rin, rout, l, c=r.kGray):
    box = r.TBox()
    box.SetFillStyle( 1001 )
    box.SetFillColor( c )
    box.SetLineWidth( 1 )
    box.SetLineColor( c )
    box.DrawBox( z-l/2, y+rin, z+l/2, y+rout )
    box.DrawBox( z-l/2, y-rin, z+l/2, y-rout )


def dr_beamline(x, y):
    dr_pipe(533.3+200/2., y, 50, 55, 200 )
    dr_pipe(533.3+200+20/2., y, 30, 55, 20 )
    dr_pipe(533.3+200+20+120/2., y, 30, 35, 120 )
    dr_pipe(533.3+200+20+120+25/2., y, 16, 35, 25 )
    dr_pipe(533.3+200+20+120-50/2., y, 6, 30, 50, r.kTeal-9 )
    dr_pipe(533.3+200+20+120-50-50/2., y, 8, 30, 50, r.kTeal-9 )


def get_events_nums():
    fin = open( 'det8.BLTrackFile' )
    out = []
    for line in fin:
        if len(line) < 10:
            continue
        if line[0] == '#':
            continue
        lin = line.split()
        out.append( lin[8] )
    return out

def put_names():
    lat = r.TLatex()
    lat.SetTextSize( .04 )
    lat.SetTextFont( 12 )
    lat.SetTextAlign( 22 )
    lat.SetTextColor( r.kRed )
    lat.DrawLatexNDC( .80, .75, 'Positrons' )
    lat.SetTextColor( r.kGreen+1 )
    lat.DrawLatexNDC( .80, .50, 'Muons' )
    lat.SetTextColor( r.kBlue )
    lat.DrawLatexNDC( .80, .25, 'Electrons' )


def loss1d():
    r.gStyle.SetOptStat(0)
    finname = 'g4beamline.root'
    fin = r.TFile( finname )
    t = fin.Get( 'NTuple/blnt' )
    c2 = getCanvas( 'c2', 600, 600 )
    t.SetMarkerStyle( 6 )
    t.SetMarkerColor( r.kWhite )
    t.Draw( 'x : z >> h2(100,500,1000, 100,-250,250)', '500<z&&z<1000 && abs(x)<250' )
    h2 = r.gDirectory.Get( 'h2' )
    h2.SetTitle( 'Top view. Particle loss' )
    h2.GetXaxis().SetTitle( 'z, mm' )
    h2.GetYaxis().SetTitle( 'x, mm' )
    h2.GetXaxis().SetTitleOffset( 1.3 )
    h2.GetYaxis().SetTitleOffset( 1.3 )
    h2.Draw()
    dr_beamline( 0, 0 )
    dr_beamline( 0, 150 )
    dr_beamline( 0, -150 )
    t.SetMarkerColor( r.kGreen+2 )
    t.Draw( 'x : z', '500<z&&z<1000 && abs(x)<250 && PDGid==-13', 'same' )
    t.SetMarkerColor( r.kRed )
    t.Draw( 'x+150 : z', '500<z&&z<1000 && abs(x)<250 && PDGid==-11', 'same' )
    t.SetMarkerColor( r.kBlue )
    t.Draw( 'x-150 : z', '500<z&&z<1000 && abs(x)<250 && PDGid==11', 'same' )
    put_names()
    c2.Update()
    raw_input()
    if 'save' in sys.argv:
        c2.SaveAs( '~/Downloads/d2line_csitl_bpm_particle_loss_top_view.png' )

def loss():
    r.gStyle.SetOptStat(0)
    finname = 'g4beamline.root'
    fin = r.TFile( finname )
    t = fin.Get( 'NTuple/blnt' )
    c2 = getCanvas( 'c2', 1200, 600 )
    c2.Divide( 2, 1 )
    c2.cd( 1 )
    t.SetMarkerStyle( 6 )
    t.SetMarkerColor( r.kWhite )
    t.Draw( 'y : z >> h1(100,500,1000, 100,-250,250)', '500<z&&z<1000 && abs(y)<250' )
    h1 = r.gDirectory.Get( 'h1' )
    h1.GetXaxis().SetTitle( 'z, mm' )
    h1.GetYaxis().SetTitle( 'y, mm' )
    h1.GetXaxis().SetTitleOffset( 1.3 )
    h1.GetYaxis().SetTitleOffset( 1.3 )
    h1.Draw()
    dr_beamline( 0, 0 )
    dr_beamline( 0, 150 )
    dr_beamline( 0, -150 )
    t.SetMarkerColor( r.kGreen+2 )
    t.Draw( 'y : z', '500<z&&z<1000 && abs(y)<250 && PDGid==-13', 'same' )
    t.SetMarkerColor( r.kRed )
    t.Draw( 'y+150 : z', '500<z&&z<1000 && abs(y)<250 && PDGid==-11', 'same' )
    t.SetMarkerColor( r.kBlue )
    t.Draw( 'y-150 : z', '500<z&&z<1000 && abs(y)<250 && PDGid==11', 'same' )
    put_names()
    c2.cd( 2 )
    t.SetMarkerColor( r.kWhite )
    t.Draw( 'x : z >> h2(100,500,1000, 100,-250,250)', '500<z&&z<1000 && abs(x)<250' )
    h2 = r.gDirectory.Get( 'h2' )
    h2.GetXaxis().SetTitle( 'z, mm' )
    h2.GetYaxis().SetTitle( 'x, mm' )
    h2.GetXaxis().SetTitleOffset( 1.3 )
    h2.GetYaxis().SetTitleOffset( 1.3 )
    h2.Draw()
    dr_beamline( 0, 0 )
    dr_beamline( 0, 150 )
    dr_beamline( 0, -150 )
    t.SetMarkerColor( r.kGreen+2 )
    t.Draw( 'x : z', '500<z&&z<1000 && abs(x)<250 && PDGid==-13', 'same' )
    t.SetMarkerColor( r.kRed )
    t.Draw( 'x+150 : z', '500<z&&z<1000 && abs(x)<250 && PDGid==-11', 'same' )
    t.SetMarkerColor( r.kBlue )
    t.Draw( 'x-150 : z', '500<z&&z<1000 && abs(x)<250 && PDGid==11', 'same' )
    c2.cd()
    c2.Update()
    raw_input()
    if 'save' in sys.argv:
        c2.SaveAs( '~/Downloads/d2line_csitl_bpm_particle_loss.png' )


def trace():
    finname = 'g4beamline.root'
    fin = r.TFile( finname )
    c2 = getCanvas( 'c2', 600, 600 )
    enum = get_events_nums()
    trs = []
    for v in enum[:50]:
        tr = fin.Get( 'Trace/Ev{}Trk1'.format( v ) )
        print tr
        if type(tr) == r.TNtuple:
            trs.append( tr )
    pls = []
    view = r.TView.CreateView( 1 )
    # view.SetRange( -500, 500, -500, 500, -1000, 3000 )
    view.SetRange( -500, -500, 0, 500, 500, 1000 )
    for tr in trs:
        n = tr.GetEntries()
        i = 0
        pl = r.TPolyLine3D( n )
        for eve in tr:
            pl.SetPoint( i, eve.x, eve.y, eve.z )
            i += 1
        pl.Draw()
        pls.append( pl )
    c2.Update()
    ####
    raw_input()


def main():
    finname = 'g4beamline.root'
    fin = r.TFile( finname )
    t = []
    for i in xrange(1, 9):
        x = fin.Get( 'VirtualDetector/det{}'.format(i) )
        if type(x) == r.TNtuple:
            t.append( x )
    c1 = getCanvas( 'c1', 1200, 600 )
    c1.Divide( 4, 2 )
    hopt = '(80,-100,100,80,-100,100)'
    for i, x in enumerate(t):
        c1.cd(i+1)
        x.Draw( 'y : x >> h{}{}'.format( i+1, hopt ), 'PDGid==-13', 'colz' )
    c1.Update()
    ####
    raw_input()


if __name__ == '__main__':
    print 'Hi!'
    if 'trace' in sys.argv:
        trace()
    elif 'loss' in sys.argv:
        loss()
    elif 'loss1d' in sys.argv:
        loss1d()
    else:
        main()
