#! /usr/bin/env python3                                                                             

import argparse
import os
import yaml
import pandas as pd

parser = argparse.ArgumentParser(
         description='Plots phonon dispersion and/or phonon density of states')
parser.add_argument('-d', '--dos', metavar='dospath',
                    default='partial_dos.dat',
                    help='path to Phonopy (partial_dos_).dat')
parser.add_argument('-n', '--atomnum', metavar='number of atoms', nargs='+', type=int,
                   default='',
                   help='number of atoms of each species in the structure')
parser.add_argument('--doscolours', metavar='Dos colours', nargs='+',
                    default=['#000000', '#5A8D03', '#E75480', '#FF6600', '#3C1361'],
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
 
  for i in range(len(y)):
      axis.plot(data[:,0], y[i][0], color=colours[i], label=labels[i], linestyle='-')

  return axis


import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from os.path import isfile
from matplotlib.gridspec import GridSpec
from cycler import cycler

plt.style.use("pretty2")

mpl.rcParams['axes.linewidth'] = 2

fig, ax = plt.subplots(figsize=(12.6, 12))
plt.subplots_adjust(left = 0.1, right = 0.95, top  = 0.97, bottom = 0.13)

ax = add_dos(ax, args.dos, args.atomnum, args.doscolours, args.doslabels)

legend = ax.legend(loc='upper left', bbox_to_anchor=(0.68,1.05))

ax.tick_params(axis='x', pad=15)
ax.tick_params(axis='y', pad=15)

ax.set_yticks([])
ax.set_xlabel('Frequency (THz)', fontsize=50)
ax.set_ylabel('pDoS', fontsize=50)
 
plt.savefig('dos{}.pdf'.format(args.output) if args.output is not None else 'dos.pdf')
plt.savefig('dos{}.png'.format(args.output) if args.output is not None else 'dos.png')
