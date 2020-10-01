#! /usr/bin/env python3                                                                             

import argparse
import os
import yaml
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(
         description='Calculates average (dos-weighted) spring constants')
parser.add_argument('-d', '--dos', metavar='dospath',
                    default='partial_dos.dat',
                    help='path to Phonopy (partial_dos_).dat')
parser.add_argument('-n', '--atomnum', metavar='number of atoms', nargs='+', type=int,
                   default='',
                   help='number of atoms of each species in the structure')
parser.add_argument('-m', '--masses', metavar='mass of atom', nargs='+', type=float,
                     default='',
                     help='mass of each atom in the structure in dalton/unified atomic mass')
parser.add_argument('--atomlab', metavar='labels for atoms', nargs='+',
                    default='',
                    help='labels for each atomic species/element symbol')
args = parser.parse_args()



def avg_spring_constant(dosfile, atomnum, masses, labels):
  """Calculates average spring constant for each atom (DoS weighted).
  Args:
      dosfile (:obj:'str'): Path to a Phonopy (projected_).dat.
      atomnum (:obj:'int'): Number of atoms of each atomic species.
      labels(:obj:'str'): Atom labels.
  Returns:
      :obj:'list': List with atom labels and their average spring constants.
  """

  data = np.loadtxt(dosfile)
  freq = data[:,0]
  pDoS = data[:,1:]

  # Total averaged frequency

  total = pDoS.sum(axis=1)  # Total projected DoS
  tot_avg_freq = (freq * total).sum() / total.sum() 

  # Average frequency per atom
  
  avg_freq_atoms = []
  iatom = 0
  for i in atomnum:
      atom_DoS = pDoS[:,iatom:i+iatom].sum(axis=1)
      avg_freq_atoms.append((freq * atom_DoS).sum() / atom_DoS.sum())
      iatom += i
 
  # Average spring constant per atom

  avg_spring_atoms = [i**2 * j * 1.66054e-27 for i, j in zip(avg_freq_atoms, masses)]
  
  # Total averaged spring constant

  tot_avg_spring_constant = np.mean(avg_spring_atoms)

  avg_spring_constants = {i:float("{:.5g}".format(j)) for i, j in zip(labels, avg_spring_atoms)}
  avg_spring_constants['tot'] = float("{:.5g}".format(tot_avg_spring_constant))

  return avg_spring_constants

print("avg_spring_constant:", avg_spring_constant(args.dos, args.atomnum, args.masses, args.atomlab))

