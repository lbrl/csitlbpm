#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
# import ROOT as r
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


def main():
    n = 100000
    weight = 1
    parentid = 0
    R = 18./2
    pdgid = '1000020040'
    #
    T = [5.48556, 5.44280, 5.38823]
    prob = [.845, .130, .016]
    totprob = sum(prob)
    print '# totprob', totprob
    malpha = 3727.3
    E = [x + malpha for x in T]
    momenta = [(x**2 - malpha**2)**.5 for x in E]
    print '# momenta = {}'.format( momenta )
    #
    for i in xrange(n):
        z = 0.
        xy = get_xy(R)
        x, y = xy[0], xy[1]
        (nx, ny, nz) = random_three_vector()
        #
        p = momenta[ what_happend( prob ) ]
        # print '*'*10, 'choosen p', p, '*'*10
        #
        px = p*nx
        py = p*ny
        pz = p*nz
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
