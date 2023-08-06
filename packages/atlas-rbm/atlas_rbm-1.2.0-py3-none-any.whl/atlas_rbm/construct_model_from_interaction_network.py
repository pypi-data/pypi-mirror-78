# -*- coding: utf-8 -*-

'''
Project "Reconstruction of RBM from biological networks", Rodrigo Santibáñez, 2019-2020 @ NBL, UMayor
Citation:
DOI:
'''

__author__  = 'Rodrigo Santibáñez'
__license__ = 'gpl-3.0'

from pysb import *
from pysb.util import *
from pysb.core import *

import re
import numpy
import pandas

from .utils import read_network, check_interaction_network, location_keys, location_values, connectAgents

def monomers_from_interaction_network(model, data, verbose = False, toFile = False):
	# find unique metabolites and correct names
	tmp = list(data['SOURCE'].values) + list(data['TARGET'].values)
	tmp = [ x.replace('[', '').replace(']', '').split(',') if x.startswith('[') else [x] for x in tmp ]
	tmp = [ i for j in tmp for i in j ]
	tmp = [ x.replace('SMALL-', '') for x in tmp if x.startswith('SMALL-') ]
	tmp = ','.join(tmp)
	#for key in location_keys().keys():
		#tmp = tmp.replace(key + '-', '') # location no longer coded in the name

	metabolites = sorted(set(tmp.split(',')))
	if len(tmp) > 0:
		for index, met in enumerate(metabolites):
			if met[0].isdigit():
				metabolites[index] = '_' + met

		code = "Monomer('met',\n" \
			"	['name', 'loc', 'dna', 'met', 'prot', 'rna'],\n" \
			"	{{ 'name' : [ {:s} ], \n" \
			"	'loc' : [{:s}]}})\n"

		all_mets = [ '\'' + x.replace('-', '_') + '\'' for x in sorted(metabolites) ]
		all_locs = [ '\'' + x.lower() + '\'' for x in sorted(location_keys().keys()) ]
		code = code.format(', '.join(all_mets), ', '.join(all_locs))

		if verbose:
			print(code)
		if toFile:
			with open(toFile, 'a+') as outfile:
				outfile.write(code)
		else:
			exec(code.replace('\n', ''))
	else:
		metabolites = []

	# find unique proteins and protein complexes, and correct names
	tmp = list(data['SOURCE'].values) + list(data['TARGET'].values)
	tmp = [ x.replace('[', '').replace(']', '').split(',') if x.startswith('[') else [x] for x in tmp ]
	tmp = [ i for j in tmp for i in j ]
	tmp = [ x for x in tmp if not (x.startswith('SMALL-') or x.startswith('BS-') or x.startswith('DNA-') or x.startswith('RNA-')) ]
	#tmp = [ ' '.join(x.replace('MEM-', '').replace('PER-', '').replace('WALL-', '').replace('EX-', '').split(',')) for x in tmp] # location no longer coded in the name
	tmp = [ ' '.join(x.split(',')) for x in tmp ]

	complexes = []
	p_monomers = []
	proteins = sorted(set(' '.join(tmp).split(' ')))
	for index, protein in enumerate(proteins):
		if protein[0].isdigit():
			protein[index] = '_' + protein
		if 'CPLX' in protein:
			complexes.append(protein)
		else:
			if 'spontaneous' != protein:
				p_monomers.append(protein)

	code = "Monomer('prot',\n" \
		"	['name', 'loc', 'dna', 'met', 'prot', 'rna', 'up', 'dw'],\n" \
		"	{{ 'name' : [ {:s} ], \n" \
		"	'loc' : [{:s}]}})\n"

	all_proteins = [ '\'' + x.replace('-', '_') + '\'' for x in sorted(p_monomers)]
	all_locs = [ '\'' + x.lower() + '\'' for x in sorted(location_keys().keys()) ]
	code = code.format(', '.join(all_proteins), ', '.join(all_locs))

	if verbose:
		print(code)
	if toFile:
		with open(toFile, 'a+') as outfile:
			outfile.write(code)
	else:
		exec(code.replace('\n', ''))

	if len(complexes) > 0:
		code = "Monomer('cplx',\n" \
			"	['name', 'loc', 'dna', 'met', 'prot', 'rna', 'up', 'dw'],\n" \
			"	{{ 'name' : [ {:s} ],\n" \
			"	'loc' : [{:s}]}})\n"

		all_cplx = [ '\'' + x.replace('-', '_') + '\'' for x in sorted(complexes)]
		code = code.format(', '.join(all_cplx), ', '.join(all_locs))

		if verbose:
			print(code)
		if toFile:
			with open(toFile, 'a+') as outfile:
				outfile.write(code)
		else:
			exec(code.replace('\n', ''))

	# find DNA binding sites and types
	tmp = list(data['SOURCE'].values) + list(data['TARGET'].values)
	tmp = [ x.replace('[', '').replace(']', '').split(',') if x.startswith('[') else [x] for x in tmp ]
	tmp = [ i for j in tmp for i in j ]
	tmp = [ x.replace('BS-', '') for x in tmp if x.startswith('BS-') ] + [ x.replace('DNA-', '') for x in tmp if x.startswith('DNA-') ]
	dnas = sorted(set(tmp))

	tmp = list(data['SOURCE'].values) + list(data['TARGET'].values)
	tmp = [ x.replace('[', '').replace(']', '').split(',') if x.startswith('[') else [x] for x in tmp ]
	tmp = [ i for j in tmp for i in j ]
	tmp = [ x.split('-')[-1] for x in tmp if x.startswith('DNA-') ] + ['BS']
	types = sorted(set(tmp))

	if len(dnas) > 0:
		code = "Monomer('dna',\n" \
			"	['name', 'type', 'loc', 'dna', 'met', 'prot', 'rna', 'up', 'dw'],\n" \
			"	{{ 'name' : [ {:s} ],\n" \
			"	'type' : [{:s}],\n" \
			"	'loc' : ['cyt']}})\n"

		code = code.format(
			', '.join([ '\'' + x.replace('-', '_') + '\'' for x in dnas ]),
			', '.join([ '\'' + x.replace('-', '_') + '\'' for x in types ]))

		if verbose:
			print(code)
		if toFile:
			with open(toFile, 'a+') as outfile:
				outfile.write(code)
		else:
			exec(code.replace('\n', ''))

	return metabolites, p_monomers, complexes, zip(list(data['SOURCE']), list(data['TARGET']))

def from_interaction_network(data, i):
	## form the LHS
	LHS = []

	# data
	agents = (data['SOURCE'].iloc[i] + ',' + data['TARGET'].iloc[i])
	names = agents.split(',')
	location = data['LOCATION'].iloc[i].replace('[', '').replace(']', '').split(',') # just in case the user wrote "[location]"

	# set locations for all agents
	if len(location) == 1: # all agents are located in the same compartment
		location = [ location_values()[location[0]] ] * len(names)
	elif len(location) == len(names): # agents are located in different compartments (e.g. araFGH)
		location = [ location_values()[x] for x in location ]
	else:
		location = [ location_values()[location[0]] ] * len(names) # fallback to warning
		print('WARNING: the location list has an incorrect length to determine location for all agents. Location for all agents will be {:s}'.format(location[0]))

	next_in_complex = False
	for name, loc in zip(names, location):
		if name[0] == '[': # we are dealing with the first monomer of a complex
			molecule = name[1:]
			next_in_complex = True
		elif name[-1] == ']': # we are dealing with the last monomer of a complex
			molecule = name[:-1]
			next_in_complex = False
		elif next_in_complex: # we are dealing with a monomer part of a complex
			molecule = name
		else:
			molecule = name

		if molecule.split('-')[-1][0:3].lower() in ['pro', 'rbs', 'cds', 'ter']:
			LHS.append('dna(name = \'{:s}\', type = \'{:s}\', loc = \'{:s}\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.split('-')[-2], molecule.split('-')[-1], loc.lower()))
		elif molecule.startswith('BS-'):
			LHS.append('dna(name = \'{:s}\', type = \'BS\', loc = \'{:s}\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.replace('BS-', ''), loc.lower()))
		elif molecule.startswith('SMALL'):
			LHS.append('met(name = \'{:s}\', loc = \'{:s}\', prot = met_link)'.format(molecule.replace('SMALL-', ''), loc.lower()))
		else:
			LHS.append('prot(name = \'{:s}\', loc = \'{:s}\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)'.format(molecule, loc.lower()))

	## join complexes
	LHS = connectAgents(agents, LHS)

	## LHS final join
	LHS = ' +\n	'.join(LHS)

	## form the RHS
	RHS = []

	## data
	agents = '[' + (data['SOURCE'].iloc[i] + ',' + data['TARGET'].iloc[i]).replace('[', '').replace(']', '') + ']'
	names = agents.split(',')

	for name in names:
		if name[0] == '[': # we are dealing with the first monomer of a complex
			molecule = name[1:]
			next_in_complex = True
		elif name[-1] == ']': # we are dealing with the last monomer of a complex
			molecule = name[:-1]
			next_in_complex = False
		elif next_in_complex: # we are dealing with a monomer part of a complex
			molecule = name
		else:
			molecule = name

		if molecule.split('-')[-1][0:3].lower() in ['pro', 'rbs', 'cds', 'ter']:
			RHS.append('dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.split('-')[-2], molecule.split('-')[-1]))
		elif molecule.startswith('BS-'):
			RHS.append('dna(name = \'{:s}\', type = \'BS\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.replace('BS-', '')))
		elif molecule.startswith('SMALL'):
			RHS.append('met(name = \'{:s}\', loc = \'cyt\', prot = met_link)'.format(molecule.replace('SMALL-', '')))
		else:
			RHS.append('prot(name = \'{:s}\', loc = \'cyt\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)'.format(molecule))

	## join complexes
	RHS = connectAgents(agents, RHS)

	## RHS final join
	RHS = ' %\n	'.join(RHS)

	return LHS, RHS

def observables_from_interaction_network(model, data, monomers, verbose = False, toFile = False):
	#locations = location_keys().keys() # reduce compilation time
	locations = ['cyt']
	for name in sorted(monomers[0]):
		name = name.replace('-','_')
		for loc in locations:
			code = 'Observable(\'obs_met_{:s}_{:s}\', met(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None))\n'
			code = code.format(name, loc.lower(), name, loc.lower())
			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code.replace('\t', ''))

			code = "Initial(met(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None), Parameter(\'t0_met_{:s}_{:s}\', 0))\n"
			code = code.format(name, loc.lower(), name, loc.lower())
			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code.replace('\t', ''))

	for name in sorted(monomers[1]):
		name = name.replace('-','_')
		for loc in locations:
			code = 'Observable(\'obs_prot_{:s}_{:s}\', prot(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = None, dw = None))\n'
			code = code.format(name, loc.lower(), name, loc.lower())
			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code.replace('\t', ''))

			code = 'Initial(prot(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = None, dw = None), Parameter(\'t0_prot_{:s}_{:s}\', 0))\n'
			code = code.format(name, loc.lower(), name, loc.lower())
			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code.replace('\t', ''))

	for name in sorted(monomers[2]):
		name = name.replace('-','_')
		for loc in locations:
			code = 'Initial(cplx(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = None, dw = None), Parameter(\'t0_cplx_{:s}_{:s}\', 0))\n'
			code = code.format(name, loc.lower(), name, loc.lower())
			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code.replace('\t', ''))

	names = []
	for left, right in zip(list(data['SOURCE']), list(data['TARGET'])):
		names.append('[' + (left + ',' + right).replace('[','').replace(']','') + ']')

	for name in sorted(set(names)):
		# initials with DNA parts are required to be concrete (so enumeration of all possible DNA-protein complexes)
		# that why we removed them from the list
		if name.startswith('[') and not 'BS' in name and not 'DNA' in name:
			monomers = name[1:-1].split(',')

			from collections import Counter
			stoichiometry = Counter(monomers)
			cplx_composition = ''
			for key, value in stoichiometry.items():
				cplx_composition += '_{:s}x{:d}'.format(key.replace('SMALL-', ''), value)

			#for location in location_keys().keys(): # reduce compilation time
			for loc in locations:
				complex_pysb = []
				for index, molecule in enumerate(monomers):
					if molecule.split('-')[-1][0:3].lower() in ['pro', 'rbs', 'cds', 'ter']:
						complex_pysb.append('dna(name = \'{:s}\', type = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = dna_link, rna = None, up = None, dw = ANY)'.format(molecule.split('-')[-2], molecule.split('-')[-1], loc.lower()))
					elif molecule.startswith('BS-'):
						complex_pysb.append('dna(name = \'{:s}\', type = \'BS\', loc = \'{:s}\', dna = None, met = None, prot = dna_link, rna = None, up = None, dw = None)'.format(molecule.replace('BS-', ''), loc.lower()))
					elif molecule.startswith('SMALL'):
						complex_pysb.append('met(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = met_link, rna = None)'.format(molecule.replace('SMALL-', ''), loc.lower()))
					else:
						complex_pysb.append('prot(name = \'{:s}\', loc = \'{:s}\', dna = dna_link, met = met_link, prot = None, rna = None, up = prot_link, dw = prot_link)'.format(molecule, loc.lower()))

				## join complexes
				complex_pysb = connectAgents(name, complex_pysb)

				## final join
				complex_pysb = ' %\n	'.join(complex_pysb)

				code = 'Initial({:s},\n' \
					'	Parameter(\'t0_cplx{:s}_{:s}\', 0))\n'
				code = code.format(complex_pysb, cplx_composition, loc.lower()).replace('-', '_')

				if verbose:
					print(code)
				if toFile:
					with open(toFile, 'a+') as outfile:
						outfile.write(code)
				else:
					exec(code.replace('\t', ' ').replace('\n', ' '))

				code = 'Observable(\'obs_cplx{:s}_{:s}\',\n' \
					'	{:s})\n'
				code = code.format(cplx_composition, loc.lower(), complex_pysb).replace('-', '_')

				if verbose:
					print(code)
				if toFile:
					with open(toFile, 'a+') as outfile:
						outfile.write(code)
				else:
					exec(code.replace('\t', ' ').replace('\n', ' '))

	return model

def construct_model_from_interaction_network(network, verbose = False, toFile = False):
	if toFile:
		with open(toFile, 'w') as outfile:
			outfile.write('from pysb import *\nModel()\n\n')

	if isinstance(network, str):
		data = read_network(network)
	elif isinstance(network, pandas.DataFrame):
		data = network
	elif isinstance(network, numpy.array):
		data = pandas.DataFrame(data = network)
	else:
		raise Exception("The network format is not yet supported.")
	data = check_interaction_network(data)

	model = Model()
	[metabolites, p_monomers, complexes, hypernodes] = \
		monomers_from_interaction_network(model, data, verbose, toFile)
	observables_from_interaction_network(model, data, [metabolites, p_monomers, complexes, hypernodes], verbose, toFile)

	for index, _ in enumerate(data.index):
		LHS, RHS = from_interaction_network(data, index)

		## complete rule
		name = 'PhysicalInteractionRule_{{:0{:d}d}}'.format(len(str(len(data.index))))
		name = name.format(index+1)
		code = 'Rule(\'{:s}\',\n' \
			'	{:s} | \n	{:s},\n' \
			'	Parameter(\'fwd_{:s}\', {:f}),\n' \
			'	Parameter(\'rvs_{:s}\', {:f}))\n'
		code = code.format(name, LHS, RHS, name, data['FWD_RATE'].iloc[index], name, data['RVS_RATE'].iloc[index])
		code = code.replace('-', '_').replace('{:s}', 'None')

		if verbose:
			print(code)
		if toFile:
			with open(toFile, 'a+') as outfile:
				outfile.write(code)
		else:
			exec(code.replace('\t', ''))

	if toFile:
		return None
	else:
		return model
