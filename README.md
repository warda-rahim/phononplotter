# # PhononPlotter

A tool for plotting phonon band structures and phonon density of states.

Prerequisites
-------------

The tools use the output from the [Phonopy code] (https://phonopy.github.io/phonopy/) [Ref. 1](#Ref1)
To use it requires a phonon calculation with the Phonopy code to have been performed on the system of interest.

The code is written in Python.

Usage
-----

1. The `phonon.py` requires `band.yaml` file from the Phonopy code, and produces a phonon band structure.

(It can also plot multiple phonon dispersion curves to test for supercell convergence).

2. The `pDoS.py` requires `projected_dos.dat` file from the Phonopy code, and produces a phonon partial density of states plot.


Examples
--------

The following examples are provided to illustrate the outputs of the code:

* [*Bi2Sn2O7*](./Example_plots) Reproduces plots for some of the calculations in [Ref. 2](#Ref2).


References
----------
1. <a name="Ref1"></a> A. Togo and I. Tanaka, "First Principles Phonon Calculations in Materials Science", Scripta Materialia, **108**, 1 (**2015**), DOI: [10.1016/j.scriptamat.2015.07.021](https://doi.org/10.1016/j.scriptamat.2015.07.021)

2. <a name="Ref2"></a>W. Rahim, J. M. Skelton and D. O. Scanlon, "\alpha-Bi2Sn2O7: A Potential Room Temperature n-type Oxide Thermoelectric", Journal of Materials Chemistry A, (**2020**), DOI: [10.1039/D0TA03945D](https://doi.org/10.1039/D0TA03945D)
