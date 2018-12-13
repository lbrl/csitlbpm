#! /usr/bin/env python

# from ROOT import RooFit as rf
# from ROOT import *
# import ROOT as r
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

# R.gSystem.Load('libRooFit')


def read_tubs():
    finname = 'beamtest2017B-tubs.tsv'
    fin = open( finname )
    out = []
    for line in fin:
        if len( line ) < 3:
            continue
        if '#' == line[0]:
            continue
        lin = line.rstrip( '\n' ).rstrip( '\r' ).split( '\t' )
        if lin[3] == '':
            continue
        x = {}
        try:
            x['name'] = lin[9]
            x['rin'] = float( lin[1] )
            x['rout'] = float( lin[2] )
            x['length'] = float( lin[4] )
            x['material'] = lin[5]
            x['zcentre'] = float( lin[6] )
            x['zupstream'] = float( lin[7] )
            x['zdownstream'] = float( lin[8] )
            if lin[10] == 'yes':
                x['vacuum_inside'] = True
            else:
                x['vacuum_inside'] = False
            out.append( x )
        except ValueError:
            print 'ERROR'
            print lin
    return out


def main():
    tubs = read_tubs()
    z0 = 0.
    for i, a in enumerate(sys.argv):
        if a == 'z0':
            z0 = float( sys.argv[i+1] )
    print 'z0 = {}'.format( z0 )
    raw_input( '\nPress ENTER to continue, please.\n\n' )

    palette = [ 
                '75/255.,0/255.,130/255.,0.3',# indigo
                '173/255.,255/255.,47/255.,0.3',# greenyellow
                '199/255.,21/255.,133/255.,0.3',# mediumvioletred
                '85/255.,107/255.,47/255.,0.3',# darkolivegreen
                '255/255.,20/255.,147/255.,0.3',# deeppink
                '30/255.,144/255.,255/255.,0.3',# dodgerblue
                '147/255.,112/255.,219/255.,0.3',# mediumpurple
                '152/255.,251/255.,152/255.,0.3',# palegreen
                '221/255.,160/255.,211/255.,0.3',# plum
                '64/255.,224/255.,208/255.,0.3'# turquoise
                ]
    '''
                '240/255.,255/255.,240/255.,0.3',# honeydew
                '245/255.,255/255.,250/255.,0.3',# mintcream
                '240/255.,255/255.,255/255.,0.3']# azure
                '240/255.,248/255.,255/255.,0.3',# aliceblue
                '/255.,/255.,/255.,0.3',#
                '/255.,/255.,/255.,0.3',#
                '/255.,/255.,/255.,0.3',#
                '/255.,/255.,/255.,0.3',#
                '/255.,/255.,/255.,0.3',#
    '''

    print '\n' + '\033[92m' + '*'*10 + '  PCDetectorConstruction.cc  ' + '*'*10 + '\033[0m'
    raw_input( '\nPress ENTER to continue, please.\n\n' )
    for i, tub in enumerate(tubs):
        print """G4VSolid* {name}_solid = new G4Tubs("{name}", {rin}*mm, {rout}*mm, 0.5*{length}*mm, 0., 360.*degree);""".format(
                name = tub['name'], rin = tub['rin'], rout = tub['rout'], length=tub['length'] )
        print """{name}_logic = new G4LogicalVolume({name}_solid, {mat}, "{name}");""".format(
                name = tub['name'], mat = tub['material'] )
        print """{name}_logic->SetVisAttributes( G4VisAttributes(G4Colour({colour})) );""".format(
                name = tub['name'], colour=palette[i % len(palette)] )
        print """new G4PVPlacement(xRot, G4ThreeVector(0,{zcentre}*mm-zz00,0), {name}_logic, "{name}", world_logic, false, 0, checkOverlaps);""".format(
                name = tub['name'], zcentre = tub['zcentre']-z0 )
        if tub['vacuum_inside']:
            vacname = tub['name'] + '_vacuum'
            print """G4VSolid* {name}_solid = new G4Tubs("{name}", 0.*mm, {rout}*mm, 0.5*{length}*mm, 0., 360.*degree);""".format(
                    name = vacname, rout = tub['rin'], length=tub['length'] )
            print """{name}_logic = new G4LogicalVolume({name}_solid, {mat}, "{name}");""".format(
                    name = vacname, mat = 'vacuum' )
            print """{name}_logic->SetVisAttributes( G4VisAttributes(G4Colour({colour})) );""".format(
                    name = vacname, colour='240/255.,255/255.,255/255.,0.3' )# azure
            print """new G4PVPlacement(xRot, G4ThreeVector(0,{zcentre}*mm-zz00,0), {name}_logic, "{name}", world_logic, false, 0, checkOverlaps);""".format(
                    name = vacname, zcentre = tub['zcentre']-z0 )
        print

    print '\n' + '\033[92m' + '*'*10 + '  PCDetectorConstruction.hh  ' + '*'*10 + '\033[0m'
    raw_input( '\nPress ENTER to continue, please.\n\n' )
    for tub in tubs:
        print """G4LogicalVolume* {name}_logic;""".format( name = tub['name'] )
        if tub['vacuum_inside']:
            vacname = tub['name'] + '_vacuum'
            print """G4LogicalVolume* {name}_logic;""".format( name = vacname )


if __name__ == '__main__':
    main()
