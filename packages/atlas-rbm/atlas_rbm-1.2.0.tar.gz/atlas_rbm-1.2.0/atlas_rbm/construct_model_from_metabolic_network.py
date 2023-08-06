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

from .utils import read_network, check_metabolic_network, location_keys, location_values

def monomers_from_metabolic_network(model, data, verbose = False, toFile = False):
	# find unique metabolites and correct names
	tmp = list(data['SUBSTRATES'].values) + list(data['PRODUCTS'].values)
	tmp = ','.join(tmp)

	# correct names
	metabolites = sorted(set(tmp.split(',')))
	for index, met in enumerate(metabolites):
		for key in location_keys().keys():
			if met.startswith(key + '-'):
				metabolites[index] = met[len(key + '-'):]
			if met[0].isdigit():
				metabolites[index] = '_' + met
	metabolites = sorted(set(metabolites))

	code = "Monomer('met',\n" \
		"	['name', 'loc', 'dna', 'met', 'prot', 'rna'],\n" \
		"	{{ 'name' : [ {:s} ],\n" \
		"	'loc' : [{:s}]}})\n"

	all_mets = [ '\'' + x.replace('-', '_').replace('+', 'plus') + '\'' for x in sorted(metabolites) ]
	all_locs = [ '\'' + x.lower() + '\'' for x in sorted(location_keys().keys()) ]
	code = code.format(', '.join(all_mets), ', '.join(all_locs))

	if verbose:
		print(code)
	if toFile:
		with open(toFile, 'a+') as outfile:
			outfile.write(code)
	else:
		exec(code.replace('\t', ' ').replace('\n', ' '))

	# find unique proteins, protein complexes, and correct names
	tmp = list(data['GENE OR COMPLEX'].values)
	tmp = [ x.replace('[', '').replace(']', '').split(',') if x.startswith('[') else [x] for x in tmp ]
	tmp = [ i for j in tmp for i in j ]
	#tmp = [ ' '.join(x.replace('EX-', '').replace('WALL-', '').replace('PER-', '').replace('MEM-', '').split(', ')) for x in tmp]
	tmp = [ ' '.join(x.split(',')) for x in tmp] # location no longer coded in the name

	complexes = []
	p_monomers = []
	proteins = sorted(set(' '.join(tmp).split(' ')))
	for index, protein in enumerate(proteins):
		if protein[0].isdigit():
			proteins[index] = '_' + protein

	for index, protein in enumerate(proteins):
		if ('CPLX' in protein) or ('CPL' in protein) or ('COMPLEX' in protein) or ('DIMER' in protein):
			complexes.append(protein)
		else:
			if 'spontaneous' != protein or 'unknown' != protein:
				p_monomers.append(protein)

	code = "Monomer('prot',\n" \
		"	['name', 'loc', 'dna', 'met', 'prot', 'rna', 'up', 'dw'],\n" \
		"	{{ 'name' : [ {:s} ],\n" \
		"	'loc' : [{:s}]}})\n"

	all_proteins = [ '\'' + x.replace('-', '_') + '\'' for x in sorted(p_monomers)]
	code = code.format(', '.join(all_proteins), ', '.join(all_locs))

	if verbose:
		print(code)
	if toFile:
		with open(toFile, 'a+') as outfile:
			outfile.write(code)
	else:
		exec(code.replace('\t', ' ').replace('\n', ' '))

	if len(complexes) > 0:
		code = "Monomer('cplx',\n" \
			"	['name', 'loc', 'dna', 'met', 'prot', 'rna', 'up', 'dw'],\n" \
			"	{{ 'name' : [ {:s} ],\n" \
			"	'loc' : [{:s}]}})\n"

		for index, cplx in enumerate(complexes):
			if cplx[0].isdigit():
				complexes[index] = '_' + cplx

		all_cplx = [ '\'' + x.replace('-', '_') + '\'' for x in sorted(complexes)]
		code = code.format(', '.join(all_cplx), ', '.join(all_locs))

		if verbose:
			print(code)
		if toFile:
			with open(toFile, 'a+') as outfile:
				outfile.write(code)
		else:
			exec(code.replace('\t', ' ').replace('\n', ' '))

	return metabolites, p_monomers, complexes, list(data['GENE OR COMPLEX'].values)

def rules_from_metabolic_network(model, data, verbose = False, toFile = False):
	for idx in data.index:
		rxn = data.loc[idx]
		if isinstance(rxn['ENZYME LOCATION'], str):
			rxn['ENZYME LOCATION'] = rxn['ENZYME LOCATION'].replace('[', '').replace(']', '').split(',')

		# first: determine enzyme composition
		if ('CPLX' in rxn['GENE OR COMPLEX']) or ('CPL' in rxn['GENE OR COMPLEX']) or ('COMPLEX' in rxn['GENE OR COMPLEX']) or ('DIMER' in rxn['GENE OR COMPLEX']): # the enzyme is an alias of a protein complex
			# correct name
			if rxn['GENE OR COMPLEX'][0].isdigit():
				rxn['GENE OR COMPLEX'] = '_' + rxn['GENE OR COMPLEX']

			if len(rxn['ENZYME LOCATION']) == 1:
				location = location_values()[rxn['ENZYME LOCATION'][0]].lower()
				enzyme = 'cplx(name = \'{:s}\', loc = \'{:s}\')'.format(rxn['GENE OR COMPLEX'].replace('-', '_'), location)

		elif rxn['GENE OR COMPLEX'].startswith('['): # an enzymatic complex described by its monomers
			monomers = rxn['GENE OR COMPLEX'][1:-1].split(',')
			enzyme = []

			# correct names
			for index, monomer in enumerate(monomers):
				if monomer[0].isdigit():
					monomers[index] = '_' + monomer

			## create link indexes
			dw = [None] * len(monomers)
			start_link = 1
			for index in range(len(monomers)-1):
				dw[index] = start_link
				start_link += 1
			up = dw[-1:] + dw[:-1]

			if len(monomers) == len(rxn['ENZYME LOCATION']):
				for index, (monomer, location) in enumerate(zip(monomers, rxn['ENZYME LOCATION'])):
					loc = location_values()[location].lower()
					enzyme.append('prot(name = \'{:s}\', loc = \'{:s}\', up = {:s}, dw = {:s})'.format(monomer, loc, str(up[index]), str(dw[index])))

			elif len(rxn['ENZYME LOCATION']) == 1:
				for index, monomer in enumerate(monomers):
					loc = location_values()[rxn['ENZYME LOCATION']].lower()
					enzyme.append('prot(name = \'{:s}\', loc = \'{:s}\', up = {:s}, dw = {:s})'.format(monomer, loc, str(up[index]), str(dw[index])))

			elif len(monomers) != len(rxn['ENZYME LOCATION']):
				for index, monomer in enumerate(monomers):
					loc = location_values()[rxn['ENZYME LOCATION'][0]].lower()
					enzyme.append('prot(name = \'{:s}\', loc = \'{:s}\', up = {:s}, dw = {:s})'.format(monomer, loc, str(up[index]), str(dw[index])))

			enzyme = ' %\n	'.join(enzyme)

		else: # the enzyme is a monomer
			# correct name
			if rxn['GENE OR COMPLEX'][0].isdigit():
				rxn['GENE OR COMPLEX'] = '_' + rxn['GENE OR COMPLEX']

			loc = location_values()[rxn['ENZYME LOCATION'][0]].lower()
			enzyme = 'prot(name = \'{:s}\', loc = \'{:s}\')'.format(rxn['GENE OR COMPLEX'].replace('-', '_'), loc)

		# second: correct reaction names starting with a digit
		name = rxn['REACTION'].replace('-', '_').replace('.', 'dot').replace('+', 'plus')
		if name[0].isdigit():
			name = '_' + name

		# third: correct metabolite names with dashes or plus signs, prefix underscore for metabolite names starting by a digit, and create a list
		substrates = rxn['SUBSTRATES'].replace('-', '_').replace('+', 'plus').split(',')
		substrates = [ '_' + subs if subs[0].isdigit() else subs for subs in substrates ]
		products = rxn['PRODUCTS'].replace('-', '_').replace('+', 'plus').split(',')
		products = [ '_' + prod if prod[0].isdigit() else prod for prod in products ]

		# fourth: write LHS and RHS
		LHS = []
		RHS = []

		if rxn['GENE OR COMPLEX'] == 'spontaneous' or rxn['GENE OR COMPLEX'] == 'unknown':
			locations = rxn['ENZYME LOCATION']
			if locations == 'unknown':
				locations = 'cytosol' # fallback
		else:
			locations = location_values().keys()

		for subs in substrates:
			islocated = False
			for loc in locations:
				loc = location_values()[loc]
				if subs.startswith(loc + '_'):
					LHS.append('met(name = \'{:s}\', loc = \'{:s}\', prot = None)'.format(subs[len(loc + '_'):], loc.lower()))
					islocated = True
			if not islocated:
				LHS.append('met(name = \'{:s}\', loc = \'{:s}\', prot = None)'.format(subs, 'cyt'))

		for prod in products:
			islocated = False
			for loc in locations:
				loc = location_values()[loc]
				if prod.startswith(loc + '_'):
					RHS.append('met(name = \'{:s}\', loc = \'{:s}\', prot = None)'.format(prod[len(loc + '_'):], loc.lower()))
					islocated = True
			if not islocated:
				RHS.append('met(name = \'{:s}\', loc = \'{:s}\', prot = None)'.format(prod, 'cyt'))

		# fifth: match the number of agents at both sides of the Rule (pySB checks and kappa v4 requires the matching)
		if len(substrates) < len(products):
			for index in range(len(substrates), len(products)):
				LHS.append('None')
		elif len(products) < len(substrates):
			for index in range(len(products), len(substrates)):
				RHS.append('None')

		# pretty print the Rule
		LHS = ' +\n	'.join(LHS)
		RHS = ' +\n	'.join(RHS)

		if rxn['GENE OR COMPLEX'] == 'spontaneous' or rxn['GENE OR COMPLEX'] == 'unknown':
			for location in rxn['ENZYME LOCATION']:
				loc = location_values()[location]
				code = 'Rule(\'{:s}\',\n' \
					'	{:s} |\n'\
					'	{:s},\n' \
					'	Parameter(\'fwd_{:s}\', {:f}), \n' \
					'	Parameter(\'rvs_{:s}\', {:f}))\n'
				code = code.format(name + '_' + loc, LHS, RHS, name + '_' + loc, float(rxn['FWD_RATE']), name + '_' + loc, float(rxn['RVS_RATE']))
				code = code.replace('loc = \'cyt\'', 'loc = \'{:s}\''.format(loc.lower()))

				if verbose:
					print(code)
				if toFile:
					with open(toFile, 'a+') as outfile:
						outfile.write(code)
				else:
					exec(code.replace('\t', ' ').replace('\n', ' '))

		else: # reaction needs an enzyme
			code = 'Rule(\'{:s}\',\n' \
				'	{:s} +\n	{:s} | \n' \
				'	{:s} +\n	{:s}, \n' \
				'	Parameter(\'fwd_{:s}\', {:f}), \n' \
				'	Parameter(\'rvs_{:s}\', {:f}))\n'
			code = code.format(name, enzyme, LHS, enzyme, RHS, name, float(rxn['FWD_RATE']), name, float(rxn['RVS_RATE']))
			code = code.replace('-', '_')

			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code.replace('\t', ' ').replace('\n', ' '))

def observables_from_metabolic_network(model, data, monomers, verbose = False, toFile = False, noInitials = False, noObservables = False):
	#locations = location_keys().keys() # reduce compilation time
	locations = ['cyt']
	if not noObservables:
		for name in sorted(monomers[0]):
			name = name.replace('-', '_').replace('+', 'plus')
			for loc in locations:
				code = 'Observable(\'obs_met_{:s}_{:s}\', met(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None))\n'
				code = code.format(name, loc.lower(), name, loc.lower())
				if verbose:
					print(code)
				if toFile:
					with open(toFile, 'a+') as outfile:
						outfile.write(code)
				else:
					exec(code.replace('\t', ' ').replace('\n', ' '))

	if not noInitials:
		for name in sorted(monomers[0]):
			name = name.replace('-', '_').replace('+', 'plus')
			for loc in locations:
				code = 'Initial(met(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None), Parameter(\'t0_met_{:s}_{:s}\', 0))\n'
				code = code.format(name, loc.lower(), name, loc.lower())
				if verbose:
					print(code)
				if toFile:
					with open(toFile, 'a+') as outfile:
						outfile.write(code)
				else:
					exec(code.replace('\t', ' ').replace('\n', ' '))

		for name in sorted(monomers[1]):
			name = name.replace('-','_')
			for loc in locations:
				code = 'Initial(prot(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = None, dw = None), Parameter(\'t0_prot_{:s}_{:s}\', 0))\n'
				code = code.format(name, loc.lower(), name, loc.lower())
				if verbose:
					print(code)
				if toFile:
					with open(toFile, 'a+') as outfile:
						outfile.write(code)
				else:
					exec(code.replace('\t', ' ').replace('\n', ' '))

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
					exec(code.replace('\t', ' ').replace('\n', ' '))

	if not noInitials or not noObservables:
		names = monomers[3]
		for name in sorted(set(names)):
			if name.startswith('['):
				monomers = name[1:-1].split(',')
				complex_pysb = []

				from collections import Counter
				stoichiometry = Counter(monomers)
				cplx_composition = ''
				for key, value in stoichiometry.items():
					cplx_composition += '_{:s}x{:d}'.format(key, value)

				## create link indexes
				dw = [None] * len(monomers)
				start_link = 1
				for index in range(len(monomers)-1):
					dw[index] = start_link
					start_link += 1
				up = dw[-1:] + dw[:-1]

				for location in locations:
					complex_pysb = []
					for index, monomer in enumerate(monomers):
						complex_pysb.append('prot(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = {:s}, dw = {:s})'.format(
							monomer, location.lower(), str(up[index]), str(dw[index])))

					complex_pysb = ' %\n	'.join(complex_pysb)

					if not noInitials:
						code = 'Initial({:s},\n\tParameter(\'t0_cplx{:s}_{:s}\', 0))\n'
						code = code.format(complex_pysb, cplx_composition, location.lower())

						if verbose:
							print(code)
						if toFile:
							with open(toFile, 'a+') as outfile:
								outfile.write(code)
						else:
							exec(code.replace('\t', ' ').replace('\n', ' '))

					if not noObservables:
						code = 'Observable(\'obs_cplx{:s}_{:s}\',\n\t{:s})\n'
						code = code.format(cplx_composition, location.lower(), complex_pysb)

						if verbose:
							print(code)
						if toFile:
							with open(toFile, 'a+') as outfile:
								outfile.write(code)
						else:
							exec(code.replace('\t', ' ').replace('\n', ' '))

def construct_model_from_metabolic_network(network, verbose = False, toFile = False, noInitials = False, noObservables = False):
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
		raise Exception("The network data type is not yet supported.")
	data = check_metabolic_network(data)

	model = Model()
	[metabolites, p_monomers, complexes, hypernodes] = \
		monomers_from_metabolic_network(model, data, verbose, toFile)
	observables_from_metabolic_network(model, data, [metabolites, p_monomers, complexes, hypernodes], verbose, toFile, noInitials, noObservables)
	rules_from_metabolic_network(model, data, verbose, toFile)

	if toFile:
		return None
	else:
		return model
