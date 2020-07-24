#! /usr/bin/env python3                                                                                                           

import argparse
import os
import yaml
import pandas as pd

parser = argparse.ArgumentParser(
         description='Plots phonon dispersion and/or phonon density of states')
#parser.add_argument('-b', '--band', metavar='bandpath',
#                    default=os.getcwd(),
#                    help='path to Phonopy (band_).yaml')
parser.add_argument('-b', '--band', metavar='bandpath', nargs='+',
                    default='band.yaml',
                    help='path to Phonopy (band_).yaml')
parser.add_argument('-d', '--dos', metavar='dospath', nargs='+',
                    default='partial_dos.dat',
                    help='path to Phonopy (partial_dos_).dat')
parser.add_argument('--bandcolours', metavar='Band colours', nargs='+',
                    default=['#5A8D03', '#E75480', '#FF6600'],
                    help='colours for the band')
parser.add_argument('--bandlabels', metavar='legend labels for bands', nargs='+',
                    default=['2x2x2', '3x3x3', '4x4x4'],
                    help='legend labels for phonon dispersions for different supercells')
parser.add_argument('--linestyles', metavar='line styles', nargs='+', 
                    default=['-', '--', '-.'],
                    help='linestyles for phonon dispersions for different supercells')
parser.add_argument('--doscolours', metavar='Dos colours', nargs='+',
                    default=['#5A8D03', '#E75480', '#FF6600'],
                    help='colours for the pDoS')
parser.add_argument('--doslabels', metavar='legend labels for dos', nargs='+',
                    default='',
                    help='legend labels for phonon density of states plot')
parser.add_argument('-o', '--output', metavar='output file suffix',
                    default='',
                    help='suffix to add at the end of output file')
parser.add_argument('--style', metavar='style sheet', nargs='+',
                    default=[],
                    help='style sheets to use. Later ones will \
                          override earlier ones if they conflict.')
args = parser.parse_args()


def add_band(axis, bandfiles, colours, labels, linestyles):
    """Adds a phonon dispersion curve to the plot.

    Args:
        axis (:obj:'matplotlib.pyplot'): Axis to plot on.
        bandfile (:obj:'str'): Path to a Phonopy (band_).yaml.
        colour(:obj:'list'): Line colour.
        labels(:obj:'list'): Legend labels.
        linestyles(:obj:'list'): Line styles.

    Returns:
        :obj:'matplotlib.pyplot': Axis with Phonon Dispersion.
    """

    #bandfiles = []

    #for root, dir, files in os.walk(path):
        #for name in files:
            #if name.endswith('yaml'):
                #bandfiles.append(name)


    data = []
    for i in bandfiles:
        with open(i, 'r') as f:
            data.append(yaml.safe_load(f))

    dists = []
    eigenvalues = []
    dists.append([i['distance'] for i in data[0]['phonon']])
    for i in range(len(data)):
        x = []
        for point in data[i]['phonon']:
            x.append([e['frequency'] for e in point['band']])
        eigenvalues.append(x)


    l = []
    p = []
    try:
        for i in data[0]['phonon']:
            if 'label' in i:
                l.append(i['label'])
                p.append(i['distance'])
            if len(l) == 0:
                raise Exception
        
    except:
        for i, j in data[0]['labels']:
            l.append(i)
            if len(l) == len(data[0]['labels']):
                l.append(j)
       
        step = data[0]['segment_nqpoint'][0]
        for i in range(0, len(dists[0]), step-1):
            p.append(dists[0][i])
    
    l = [r'$\Gamma$' if x=='G' else x for x in l]

   
    plt.xticks(p, l)
    axis.xaxis.set_minor_locator(mpl.ticker.NullLocator())
    axis.set_xlim(0, p[-1])
    #axis.set_ylim(bottom=0, top=1.05 * np.max(eigenvalues))

    axis.tick_params(axis='x', pad=15)
    axis.tick_params(axis='y', pad=15)

    axis.set_ylabel('Frequency (THz)', fontsize=50)
    
    try:
        colormap = plt.cm.get_colormap(colours[0])
        colours =  colormap(np.linspace(0, 1, 5))
    except Exception:
        pass


    if len(bandfiles) > 1:
       if len(bandfiles) > 3:
          colours.extend([colours[0] for i in range(len(bandfiles)-3)])
          linestyles.extend([linestyles[0] for i in range(len(bandfiles)-3)])

       for i in range(len(bandfiles)):
           axis.plot(dists[0], eigenvalues[i], linewidth=2.5, label=labels[i], color=colours[i], linestyle=linestyles[i])
    else:
        axis.plot(dists[0], eigenvalues[0], linewidth=2.5, color=colours[0]) 


    axis.axhline(linewidth=2, color='black', linestyle='--')
    for x in p:
        axis.axvline(x=x, linewidth=2, color='black')

    return axis



import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from os.path import isfile
from matplotlib.gridspec import GridSpec
from cycler import cycler

plt.style.use("pretty2")

mpl.rcParams['axes.linewidth'] = 2

if len(args.band) > 1:
    fig, ax = plt.subplots(figsize=(16, 12))
    plt.subplots_adjust(left = 0.12, right = 0.8, top  = 0.97, bottom = 0.1)
else:
    fig, ax = plt.subplots(figsize=(12.6, 12))
    plt.subplots_adjust(left = 0.15, right = 0.95, top  = 0.97, bottom = 0.1)


ax = add_band(ax, args.band, args.bandcolours, args.bandlabels, args.linestyles)

if args.bandlabels is not None:
    legend = ax.legend()
    handles, tags = ax.get_legend_handles_labels()
    handle = []
    tag = []
    for i in range(len(tags)):
        if tags[i] not in tag:
            handle.append(handles[i])
            tag.append(tags[i])
    legend = ax.legend(handle, tag, frameon=False, prop={'size': 36}, loc='upper left', bbox_to_anchor=(0.98,0.95))


plt.savefig('phonon{}.pdf'.format(args.output) if args.output is not None else 'phonon.pdf')
plt.savefig('phonon{}.png'.format(args.output) if args.output is not None else 'phonon.png')
