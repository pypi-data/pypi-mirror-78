# -*- coding: utf-8 -*-

'''
Project "Reconstruction of RBM from biological networks", Rodrigo Santibáñez, 2019-2020 @ NBL, UMayor
Citation:
DOI:
'''

__author__  = 'Rodrigo Santibáñez'
__license__ = 'gpl-3.0'

#from pysb.bng import generate_network, generate_equations
from pysb.export import export
from pysb.pathfinder import set_path
from pysb.bng import generate_network, generate_equations

def to_sbml(model, outfile):
	with open(outfile, 'w') as outfile:
		outfile.write(export(model, 'sbml'))
	return None

def to_matlab(model, outfile):
	with open(outfile, 'w') as outfile:
		outfile.write(export(model, 'matlab'))
	return None

def to_mathematica(model, outfile):
	with open(outfile, 'w') as outfile:
		outfile.write(export(model, 'mathematica'))
	return None

def to_potterswheel(model, outfile):
	with open(outfile, 'w') as outfile:
		outfile.write(export(model, 'potterswheel'))
	return None

def to_bngl(model, outfile):
	with open(outfile, 'w') as outfile:
		outfile.write(export(model, 'bngl'))
	return None

def to_bngnet(model, outfile):
	with open(outfile, 'w') as outfile:
		outfile.write(export(model, 'bng_net'))
	return None

def to_kappa(model, outfile):
	with open(outfile, 'w') as outfile:
		outfile.write(export(model, 'kappa'))
	return None

def to_python(model, outfile):
	with open(outfile, 'w') as outfile:
		outfile.write(export(model, 'python'))
	return None

def to_pysb(model, outfile):
	with open(outfile, 'w') as outfile:
		outfile.write(export(model, 'pysb_flat'))
	return None

def to_stochkit(model, outfile):
	with open(outfile, 'w') as outfile:
		outfile.write(export(model, 'stochkit'))
	return None

def to_json(model, outfile):
	with open(outfile, 'w') as outfile:
		outfile.write(export(model, 'json'))
	return None
