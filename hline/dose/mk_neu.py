#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
import ROOT as r
import sys
import os
import random
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


def get_xy(R):
    while 1:
        x = np.random.uniform(-R, R)
        y = np.random.uniform(-R, R)
        if x**2 + y**2 < R**2:
            break
    return [x, y]


def random_three_vector():
    """
    Generates a random 3D unit vector (direction) with a uniform spherical distribution
    Algo from http://stackoverflow.com/questions/5408276/python-uniform-spherical-distribution
    :return:
    """
    phi = np.random.uniform(0, np.pi*2)
    costheta = np.random.uniform(-1, 1)

    theta = np.arccos( costheta )
    x = np.sin( theta) * np.cos( phi )
    y = np.sin( theta) * np.sin( phi )
    z = np.cos( theta )
    return (x, y, z)


def what_happend( dp ):
    tot = sum(dp)
    p = [ dp[0]/tot ]
    for x in dp[1:]:
        p.append( p[-1]+x/tot )
    # print 'p', p
    proba = np.random.uniform(0, 1)
    # print 'proba', proba
    for i, x in enumerate(p):
        # print i, x
        if proba <= x:
            # print 'return', i
            return i

def T2p(T, m):
    return ((m+T)**2 - m**2)**.5


def mainroot():
    n = 10000000
    weight = 1
    parentid = 0
    R = 18./2
    pdgid = '2112'# neutron
    # pdgid = '2212'# proton
    #
    mneu = 939.56563
    ghg = get_gr()
    #
    x = np.zeros(1, dtype=float)
    y = np.zeros(1, dtype=float)
    z = np.zeros(1, dtype=float)
    Px = np.zeros(1, dtype=float)
    Py = np.zeros(1, dtype=float)
    Pz = np.zeros(1, dtype=float)
    time = np.zeros(1, dtype=float)
    PDGid = np.zeros(1, dtype=float)
    EvNum = np.zeros(1, dtype=float)
    TrkId = np.zeros(1, dtype=float)
    Parent = np.zeros(1, dtype=float)
    weight = np.zeros(1, dtype=float)
    Fout = r.TFile( 'neu.root', 'recreate' )
    t = r.TTree( 't', 'tree with initial neutrons' )
    t.Branch( 'x', x, 'x/F' )
    t.Branch( 'y', y, 'y/F' )
    t.Branch( 'z', z, 'z/F' )
    t.Branch( 'Px', Px, 'Px/F' )
    t.Branch( 'Py', Py, 'Py/F' )
    t.Branch( 'Pz', Pz, 'Pz/F' )
    t.Branch( 't', time, 't/F' )
    t.Branch( 'PDGid', PDGid, 'PDGid/F' )
    t.Branch( 'EvNum', EvNum, 'EvNum/F' )
    t.Branch( 'TrkId', TrkId, 'TrkId/F' )
    t.Branch( 'Parent', Parent, 'Parent/F' )
    t.Branch( 'Weight', weight, 'Weight/F' )
    #
    weight[0] = 0
    for i in xrange(n):
        z = 0.
        xy = get_xy(R)
        x[0], y[0] = xy[0], xy[1]
        (nx, ny, nz) = random_three_vector()
        #
        p = T2p( ghg[1].GetRandom(), mneu )
        #
        Px[0] = p*nx
        Py[0] = p*ny
        Pz[0] = p*abs(nz)# to one hemisphere
        EvNum[0] = i
        TrkId[0] = 1
        time[0] = 0.
        t.Fill()
    t.Write()
    Fout.Close()

def main():
    n = 10000000
    weight = 1
    parentid = 0
    R = 18./2
    pdgid = '2112'# neutron
    # pdgid = '2212'# proton
    #
    mneu = 939.56563
    ghg = get_gr()
    #
    print '#BLTrackFile ... user comment...'
    print '#x y z Px Py Pz t PDGid EvNum TrkId Parent weight'
    print '#mm mm mm MeV/c MeV/c MeV/c ns - - - - -'
    for i in xrange(n):
        z = 0.
        xy = get_xy(R)
        x, y = xy[0], xy[1]
        (nx, ny, nz) = random_three_vector()
        #
        p = T2p( ghg[1].GetRandom(), mneu )
        #
        px = p*nx
        py = p*ny
        pz = p*abs(nz)# to one hemisphere
        eventid = i
        trackid = 1
        t = 0.
        # x y z Px Py Pz t PDGid EvNum TrkId Parent weight
        out = '{:>10.4f} {:>10.4f} {:>10.4f}'.format( x, y, z )
        out += ' {:>10.4f} {:>10.4f} {:>10.4f}'.format( px, py, pz )
        out += ' {:>10.4f} {:>10} {:>10.0f} {:>10.0f}'.format( t, pdgid, eventid, trackid )
        out += ' {:>10.0f} {:>10.0f}'.format( parentid, weight )
        print out


if __name__ == '__main__':
    main()
