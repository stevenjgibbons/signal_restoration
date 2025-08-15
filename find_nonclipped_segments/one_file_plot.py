#!/bin/env python
import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from obspy import UTCDateTime
from datetime import datetime

#==========================================================================
def file_exist(file):
    """Check if a file (with full path) exist"""
    if not os.path.isfile(file):
        print("File: ",file," does not exist. Bailing out ...")
        exit()

def read_seismogram( filename ):
    file_exist( filename )
    S_tvec  = []
    S_vvec  = []
    S_fvec  = []
    infile  = open( filename, 'r' )
    line1   = infile.readline()
    words   = line1.split()
    deltat  = float( words[2] )
    st      = UTCDateTime( words[1] )
    channel = words[ 5 ]
    for line in infile:
        words = line.split()
        x     = float( words[0] )
        y     = float( words[1] )
        z     = float( words[2] )
        S_tvec.append( st + x*deltat )
        S_vvec.append( y )
        S_fvec.append( z )
    return S_tvec, S_vvec, S_fvec, channel

#
#   Want to generate two lists:
#   intstart, intmemb
#   which contain the starting sample of each segment
#   and the number of members of each segment respectively
#
def generate_segment_indices( S_fvec ):
    smallval = 0.01
    length   = len( S_fvec )
    lastn    = length - 1
    intstart = []
    intmemb  = []
    intflag  = []
    istart   = 0
    nummemb  = 0
    currflag = S_fvec[istart]
    for i in range(length):
        newflag = S_fvec[i]
        print ( i, newflag, currflag )
        if ( abs( newflag - currflag ) > smallval ):
            intstart.append( istart )
            intmemb.append( nummemb )
            intflag.append( currflag )
            istart  = i
            nummemb = 0
        else:
            nummemb += 1
            if i == lastn:
                intstart.append( istart )
                intmemb.append( nummemb )
                intflag.append( currflag )
        currflag = newflag

    return intstart, intmemb, intflag
                

if __name__ == "__main__":
    print("Hello, World!")
    #
    # We don't want any segments that are less than 15 seconds long.
    # I want to have at least 40 seconds sampling and 10 second segments.
    # So 15*40 = 600
    #
    MINSAMPLES = 600
    #
    filename = sys.argv[1]
    # filename = '/data_large/stg/PAPERS/CLIPPING_WORK/BRVK_archive/ASCII_ARCHIVE/730216.0503.brvk.KODB.SHZ0.030.txt'
    bn = os.path.basename( filename )
    X, Y, Z, channel = read_seismogram( filename )
    intstart, intmemb, intflag = generate_segment_indices( Z )
    Xarr = np.array( X )
    Yarr = np.array( Y )
    Zarr = np.array( Z )
    deltat = Xarr[1]-Xarr[0]
    print ( Xarr[0], Yarr[0] )
    print ( Xarr[1], Yarr[1] )
    # Plot as a time series plot
    numsegments = len( intstart )
    print ("numsegments = ", numsegments )
    fig, ax = plt.subplots(1)
    ax.xaxis_date()
    plt.title(bn)
    ymin =  20000.0
    ymax = -20000.0
    for iseg in range( numsegments ):
        istart  = intstart[iseg]
        nummemb = intmemb[iseg]
        iflag   = intflag[iseg]
        iend    = istart + nummemb
        if abs( iflag ) < 0.1:
            print ("Segment ", iseg, " flag ", iflag )
            print ("start ", istart, " end ", iend )
            tarr = matplotlib.dates.date2num( Xarr[istart:iend] )
            print ("tarr" , tarr )
            try:
                segmin = np.min( Yarr[istart:iend] )
                if segmin < ymin:
                    ymin = segmin
            except:
                pass
            try:
                segmax = np.max( Yarr[istart:iend] )
                if segmax > ymax:
                    ymax = segmax
            except:
                pass
            try:
                plt.plot( tarr, Yarr[istart:iend] )
            except:
                pass

    for iseg in range( numsegments ):
        istart  = intstart[iseg]
        nummemb = intmemb[iseg]
        iflag   = intflag[iseg]
        iend    = istart + nummemb
        if abs( iflag+1.0 ) < 0.1:
            print ("Segment ", iseg, " flag ", iflag )
            print ("start ", istart, " end ", iend )
            Xlist = []
            Xlist.append( Xarr[istart] - deltat*0.5 )
            Xlist.append( Xarr[iend]   + deltat*0.5 )
            tarr = matplotlib.dates.date2num( Xlist )
            xpoly = []
            ypoly = []
            print ("tarr" , tarr )
            xpoly.append( tarr[0] )
            ypoly.append( 0.0     )
            xpoly.append( tarr[1] )
            ypoly.append( 0.0     )
            xpoly.append( tarr[1] )
            ypoly.append( ymin * 1.2     )
            xpoly.append( tarr[0] )
            ypoly.append( ymin * 1.2     )
            #xpoly[0] = tarr[0]
            #xpoly[1] = tarr[nummemb-1]
            #xpoly[2] = tarr[nummemb-1]
            #xpoly[3] = tarr[0]
            #ypoly[0] = 0.0
            #ypoly[1] = 0.0
            #ypoly[2] = ymin * 1.2
            #ypoly[3] = ymin * 1.2 
            ax.fill( xpoly, ypoly, "b" )
            plt.plot( xpoly, ypoly, "b" )
        if abs( iflag-1.0 ) < 0.1:
            print ("Segment ", iseg, " flag ", iflag )
            print ("start ", istart, " end ", iend )
            Xlist = []
            Xlist.append( Xarr[istart] - deltat*0.5 )
            Xlist.append( Xarr[iend]   + deltat*0.5 )
            tarr = matplotlib.dates.date2num( Xlist )
            xpoly = []
            ypoly = []
            print ("tarr" , tarr )
            xpoly.append( tarr[0] )
            ypoly.append( 0.0     )
            xpoly.append( tarr[1] )
            ypoly.append( 0.0     )
            xpoly.append( tarr[1] )
            ypoly.append( ymax * 1.2     )
            xpoly.append( tarr[0] )
            ypoly.append( ymax * 1.2     )
            # print ( xpoly[0] )
            # print ( tarr[0] )
            # xpoly[0] = tarr[0]
            # xpoly[1] = tarr[nummemb-1]
            # xpoly[2] = tarr[nummemb-1]
            # xpoly[3] = tarr[0]
            # ypoly[0] = 0.0
            # ypoly[1] = 0.0
            # ypoly[2] = ymax * 1.2
            # ypoly[3] = ymax * 1.2 
            ax.fill( xpoly, ypoly, "r" )
            plt.plot( xpoly, ypoly, "r" )

    fig.autofmt_xdate()
    # plt.plot_date( tarr, Yarr, linewidth=1, c='black' )
    plotdir = 'plots'
    pngfile = plotdir + '/' + bn + '.png'
    pdffile = plotdir + '/' + bn + '.pdf'
    # plt.show() 
    plt.savefig( pngfile ) 
    plt.savefig( pdffile ) 
    axes = plt.gca()
    xlvalues = ax.get_xlim()
    xleft    = xlvalues[0]
    xright   = xlvalues[1]
    print( "axes = ", axes )
    print( "xlvalues = ", xlvalues )

    for iseg in range( numsegments ):
        istart  = intstart[iseg]
        nummemb = intmemb[iseg]
        iflag   = intflag[iseg]
        iend    = istart + nummemb
        print ("ISEG ", iseg, istart, iend )
        if abs( iflag+1.0 ) > 0.1:
            Write   = True
            tarr = matplotlib.dates.date2num( Xarr[istart:iend] )
            narr =                            Yarr[istart:iend]
            print (tarr)
            print (len(tarr))
            indices = np.where(np.logical_and(tarr>=xleft, tarr<=xright))[0]
            print (indices)
            numgood = len(indices)
            print ("numgood ", numgood )
            if numgood > MINSAMPLES:
                outdir = 'outfiles'
                fileout = outdir + '/' + bn + "seg" + "{:08d}".format(iseg)
                exists = os.path.isfile( fileout )
                if exists:
                    os.remove( fileout )
                f = open( fileout, "w" )
                for i in range(numgood):
                    print (i, tarr[ indices[i] ], narr[ indices[i] ] )
                    sy = narr[ indices[i] ]
                    line="{:.6f}".format( sy ).rjust(14) + "\n"
                    f.write( line )
                f.close()
