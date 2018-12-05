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
import cProfile


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
    if '-b' in sys.argv:
        c1.SetWindowSize(cw + (cw - c1.GetWw()), ch + (ch - c1.GetWh()));
    else:
        c1.SetCanvasSize(cw, ch)
    return c1


def mypol1(xx, pp):
    x = xx[0]
    antixmin = pp[0]
    antixmax = pp[1]
    if antixmin < x and x < antixmax:
        r.TF1.RejectPoint()
        # return 0.
    c0 = pp[2]
    c1 = pp[3]
    return c0 + c1*x

def tune_hp( hpx, hpy ):
    hpy.GetXaxis().SetRangeUser(0, 1190)
    hpx.SetTitle( 'hpx' )
    hpy.SetTitle( 'hpy' )
    hpx.GetXaxis().SetTitle( 'Horizontal axis, pixels' )
    hpx.GetYaxis().SetTitle( 'Amplitude, CCD counts' )
    hpy.GetXaxis().SetTitle( 'Vertical axis, pixels' )
    hpy.GetYaxis().SetTitle( 'Amplitude, CCD counts' )
    hpy.GetXaxis().SetTitleOffset( 1.3 )
    hpy.GetYaxis().SetTitleOffset( 1.3 )
    hpx.GetXaxis().SetTitleOffset( 1.3 )
    hpx.GetYaxis().SetTitleOffset( 1.3 )


def read_positron_table():
    # fin = open( 'positron_table.txt' )
    fin = open( 'positron_table.tsv' )
    out = {}
    for line in fin:
        if len(line) < 4:
            continue
        if line[0] == '#':
            continue
        # lin = line.split()
        lin = line.rstrip('\n').split('\t')
        if len(lin) < 25:
            continue
        out[ lin[0] ] = {}
        out[ lin[0] ]['shift'] = lin[1]
        out[ lin[0] ]['comment'] = lin[2]
        out[ lin[0] ]['start_time'] = lin[3]
        out[ lin[0] ]['end_time'] = lin[4]
        out[ lin[0] ]['target'] = lin[5]
        if '3um' in out[ lin[0] ]['target']:
            out[ lin[0] ]['thickness'] = 3.e-6
        elif '4.82um' in out[ lin[0] ]['target']:
            out[ lin[0] ]['thickness'] = 4.82e-6
        elif '5um' in out[ lin[0] ]['target']:
            out[ lin[0] ]['thickness'] = 5.e-6
        elif '2.19mm' in out[ lin[0] ]['target']:
            out[ lin[0] ]['thickness'] = 2.19e-3
        elif '1.37' in out[ lin[0] ]['target']:
            out[ lin[0] ]['thickness'] = 1.37e-3
        else:
            out[ lin[0] ]['thickness'] = -1.
        out[ lin[0] ]['mirror'] = lin[6]
        out[ lin[0] ]['texp_min'] = lin[7]
        out[ lin[0] ]['texp_sec'] = lin[8]
        out[ lin[0] ]['npic'] = lin[9]
        out[ lin[0] ]['slit'] = lin[10]
        #
        out[ lin[0] ]['npulse'] = lin[24]
        out[ lin[0] ]['nclock'] = lin[23]
    return out


def read_log():
    fin = open( 'robust_signal_log.txt' )
    out = {}
    for line in fin:
        if len(line) < 4:
            continue
        if line[0] == '#':
            continue
        lin = line.split()
        out[ lin[0] ] = {}
        out[ lin[0] ]['centre_x'] = float(lin[1])
        out[ lin[0] ]['centre_y'] = float(lin[2])
        out[ lin[0] ]['signal_a'] = float(lin[3])
        out[ lin[0] ]['signal_b'] = float(lin[4])
        out[ lin[0] ]['bkg_a'] = float(lin[5])
        out[ lin[0] ]['bkg_b'] = float(lin[6])
        out[ lin[0] ]['bkg_A'] = float(lin[7])
        out[ lin[0] ]['bkg_B'] = float(lin[8])
    return out


def within_ellipse( x, y, x0, y0, rx, ry ):
    a = ((x-x0)/rx)**2
    a += ((y-y0)/ry)**2
    if a <= 1:
        return True
    else:
        return False

def within_signal_ellipse( log, x, y ):
    return within_ellipse(x, y, log['centre_x'], log['centre_y'], log['bkg_a'], log['bkg_b'])


def integ_signal_area( hh, log ):
    return integ_ellipse( hh, log['centre_x'], log['centre_y'], log['signal_a'], log['signal_b'] )

def integ_bkg_area( hh, log ):
    res = integ_ring( hh, log['centre_x'], log['centre_y'], log['bkg_a'], log['bkg_b'],
            log['bkg_A'], log['bkg_B'] )
    return res
    '''
    res1 = integ_ellipse( hh, log['centre_x'], log['centre_y'], log['bkg_a'], log['bkg_b'] )
    res2 = integ_ellipse( hh, log['centre_x'], log['centre_y'], log['bkg_A'], log['bkg_B'] )
    return [res2[0]-res1[0], res2[1]-res1[1],
            min([res2[2], res1[2]]), max([res2[3], res1[3]]) ]
    '''

def integ_ellipse( hh, x0, y0, rx, ry ):
    ax = hh.GetXaxis()
    ay = hh.GetYaxis()
    res = 0.
    n = 0
    mi = hh.GetBinContent( ax.FindBin(x0), ax.FindBin(y0) )
    ma = mi
    for i in xrange(1, 1601):
        x = ax.GetBinCenter(i)
        if x < x0-rx or x > x0+rx:
            continue
        for j in xrange(1, 1201):
            y = ay.GetBinCenter(j)
            if y < y0-ry or y > y0+ry:
                continue
            if within_ellipse( x, y, x0, y0, rx, ry ):
                bc = hh.GetBinContent( i, j )
                # bc = hh[ j*1602+i ]
                res += bc
                n += 1
                if bc < mi:
                    mi = bc
                if bc > ma:
                    ma = bc
    return [res, n, mi, ma]

def integ_ring( hh, x0, y0, rx, ry, Rx, Ry ):
    ax = hh.GetXaxis()
    ay = hh.GetYaxis()
    res = 0.
    n = 0
    mi = hh.GetBinContent( ax.FindBin(x0), ax.FindBin(y0) )
    ma = mi
    for i in xrange(1, 1601):
        # x = ax.GetBinCenter(i)
        # print 'i {}   x {}'.format(i, x)
        x = i - .5
        if x < x0-Rx or x > x0+Rx:
            continue
        for j in xrange(1, 1201):
            # y = ay.GetBinCenter(j)
            # print 'j {}   y {}'.format(j, y)
            y = j - .5
            if y < y0-Ry or y > y0+Ry:
                continue
            if within_ellipse( x, y, x0, y0, Rx, Ry ) and not within_ellipse( x, y, x0, y0, rx, ry ):
                bc = hh.GetBinContent( i, j )
                # bc = hh[ j*1602+i ]
                res += bc
                n += 1
                if bc < mi:
                    mi = bc
                if bc > ma:
                    ma = bc
    return [res, n, mi, ma]


def main_2d(finname, isDraw=True):
    print 'finname', finname
    run = finname.split('/')[-1].split('.')[0]
    logs = read_log()
    if run in logs:
        log = logs[run]
    else:
        print WARNING
        print 'main_2d : there is no log for {}.'.format( run )
        print ENDC
        return 1
    Fin = r.TFile( finname )
    hh = Fin.Get( 't1' )
    print 'hh', hh
    ###
    Sraw = integ_signal_area( hh, log )
    bkg = integ_bkg_area( hh, log )
    print 'S', Sraw
    print 'bkg', bkg
    S = Sraw[0] - Sraw[1]*bkg[0]/bkg[1]
    print 'true S', S
    ###
    rebin = 4
    ###
    if isDraw:
        c1 = getCanvas( 'c1', 800, 800 )
        c1.SetGrid()
        hh.Rebin2D( rebin, rebin )
        hh.Draw( 'colz' )
        # hh.GetZaxis().SetRangeUser( bkg[2], rebin*max([bkg[3], Sraw[3]]) )
        ztop = hh.GetBinContent( hh.GetXaxis().FindBin(log['centre_x']), hh.GetYaxis().FindBin(log['centre_y']) )
        zbot = hh.GetBinContent( hh.GetXaxis().FindBin(log['centre_x']+log['bkg_a']), hh.GetYaxis().FindBin(log['centre_y']) )
        zz = [ztop, zbot]
        ztop = max(zz)
        zbot = min(zz)
        zdel = ztop - zbot
        hh.GetZaxis().SetRangeUser( max([zbot*.75, zbot-.5*zdel]), ztop+zdel*.5 )
        # c1.SetLogz()
        line = r.TLine()
        line.SetLineColor( r.kCyan )
        line.DrawLine( log['centre_x']-25, log['centre_y'], log['centre_x']+25, log['centre_y'] )
        line.DrawLine( log['centre_x'], log['centre_y']-25, log['centre_x'], log['centre_y']+25 )
        ell = r.TEllipse()
        ell.SetFillStyle( 0 )
        ell.SetLineColor( r.kCyan )
        ell.DrawEllipse( log['centre_x'], log['centre_y'], log['signal_a'], log['signal_b'], 0, 360, 0 )
        ell.DrawEllipse( log['centre_x'], log['centre_y'], log['bkg_a'], log['bkg_b'], 0, 360, 0 )
        ell.DrawEllipse( log['centre_x'], log['centre_y'], log['bkg_A'], log['bkg_B'], 0, 360, 0 )
        c1.Update()
        if not '-b' in sys.argv:
            raw_input()
        if 'save' in sys.argv:
            c1.SaveAs( '/Users/liberulo/kek/csibpm/data/beamtest2017B/img/robust_signal_{}.png'.format(run) )
    ###
    Fin.Close()
    return { 'Sraw' : Sraw, 'S' : S, 'bkg' : bkg }


def main(finname, isDraw=True):
    log = read_log()
    r.gStyle.SetOptStat( 0 )
    r.TGaxis.SetMaxDigits( 3 )
    print finname
    run = finname.split('/')[-1].split('.')[0]
    Fin = r.TFile( finname )
    hh = Fin.Get( 't1' )
    hpx = hh.ProjectionX( 'hpx', 500, 1100 )
    hpy = hh.ProjectionY( 'hpy', 500, 1100 )
    tune_hp( hpx, hpy )
    ########
    axi, axa = 200, 1200
    fx = r.TF1( 'fx', mypol1, 100, 1600, 4 )
    fx.SetParameters( 200, 1200, 62e3, .1 )
    fx.FixParameter( 0, antixmin )
    fx.FixParameter( 1, antixmax )
    hpx.Fit( fx, 'r', 'goff' )
    parx = fx.GetParameters()
    bin1, bin2 = hpx.FindBin( axi ), hpx.FindBin( axa )
    sx = sum( list(hpx)[bin1:bin2+1] )
    print OKGREEN
    print 'x :  total sum  =  {:.4g} CCD counts'.format( sx )
    sx -= parx[2]*(axa-axi) + parx[3]/2. * (axa**2 - axi**2)
    print 'x :  total sum - offset  = {:.4g} CCD counts'.format( sx )
    sx *= 2.1
    print 'x :  total sum - offset  =  {:.4g} ph. e.'.format( sx )
    print ENDC
    #
    ayi, aya = 400, 1100
    fy = r.TF1( 'fy', mypol1, 100, 1180, 4 )
    fy.SetParameters( 200, 1200, 62e3, .1 )
    fy.FixParameter( 0, ayi )
    fy.FixParameter( 1, aya )
    hpy.Fit( fy, 'r', 'goff' )
    pary = fy.GetParameters()
    bin1, bin2 = hpy.FindBin( ayi ), hpy.FindBin( aya )
    sy = sum( list(hpy)[bin1:bin2+1] )
    print OKGREEN
    print 'y :  total sum  =  {:.4g} CCD counts'.format( sy )
    sy -= pary[2]*(aya-ayi) + pary[3]/2. * (aya**2 - ayi**2)
    print 'y :  total sum - offset  = {:.4g} CCD counts'.format( sy )
    sy *= 2.1
    print 'y :  total sum - offset  =  {:.4g} ph. e.'.format( sy )
    sy /= texp
    print 'y :  (total sum - offset)/texp  =  {:.4g} ph. e. / min'.format( sy )
    print ENDC
    ########
    if isDraw:
        c1 = getCanvas( 'c1', 1200, 600 )
        c1.Divide( 2, 1 )
        line = r.TLine()
        line.SetLineColor( r.kGreen+2 )
        line.SetLineStyle( 2 )
        lat = r.TLatex()
        lat.SetTextFont( 12 )
        lat.SetTextSize( .04 )
        #
        c1.cd( 1 )
        hpx.Draw()
        fx.Draw( 'same' )
        line.DrawLine( axi, hpx.GetMinimum(), axi, hpx.GetMaximum() )
        line.DrawLine( axa, hpx.GetMinimum(), axa, hpx.GetMaximum() )
        lat.DrawLatexNDC( .15, .85, r'S / #tau_{exp}'+'  =  {:.4g} ph. e.'.format(sx) )
        lat.DrawLatexNDC( .15, .80, r'#tau_{exp}  = '+' {:.1f} min'.format(texp) )
        #
        c1.cd( 2 )
        hpy.Draw()
        fy.Draw( 'same' )
        line.DrawLine( ayi, hpy.GetMinimum(), ayi, hpy.GetMaximum() )
        line.DrawLine( aya, hpy.GetMinimum(), aya, hpy.GetMaximum() )
        lat.DrawLatexNDC( .15, .85, r'S / #tau_{exp}'+'  =  {:.4g} ph. e.'.format(sy) )
        c1.Update()
        ans = raw_input()
        if ans == 'save':
            c1.SaveAs( '~/Downloads/diff_exp_time_{}_{}.png'.format(
                finname.split('/')[-3], finname.split('/')[-1].split('.')[0] ) )
    ########
    Fin.Close()
    return {'sx' : sx, 'sy' : sy}


def supmain():
    base = '/Users/liberulo/kek/csibpm/data/beamtest2017B/hp/'
    runs = ''
    inname = 'robust_signal_in_file_list_2.txt'
    innames = {'00' : 'robust_signal_in_file_list_r000x.txt',
            '10' : 'robust_signal_in_file_list_r001x.txt',
            '20' : 'robust_signal_in_file_list_r002x.txt',
            '30' : 'robust_signal_in_file_list_r003x.txt',
            '40' : 'robust_signal_in_file_list_r004x.txt',
            '50' : 'robust_signal_in_file_list_r005x.txt',
            'total' : 'robust_signal_in_file_list_total.txt'}
    for i, a in enumerate(sys.argv):
        if a == 'base':
            if 'hp' == sys.argv[i+1]:
                base = '/Users/liberulo/kek/csibpm/data/beamtest2017B/hp/'
            elif sys.argv in ['root', 'bpm_root']:
                base = '/Users/liberulo/kek/csibpm/data/beamtest2017B/BPM_ROOT/'
        elif a == 'runs':
            runs = sys.argv[i+1]
            if runs in innames:
                inname = innames[ runs ]
    fin = open( inname )
    file_names = []
    for line in fin:
        lin = line.rstrip('\n')
        file_names.append( base+lin )
    ###
    posi = read_positron_table()
    ###
    if len( runs ) > 0:
        Fout = r.TFile( '/Users/liberulo/kek/csibpm/data/beamtest2017B/robust_signal_{}.root'.format(runs), 'recreate' )
    else:
        Fout = r.TFile( '/Users/liberulo/kek/csibpm/data/beamtest2017B/robust_signal.root', 'recreate' )
    t = r.TTree( 't', 't' )
    S = np.zeros( 1 )
    Sraw = np.zeros( 2 )
    bkg = np.zeros( 2 )
    slit = np.zeros( 1 )
    texp = np.zeros( 1 )
    npulse = np.zeros( 1 )
    nclock = np.zeros( 1 )
    thickness = np.zeros( 1 )
    run = np.zeros( 1, dtype=int )
    subrun = np.zeros( 1, dtype=int )
    t.Branch( 'run', run, 'run/I' )
    t.Branch( 'subrun', subrun, 'subrun/I' )
    t.Branch( 'S', S, 'S/D' )
    t.Branch( 'Sraw', Sraw, 'Sraw[2]/D' )
    t.Branch( 'bkg', bkg, 'bkg[2]/D' )
    t.Branch( 'slit', slit, 'slit/D' )
    t.Branch( 'texp', texp, 'texp/D' )
    t.Branch( 'nclock', nclock, 'nclock/D' )
    t.Branch( 'npulse', npulse, 'npulse/D' )
    t.Branch( 'thickness', thickness, 'thickness/D' )
    ###
    for finname in file_names:
        res = main_2d( finname, isDraw=True )
        if res == 1:
            continue
        runsubrun = finname.split('/')[-1].split('.')[0][1:]
        if not runsubrun in posi:
            print WARNING
            print 'supmain : there is no {} in the positron table.'.format( runsubrun )
            print ENDC
            continue
        S[0] = res['S']
        Sraw[0] = res['Sraw'][0]
        Sraw[1] = res['Sraw'][1]
        bkg[0] = res['bkg'][0]
        bkg[1] = res['bkg'][1]
        run[0] = int( runsubrun.replace('r', '').split('_')[0] )
        subrun[0] = int( runsubrun.replace('r', '').split('_')[1] )
        try:
            slit[0] = float( posi[runsubrun]['slit'] )
            texp[0] = float( posi[runsubrun]['texp_sec'] )
            nclock[0] = float( posi[runsubrun]['nclock'] )
            npulse[0] = float( posi[runsubrun]['npulse'] )
            thickness[0] = float( posi[runsubrun]['thickness'] )
        except ValueError as e:
            print e
            for v in ['slit', 'texp_sec', 'nclock', 'npulse', 'thickness']:
                print FAIL, v, posi[runsubrun][v], ENDC
            continue
        t.Fill()
    ###
    c1 = getCanvas( 'c1' )
    t.Draw( 'S>>h(300)' )
    c1.Update()
    if not '-b' in sys.argv:
        raw_input()
    Fout.cd()
    t.Write()
    Fout.Close()


if __name__ == '__main__':
    print 'Hi!'
    if 'profile' in sys.argv:
        cProfile.run( 'supmain()' )
    else:
        supmain()
