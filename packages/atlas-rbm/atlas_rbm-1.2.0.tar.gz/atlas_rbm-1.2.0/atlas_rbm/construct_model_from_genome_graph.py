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

from .utils import read_network, check_genome_graph

def monomers_from_genome_graph(data, verbose = False, toFile = False):
	# find DNA parts
	architecture = list(data['UPSTREAM']) + list(data['DOWNSTREAM'])
	architecture = [ x.replace('[', '').replace(']', '') for x in architecture ]

	names = []
	types = []
	for dna_part in sorted(set(architecture)):
		if dna_part.startswith('BS'):
			names.append('_'.join(dna_part.replace('BS-', '').split('-')))
		else:
			names.append(dna_part.split('-')[0])
			types.append(dna_part.split('-')[1])

	# dna
	code = "Monomer('dna',\n" \
		"	['name', 'type', 'loc', 'dna', 'met', 'prot', 'rna', 'up', 'dw'],\n" \
		"	{{ 'name' : [{:s}],\n" \
		"	'type' : [{:s}],\n" \
		"	'loc' : ['cyt']}})\n"

	code = code.format(
		', '.join([ '\'' + x + '\'' for x in sorted(set(names))]),
		', '.join([ '\'' + x + '\'' for x in sorted(set(types + ['BS']))]))

	if verbose:
		print(code)
	if toFile:
		with open(toFile, 'a+') as outfile:
			outfile.write(code)
	else:
		exec(code)

	# rna
	code = "Monomer('rna',\n" \
		"	['name', 'type', 'loc', 'dna', 'met', 'prot', 'rna', 'up', 'dw'],\n" \
		"	{{ 'name' : [{:s}],\n" \
		"	'type' : [{:s}],\n" \
		"	'loc' : ['cyt']}})\n"

	code = code.format(
		', '.join([ '\'' + x + '\'' for x in sorted(set(names))]),
		', '.join([ '\'' + x + '\'' for x in sorted(set(types + ['BS']))]))

	if verbose:
		print(code)
	if toFile:
		with open(toFile, 'a+') as outfile:
			outfile.write(code)
	else:
		exec(code)

	# prot
	code = "Monomer('prot',\n" \
		"	['name', 'loc', 'dna', 'met', 'prot', 'rna', 'up', 'dw'],\n" \
		"	{{ 'name' : [{:s}],\n" \
		"	'loc' : ['cyt', 'mem']}})\n"
	names = [ x for x in names if not x.startswith('BS') ]
	code = code.format(', '.join([ '\'' + x + '\'' for x in sorted(set(names))]))

	if verbose:
		print(code)
	if toFile:
		with open(toFile, 'a+') as outfile:
			outfile.write(code)
	else:
		exec(code)

	# complexes
	code = "Monomer('cplx',\n" \
		"	['name', 'loc', 'dna', 'met', 'prot', 'rna'],\n" \
		"	{ 'name' : ['RNAP_CPLX', 'RIBOSOME_CPLX'],\n" \
		"	'loc' : ['cyt']})\n"

	if verbose:
		print(code)
	if toFile:
		with open(toFile, 'a+') as outfile:
			outfile.write(code)
	else:
		exec(code)

def polymerase_docking_rules(data, verbose = False, toFile = False):
	architecture = list(data['UPSTREAM']) + [data['DOWNSTREAM'].iloc[-1]]

	for idx, dna_part in enumerate(architecture):
		if 'pro' in dna_part.lower(): # docking rules
			name = dna_part.split('-')[0]
			type = dna_part.split('-')[1]

			code = 'Rule(\'docking_{:s}\',\n' \
				'	cplx(name = \'RNAP-CPLX\', loc = \'cyt\', dna = None) +\n' \
				'	dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = None) |\n' \
				'	cplx(name = \'RNAP-CPLX\', loc = \'cyt\', dna = 1) %\n' \
				'	dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = 1),\n' \
				'	Parameter(\'fwd_docking_{:s}\', {:f}),\n' \
				'	Parameter(\'rvs_docking_{:s}\', {:f}))\n'
			code = code.format(
					dna_part, name, type, name, type,
					dna_part, float(data['RNAP_FWD_DOCK_RATE'].iloc[idx]),
					dna_part, float(data['RNAP_RVS_DOCK_RATE'].iloc[idx]))

			code = code.replace('-', '_').replace('[', '').replace(']', '')
			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code)

def polymerase_sliding_rules(data, verbose = False, toFile = False):
	architecture = data['UPSTREAM'] + ',' + data['DOWNSTREAM']
	operons = []
	for dna_part in architecture:
		if dna_part.startswith('['):
			operon = []
			operon.append(dna_part.split(',')[0][1:])
		elif dna_part.endswith(']'):
			operon.append(dna_part.split(',')[0])
			operon.append(dna_part.split(',')[1][:-1])
			operons.append(','.join(operon))
		else:
			operon.append(dna_part.split(',')[0])

	for rna_form in operons:
		UPSTREAM = rna_form.split(',')[:-1]
		DOWNSTREAM = rna_form.split(',')[1:]

		for idx, (dna_part1, dna_part2) in enumerate(zip(UPSTREAM, DOWNSTREAM)):
			name1 = dna_part1.split('-')[0]
			type1 = dna_part1.split('-')[1]
			name2 = dna_part2.split('-')[0]
			type2 = dna_part2.split('-')[1]

			if 'BS' in dna_part1:  # catch DNA binding sites to add to sliding rules
				name1 = dna_part1.replace('BS-', '')
				type1 = 'BS'
			elif 'BS' in dna_part2:
				name2 = dna_part2.replace('BS-', '')
				type2 = 'BS'

			code = 'Rule(\'sliding_{:s}\',\n' \
				'	cplx(name = \'RNAP-CPLX\', loc = \'cyt\', dna = 1) %\n' \
				'	dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = 1) +\n' \
				'	dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = None) +\n' \
				'	None >>\n' \
				'	cplx(name = \'RNAP-CPLX\', loc = \'cyt\', dna = 1) %\n' \
				'	dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = 1) +\n' \
				'	dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = None) +\n' \
				'	rna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', dna = None, met = None, prot = None, rna = None, up = None, dw = None),\n' \
				'	Parameter(\'fwd_sliding_{:s}\', {:f}))\n'
			code = code.format(
				dna_part1, name1, type1, name2, type2, name2, type2, name1, type1, name2, type2,
				dna_part1, float(data['RNAP_FWD_SLIDE_RATE'].iloc[idx]))

			code = code.replace('-', '_').replace('[', '').replace(']', '')

			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code)

def polymerase_falloff_rules(data, verbose = False, toFile = False):
	architecture = list(data['UPSTREAM']) + [data['DOWNSTREAM'].iloc[-1]]

	for idx, dna_part in enumerate(architecture):
		if 'ter' in dna_part: # falloff rules
			name = dna_part.split('-')[0]
			type = dna_part.split('-')[1]

			code = 'Rule(\'falloff_{:s}\',\n' \
				'	cplx(name = \'RNAP-CPLX\', loc = \'cyt\', dna = 1) %\n' \
				'	dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = 1) >>\n' \
				'	cplx(name = \'RNAP-CPLX\', loc = \'cyt\', dna = None) +\n' \
				'	dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = None),\n' \
				'	Parameter(\'fwd_falloff_{:s}\', {:f}))\n'
			code = code.format(
				dna_part, name, type, name, type,
				dna_part, float(data['RNAP_FWD_FALL_RATE'].iloc[idx-1]))

			code = code.replace('-', '_').replace('[', '').replace(']', '')
			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code)

def ribosome_docking_rules(data, verbose = False, toFile = False):
	architecture = list(data['UPSTREAM']) + [data['DOWNSTREAM'].iloc[-1]]

	for idx, dna_part in enumerate(architecture):
		if 'rbs' in dna_part: # docking rules
			name = dna_part.split('-')[0]
			type = dna_part.split('-')[1]

			code = 'Rule(\'dr_{:s}\',\n' \
				'	cplx(name = \'RIBOSOME-CPLX\', loc = \'cyt\', rna = None) +\n' \
				'	rna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = None) |\n' \
				'	cplx(name = \'RIBOSOME-CPLX\', loc = \'cyt\', rna = 1) %\n' \
				'	rna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = 1),\n' \
				'	Parameter(\'fwd_dr_{:s}\', {:f}),\n' \
				'	Parameter(\'rvs_dr_{:s}\', {:f}))\n'
			code = code.format(
				dna_part, name, type, name, type,
				dna_part, float(data['RIB_FWD_DOCK_RATE'].iloc[idx]),
				dna_part, float(data['RIB_RVS_DOCK_RATE'].iloc[idx]))

			code = code.replace('-', '_').replace('[', '').replace(']', '')
			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code)

def ribosome_sliding_rules(data, verbose = False, toFile = False):
	for idx, (dna_part1, dna_part2) in enumerate(zip(data['UPSTREAM'], data['DOWNSTREAM'])):
		#dna_part1, dna_part2 = (dna_part1, dna_part2)

		if 'BS' in dna_part1:  # catch DNA binding sites to add to sliding rules
			name1 = dna_part1.replace('BS-', '')
			type1 = 'BS'
		elif 'BS' in dna_part2:
			name2 = dna_part2.replace('BS-', '')
			type2 = 'BS'
		else:
			name1 = dna_part1.split('-')[0]
			type1 = dna_part1.split('-')[1]
			name2 = dna_part2.split('-')[0]
			type2 = dna_part2.split('-')[1]

		if 'cds' in type2:
			code = 'Rule(\'sr_{:s}\',\n' \
				'	cplx(name = \'RIBOSOME-CPLX\', loc = \'cyt\', rna = 1) %\n' \
				'	rna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = 1) +\n' \
				'	rna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = None) +\n' \
				'	None >>\n' \
				'	cplx(name = \'RIBOSOME-CPLX\', rna = 1) %\n' \
				'	rna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = 1) +\n' \
				'	rna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = None) +\n' \
				'	prot(name = \'{:s}\', loc = \'cyt\', dna = None, met = None, prot = None, rna = None, up = None, dw = None),\n' \
				'	Parameter(\'fwd_sr_{:s}\', {:f}))\n'
			code = code.format(
				dna_part1,
				name1, type1,
				name2, type2,
				name2, type2,
				name1, type1,
				name1,
				dna_part1, float(data['RIB_FWD_SLIDE_RATE'].iloc[idx]))

			code = code.replace('-', '_').replace('[', '').replace(']', '')
			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code)

def ribosome_falloff_rules(data, verbose = False, toFile = False):
	architecture = list(data['UPSTREAM']) + [data['DOWNSTREAM'].iloc[-1]]

	for idx, dna_part in enumerate(architecture):
		if 'cds' in dna_part: # falloff rules
			name = dna_part.split('-')[0]
			type = dna_part.split('-')[1]

			code = 'Rule(\'fr_{:s}\',\n' \
				'	cplx(name = \'RIBOSOME-CPLX\', loc = \'cyt\', rna = 1) %\n' \
				'	rna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = 1) >>\n' \
				'	cplx(name = \'RIBOSOME-CPLX\', loc = \'cyt\', rna = None) +\n' \
				'	rna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = None),\n' \
				'	Parameter(\'fwd_fr_{:s}\', {:f}))\n'
			code = code.format(
				dna_part, name, type, name, type,
				dna_part, float(data['RIB_FWD_FALL_RATE'].iloc[idx-1]))

			code = code.replace('-', '_').replace('[', '').replace(']', '')
			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code)

def observables_from_genome_graph(data, verbose = False, toFile = False):
	architecture = data['UPSTREAM'] + ',' + data['DOWNSTREAM']
	operons = []
	for dna_part in architecture:
		if dna_part.startswith('['):
			operon = []
			operon.append(dna_part.split(',')[0][1:])
		elif dna_part.endswith(']'):
			operon.append(dna_part.split(',')[0])
			operon.append(dna_part.split(',')[1][:-1])
			operons.append(','.join(operon))
		else:
			operon.append(dna_part.split(',')[0])

	# prots
	for operon in sorted(set(operons)):
		names = [(m.start(0), m.end(0)) for m in re.finditer(r'\w+-cds\d?', operon)]

		prots = []
		for lst in names:
			prots.append(operon[lst[0]:lst[1]].split('-')[0])

		for name in prots:
			code = 'Initial(prot(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = None, dw = None),\n' \
			'	Parameter(\'t0_prot_{:s}_{:s}\', 0))\n'
			code = code.format(name, 'cyt', name, 'cyt')

			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code)

			code = 'Observable(\'obs_prot_{:s}_{:s}\',\n' \
				'	prot(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = None, dw = None))\n'
			code = code.format(name, 'cyt', name, 'cyt')

			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code)

		operon_name = ''.join(prots)

		# dnas
		## create link indexes
		dw = [None] * len(operon.split(','))
		start_link = 1
		for index in range(len(operon.split(','))-1):
			dw[index] = start_link
			start_link += 1
		up = dw[-1:] + dw[:-1]

		complex_pysb = []
		for index, monomer in enumerate(operon.split(',')):
			if monomer.startswith('BS'):
				complex_pysb.append('dna(name = \'{:s}\', type = \'BS\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = {:s}, dw = {:s})'.format(
					monomer.replace('BS-', '').replace('-', '_'), 'cyt', str(up[index]), str(dw[index])))
			else:
				complex_pysb.append('dna(name = \'{:s}\', type = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = {:s}, dw = {:s})'.format(
					monomer.split('-')[0], monomer.split('-')[1], 'cyt', str(up[index]), str(dw[index])))

		complex_pysb = ' %\n	'.join(complex_pysb)

		code = 'Initial({:s},\n' \
			'	Parameter(\'t0_dna_{:s}\', 0))\n'
		code = code.format(complex_pysb, operon_name)

		if verbose:
			print(code)
		if toFile:
			with open(toFile, 'a+') as outfile:
				outfile.write(code)
		else:
			exec(code)

		code = 'Observable(\'obs_dna_{:s}\',\n' \
			'	{:s})\n'
		code = code.format(operon_name, complex_pysb)

		if verbose:
			print(code)
		if toFile:
			with open(toFile, 'a+') as outfile:
				outfile.write(code)
		else:
			exec(code)

		# rnas start at any promoter and ends at any terminator
		rna_forms = []
		a = [(m.start(0), m.end(0)) for m in re.finditer(r'\w+-pro\d?', operon)]
		b = [(m.start(0), m.end(0)) for m in re.finditer(r'\w+-ter\d?', operon)]
		for lst in itertools.product(a, b):
			rna_forms.append(operon[lst[0][0]:lst[1][1]].split(','))

		for idx, rna_form in enumerate(rna_forms):
			## create link indexes
			dw = [None] * (len(rna_form)-1)
			start_link = 1
			for index in range(len(rna_form)-2):
				dw[index] = start_link
				start_link += 1
			up = dw[-1:] + dw[:-1]

			complex_pysb = []
			for index, monomer in enumerate(rna_form[1:]):
				if monomer.startswith('BS'):
					complex_pysb.append('rna(name = \'{:s}\', type = \'BS\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = {:s}, dw = {:s})'.format(
						monomer.replace('BS-', '').replace('-', '_'), 'cyt', str(up[index]), str(dw[index])))
				else:
					complex_pysb.append('rna(name = \'{:s}\', type = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = {:s}, dw = {:s})'.format(
						monomer.split('-')[0], monomer.split('-')[1], 'cyt', str(up[index]), str(dw[index])))

			complex_pysb = ' %\n	'.join(complex_pysb)

			code = 'Initial({:s},\n' \
				'	Parameter(\'t0_rna_{:s}_form{:d}\', 0))\n'
			code = code.format(complex_pysb, operon_name, idx+1)

			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code)

			code = 'Observable(\'obs_rna_{:s}_form{:d}\',\n' \
				'	{:s})\n'
			code = code.format(operon_name, idx+1, complex_pysb)

			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code)

def construct_model_from_genome_graph(network, verbose = False, toFile = False):
	if toFile:
		with open(toFile, 'w') as outfile:
			outfile.write('from pysb import *\nModel()\n\n')

	if isinstance(network, str):
		data = read_network(network)
	elif isinstance(network, pandas.DataFrame):
		data = network
	elif isinstance(network, numpy.array):
		columns = [
			'UPSTREAM',
			'DOWNSTREAM',
			'RNAP_FWD_DOCK_RATE',
			'RNAP_RVS_DOCK_RATE',
			'RNAP_FWD_SLIDE_RATE',
			'RNAP_FWD_FALL_RATE',
			'RIB_FWD_DOCK_RATE',
			'RIB_RVS_DOCK_RATE',
			'RIB_FWD_SLIDE_RATE',
			'RIB_FWD_FALL_RATE'
			]
		data = pandas.DataFrame(data = network, columns = columns)
	else:
		raise Exception("The network format is not yet supported.")
	data = check_genome_graph(data)

	model = Model()
	monomers_from_genome_graph(data, verbose, toFile)

	# write docking, slide, and falloff of RNAP-CPLX (without sigma factor) from DNA
	polymerase_docking_rules(data, verbose, toFile)
	polymerase_sliding_rules(data, verbose, toFile)
	polymerase_falloff_rules(data, verbose, toFile)

	# write docking, slide, and falloff of RIBOSOME-CPLX from RNA
	ribosome_docking_rules(data, verbose, toFile)
	ribosome_sliding_rules(data, verbose, toFile)
	ribosome_falloff_rules(data, verbose, toFile)

	# TODO
	# write docking, slide, and falloff of RNASE-CPLX from RNA
	# write docking, slide, and falloff of PROTEASE-CPLX from protein
	observables_from_genome_graph(data, verbose, toFile)

	if toFile:
		return None
	else:
		return model
