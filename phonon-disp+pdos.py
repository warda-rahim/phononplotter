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
parser.add_argument('-b', '--band', metavar='bandpath',
                    default='band.yaml',
                    help='path to Phonopy (band_).yaml')
parser.add_argument('--bandcolour', metavar='Band colour', 
                    default='#5A8D03',
                    help='colour for the phonon band structure')
parser.add_argument('--linestyle', metavar='line style', 
                    default='-',
                    help='linestyle for phonon dispersion')
parser.add_argument('-d', '--dos', metavar='dospath',
                    default='partial_dos.dat',
                    help='path to Phonopy (partial_dos_).dat')
parser.add_argument('-n', '--atomnum', metavar='number of atoms', nargs='+', type=int,
                   default='',
                   help='number of atoms of each species in the structure')
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


with open(args.band, 'r') as f:
    data = yaml.safe_load(f)

dists = []
eigenvalues = []
dists.append([i['distance'] for i in data['phonon']])
for point in data['phonon']:
    eigenvalues.append([e['frequency'] for e in point['band']])


def add_band(axis, bandfile, colour, linestyle):
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


    #with open(bandfile, 'r') as f:
     #   data = yaml.safe_load(f)

    #dists = []
    #eigenvalues = []
    #dists.append([i['distance'] for i in data['phonon']])
    #for point in data['phonon']:
     #   eigenvalues.append([e['frequency'] for e in point['band']])

    l = []
    p = []
    try:
        for i in data['phonon']:
            if 'label' in i:
                l.append(i['label'])
                p.append(i['distance'])
            if len(l) == 0:
                raise Exception
    except:
        for i, j in data['labels']:
            l.append(i)
            if len(l) == len(data['labels']):
                l.append(j)
   
    step = data['segment_nqpoint'][0]
    for i in range(0, len(dists[0]), step-1):
        p.append(dists[0][i])
    
    l = [r'$\Gamma$' if x=='G' else x for x in l]

    plt.xticks(p, l)
    axis.xaxis.set_minor_locator(mpl.ticker.NullLocator())
    axis.set_xlim(0, p[-1])
    axis.set_ylim(bottom=0, top=1.05 * np.max(eigenvalues))

    axis.tick_params(axis='x', pad=15)
    axis.tick_params(axis='y', pad=15)

    axis.set_ylabel('Frequency (THz)', fontsize=50)
    
    try:
        colormap = plt.cm.get_colormap(colours[0])
        colours =  colormap(np.linspace(0, 1, 5))
    except Exception:
        pass

    axis.plot(dists[0], eigenvalues, linewidth=2.5, color=colour, linestyle=linestyle) 


    axis.axhline(linewidth=2, color='black', linestyle='--')
    for x in p:
        axis.axvline(x=x, linewidth=2, color='black')

    return axis


def add_dos(axis, dosfile, atomnum, colours, labels):
  """Adds a phonon density of states curve to the plot.
  Args:
      axis (:obj:'matplotlib.pyplot'): Axis to plot on.
      dosfile (:obj:'str'): Path to a Phonopy (projected_).dat.
      colour(:obj:'list'): Line colour.
  Returns:
      :obj:'matplotlib.pyplot': Axis with Phonon Dispersion.
  """

  data = np.loadtxt(dosfile)

  y = []
  y.extend([] for i in range(len(atomnum)))

  data2 = data[:,1:]
  for i, j in enumerate(atomnum):
      if j > 1:
          y[i].extend([sum(data2[:,k] for k in range(j))])
      data2 = data2[:,j:]

  axis.set_xticks([])
  axis.set_yticks([])
  axis.set_ylim(bottom=0, top=1.05 * np.max(eigenvalues))

  for i in range(len(y)):
      axis.plot(y[i][0], data[:,0], color=colours[i], label=labels[i], linestyle='-')

  return axis



import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from os.path import isfile
from matplotlib.gridspec import GridSpec
from cycler import cycler

plt.style.use("pretty2")

mpl.rcParams['axes.linewidth'] = 2

fig = plt.figure(figsize=(16, 12))

gs = GridSpec(1, 4, wspace=0)
ax1 = fig.add_subplot(gs[:,:-1])
ax1 = add_band(ax1, args.band, args.bandcolour, args.linestyle)
ax2 = fig.add_subplot(gs[:,-1])
ax2 = add_dos(ax2, args.dos, args.atomnum, args.doscolours, args.doslabels)

legend2 = ax2.legend(loc='upper left', bbox_to_anchor=(0.84,1.05))

plt.subplots_adjust(left = 0.12, right = 0.82, top  = 0.97, bottom = 0.1)

plt.savefig('phonon+pdos{}.pdf'.format(args.output) if args.output is not None else 'phonon+pdos.pdf')
plt.savefig('phonon+pdos{}.png'.format(args.output) if args.output is not None else 'phonon+pdos.png')
