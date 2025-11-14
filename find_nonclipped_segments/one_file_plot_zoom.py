#!/bin/env python
import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from obspy import UTCDateTime

#==========================================================================

def file_exist(file):
    """Check if a file (with full path) exists"""
    if not os.path.isfile(file):
        print("File:", file, "does not exist. Bailing out ...")
        exit()

def read_seismogram(filename):
    file_exist(filename)
    S_tvec, S_vvec, S_fvec = [], [], []
    with open(filename, 'r') as infile:
        line1 = infile.readline()
        words = line1.split()
        deltat = float(words[2])
        st = UTCDateTime(words[1])
        channel = words[5]
        for line in infile:
            words = line.split()
            x = float(words[0])
            y = float(words[1])
            z = float(words[2])
            S_tvec.append(st + x * deltat)
            S_vvec.append(y)
            S_fvec.append(z)
    return S_tvec, S_vvec, S_fvec, channel

def generate_segment_indices(S_fvec):
    smallval = 0.01
    length = len(S_fvec)
    lastn = length - 1
    intstart, intmemb, intflag = [], [], []
    istart = 0
    nummemb = 0
    currflag = S_fvec[istart]
    for i in range(length):
        newflag = S_fvec[i]
        if abs(newflag - currflag) > smallval:
            intstart.append(istart)
            intmemb.append(nummemb)
            intflag.append(currflag)
            istart = i
            nummemb = 0
        else:
            nummemb += 1
        if i == lastn:
            intstart.append(istart)
            intmemb.append(nummemb)
            intflag.append(currflag)
        currflag = newflag
    return intstart, intmemb, intflag

if __name__ == "__main__":
    MINSAMPLES = 600
    filename = sys.argv[1]
    bn = os.path.basename(filename)

    X, Y, Z, channel = read_seismogram(filename)
    intstart, intmemb, intflag = generate_segment_indices(Z)

    Xarr = np.array(X)
    Yarr = np.array(Y)
    Zarr = np.array(Z)
    deltat = Xarr[1] - Xarr[0]

    numsegments = len(intstart)
    fig, ax = plt.subplots(1)
    ax.xaxis_date()
    plt.title(bn)

    ymin, ymax = 20000.0, -20000.0
    for iseg in range(numsegments):
        istart = intstart[iseg]
        iend = istart + intmemb[iseg]
        tarr = matplotlib.dates.date2num(Xarr[istart:iend])
        try:
            segmin = np.min(Yarr[istart:iend])
            if segmin < ymin:
                ymin = segmin
        except:
            pass
        try:
            segmax = np.max(Yarr[istart:iend])
            if segmax > ymax:
                ymax = segmax
        except:
            pass
        try:
            plt.plot(tarr, Yarr[istart:iend])
        except:
            pass

    fig.autofmt_xdate()
    plotdir = 'plots'
    os.makedirs(plotdir, exist_ok=True)
    pngfile = os.path.join(plotdir, bn + '.png')
    pdffile = os.path.join(plotdir, bn + '.pdf')

    print("\n>>> Zoom in on the plot as desired, then close the window to export visible data.\n")
    plt.show()

    plt.savefig(pngfile)
    plt.savefig(pdffile)

    xlvalues = ax.get_xlim()
    xleft, xright = xlvalues[0], xlvalues[1]

    outdir = 'outfiles'
    os.makedirs(outdir, exist_ok=True)

    for iseg in range(numsegments):
        istart = intstart[iseg]
        iend = istart + intmemb[iseg]
        tarr = matplotlib.dates.date2num(Xarr[istart:iend])
        narr = Yarr[istart:iend]
        indices = np.where(np.logical_and(tarr >= xleft, tarr <= xright))[0]
        numgood = len(indices)
        if numgood > MINSAMPLES:
            fileout = os.path.join(outdir, bn + "_seg" + "{:08d}".format(iseg))
            with open(fileout, "w") as f:
                for i in range(numgood):
                    sy = narr[indices[i]]
                    line = "{:.6f}".format(sy).rjust(14) + "\n"
                    f.write(line)


