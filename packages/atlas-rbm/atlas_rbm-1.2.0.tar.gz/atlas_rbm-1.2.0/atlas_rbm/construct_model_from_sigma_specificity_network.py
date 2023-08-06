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

from .utils import read_network, check_genome_graph, check_interaction_network, connectAgents
#from .construct_model_from_genome_graph import monomers_from_genome_graph, observables_from_genome_graph # not working because reasons
#from .construct_model_from_genome_graph import ribosome_docking_rules, ribosome_sliding_rules, ribosome_falloff_rules # not working because reasons

def monomers_from_genome_graph(data, verbose = False, toFile = False):
	# find DNA parts
	architecture = list(data['UPSTREAM']) + list(data['DOWNSTREAM'])
	architecture = [ x.replace('[', '').replace(']', '') for x in architecture ]

	names = []
	types = []
	for dna_part in sorted(set(architecture)):
		if dna_part.startswith('BS-'):
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
		"	{ 'name' : ['RIBOSOME_CPLX'],\n" \
		"	'loc' : ['cyt']})\n"

	if verbose:
		print(code)
	if toFile:
		with open(toFile, 'a+') as outfile:
			outfile.write(code)
	else:
		exec(code)

def polymerase_docking_rules(data, data_arq, verbose = False, toFile = False):
	RULE_LHS = []
	for i in data.index:
		# data
		agents = (data['SOURCE'].iloc[i] + ',' + data['TARGET'].iloc[i])
		names = agents.split(',')

		## form the LHS
		LHS = []
		next_in_complex = False
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

			if molecule.split('-')[-1][0:3].lower() == 'pro':
				LHS.append('dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.split('-')[-2], molecule.split('-')[-1]))
			elif molecule.startswith('SMALL'):
				LHS.append('met(name = \'{:s}\', loc = \'cyt\', prot = met_link)'.format(molecule.replace('SMALL-', '')))
			else:
				LHS.append('prot(name = \'{:s}\', loc = \'cyt\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)'.format(molecule))

		## join complexes
		LHS = connectAgents(agents, LHS)

		## LHS final join
		LHS = ' +\n	'.join(LHS)
		RULE_LHS.append(LHS)

	RULE_RHS = []
	for i in data.index:
		## data
		agents = (data['SOURCE'].iloc[i].replace(']', '') + ',' + data['TARGET'].iloc[i]) + ']'
		names = agents.split(',')

		## write the RHS
		RHS = []
		for index, name in enumerate(names):
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

			if molecule.split('-')[-1][0:3].lower() == 'pro':
				RHS.append('dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.split('-')[-2], molecule.split('-')[-1]))
			elif molecule.startswith('SMALL'):
				RHS.append('met(name = \'{:s}\', loc = \'cyt\', prot = met_link)'.format(molecule.replace('SMALL-', '')))
			else:
				RHS.append('prot(name = \'{:s}\', loc = \'cyt\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)'.format(molecule))

		## join complexes
		RHS = connectAgents(agents, RHS)

		## LHS final join
		RHS = ' +\n	'.join(RHS)
		RULE_RHS.append(RHS)

	for index in data.index:
		for dna_part1 in data_arq['UPSTREAM']:
			if data['TARGET'].iloc[index] == dna_part1.replace('[', ''):
				## complete rule
				code = 'Rule(\'docking_{:d}_{:s}\',\n' \
					'	{:s} |\n' \
					'	{:s},\n' \
					'	Parameter(\'fwd_docking_{:d}_{:s}\', {:f}),\n' \
					'	Parameter(\'rvs_docking_{:d}_{:s}\', {:f}))\n'

				code = code.format(
					index+1, dna_part1.replace('[', ''), RULE_LHS[index], RULE_RHS[index],
					index+1, dna_part1.replace('[', ''), data['FWD_DOCK_RATE'].iloc[index],
					index+1, dna_part1.replace('[', ''), data['RVS_DOCK_RATE'].iloc[index])

				code = code.replace('-', '_')
				if verbose:
					print(code)
				if toFile:
					with open(toFile, 'a+') as outfile:
						outfile.write(code)
				else:
					exec(code)

def polymerase_sliding_from_promoters_rules(data, data_arq, verbose = False, toFile = False):
	RULE_LHS = []
	RULE_RHS = []

	for index, sigma in enumerate(data.index):
		for dna_part1, dna_part2 in zip(data_arq['UPSTREAM'], data_arq['DOWNSTREAM']):
			if data['TARGET'].iloc[sigma] == dna_part1.replace('[', ''):

				## form the LHS
				agents = data['SOURCE'].iloc[sigma][:-1] + ',' + data['TARGET'].iloc[sigma] + '],' + dna_part2
				names = agents.split(',')

				LHS = []
				next_in_complex = False
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
						LHS.append('dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.split('-')[-2], molecule.split('-')[-1]))
					elif molecule.startswith('BS-'):
						LHS.append('dna(name = \'{:s}\', type = \'BS\', loc = \'cyt\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.replace('BS-', '')))
					elif molecule.startswith('SMALL'):
						LHS.append('met(name = \'{:s}\', loc = \'cyt\', prot = met_link)'.format(molecule.replace('SMALL-', '')))
					else:
						LHS.append('prot(name = \'{:s}\', loc = \'cyt\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)'.format(molecule))

				# append an empty slot to match the RNA synthesis
				LHS.append('None')

				## join complexes
				LHS = connectAgents(agents, LHS)

				## LHS final join
				LHS = ' +\n	'.join(LHS)
				RULE_LHS.append(LHS)

				## form the RHS
				agents = ','.join(data['SOURCE'].iloc[sigma].split(',')[:-1]) + ',' + dna_part2 + '],' + data['TARGET'].iloc[sigma]
				names = agents.split(',')

				RHS = []
				next_in_complex = False
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
						RHS.append('dna(name = \'{:s}\', type = \'BS\', loc = \'cyt\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.replace('BS-', '')))
					elif molecule.startswith('SMALL'):
						RHS.append('met(name = \'{:s}\', loc = \'cyt\', prot = met_link)'.format(molecule.replace('SMALL-', '')))
					else:
						RHS.append('prot(name = \'{:s}\', loc = \'cyt\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)'.format(molecule))

				# append the RNA synthetized from the rule application
				if dna_part2.startswith('BS'):
					RHS.append('rna(name = \'{:s}\', type = \'BS\', loc = \'cyt\', dna = None, met = None, prot = None, rna = None, up = None, dw = None)'.format(
						dna_part2.replace('BS-', '')))
				else:
					RHS.append('rna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', dna = None, met = None, prot = None, rna = None, up = None, dw = None)'.format(
						dna_part2.split('-')[0], dna_part2.split('-')[1]))

				## join complexes
				RHS = connectAgents(agents, RHS)

				## RHS final join
				RHS = ' +\n	'.join(RHS)
				RULE_RHS.append(RHS)

				## complete rule
				code = 'Rule(\'sliding_{:d}_{:s}_holoenzyme\',\n' \
					'	{:s} >>\n' \
					'	{:s},\n' \
					'	Parameter(\'fwd_sliding_{:d}_{:s}_holoenzyme\', {:f}))\n' \

				code = code.format(
					index+1, dna_part1.replace('[', '') + '_' + dna_part2.split('-')[-1],
					RULE_LHS[index], RULE_RHS[index].replace('[', ''),
					index+1, dna_part1.replace('[', '') + '_' + dna_part2.split('-')[-1],
					data_arq['RNAP_FWD_SLIDE_RATE'][data_arq['DOWNSTREAM'].replace(']', '').str.match(dna_part2)].values[0])

				code = code.replace('-', '_')
				if verbose:
					print(code)
				if toFile:
					with open(toFile, 'a+') as outfile:
						outfile.write(code)
				else:
					exec(code)

def polymerase_sliding_from_others_rules(data, data_arq, verbose = False, toFile = False):
	architecture = data_arq['UPSTREAM'] + ',' + data_arq['DOWNSTREAM']
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
		rna_form = rna_form.split(',')
		# remove the first promoter because its redundant with the sliding of the holoenzyme from the promoter
		for idx, dna_part in enumerate(rna_form[2:], 1):
			## form the LHS
			agents = ','.join(data['SOURCE'].iloc[0].split(',')[:-1]) + ',' + rna_form[idx] + '],' + rna_form[idx+1]
			names = agents.split(',')

			LHS = []
			next_in_complex = False
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
					LHS.append('dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.split('-')[-2], molecule.split('-')[-1]))
				elif molecule.startswith('BS-'):
					LHS.append('dna(name = \'{:s}\', type = \'BS\', loc = \'cyt\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.replace('BS-', '')))
				elif molecule.startswith('SMALL-'):
					LHS.append('met(name = \'{:s}\', loc = \'cyt\', prot = met_link)'.format(molecule.replace('SMALL-', '')))
				else:
					LHS.append('prot(name = \'{:s}\', loc = \'cyt\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)'.format(molecule))

			# match the synthesis of RNA in RHS
			if 'ter' not in rna_form[idx+1]:
				LHS.append('None')

			## join complexes
			LHS = connectAgents(agents, LHS)

			## LHS final join
			LHS = ' +\n	'.join(LHS)

			## form the RHS
			agents = ','.join(data['SOURCE'].iloc[0].split(',')[:-1]) + ',' + rna_form[idx+1] + '],' + rna_form[idx]
			names = agents.split(',')

			RHS = []
			next_in_complex = False
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
					RHS.append('dna(name = \'{:s}\', type = \'BS\', loc = \'cyt\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.replace('BS-', '')))
				elif molecule.startswith('SMALL-'):
					RHS.append('met(name = \'{:s}\', loc = \'cyt\', prot = met_link)'.format(molecule.replace('SMALL-', '')))
				else:
					RHS.append('prot(name = \'{:s}\', loc = \'cyt\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)'.format(molecule))

			# synthesis of RNA, except when sliding into a terminator
			if 'ter' not in rna_form[idx+1]:
				if rna_form[idx+1].startswith('BS'):
					RHS.append('rna(name = \'{:s}\', type = \'BS\', loc = \'cyt\', dna = None, met = None, prot = None, rna = None, up = None, dw = None)'.format(
						rna_form[idx+1].replace('BS-', '')))
				else:
					RHS.append('rna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', dna = None, met = None, prot = None, rna = None, up = None, dw = None)'.format(
						rna_form[idx+1].split('-')[0], rna_form[idx+1].split('-')[1]))

			## join complexes
			RHS = connectAgents(agents, RHS)

			## RHS final join
			RHS = ' +\n	'.join(RHS)

			## complete rule
			code = 'Rule(\'sliding_{:d}_{:s}_to_{:s}\',\n' \
				'	{:s} >>\n' \
				'	{:s},\n' \
				'	Parameter(\'fwd_sliding_{:d}_{:s}_to_{:s}\', {:f}))\n'

			code = code.format(
				idx, rna_form[idx], rna_form[idx+1],
				LHS, RHS,
				idx, rna_form[idx], rna_form[idx+1],
				data_arq['RNAP_FWD_SLIDE_RATE'][data_arq['DOWNSTREAM'].replace(']', '').str.match(rna_form[idx+1])].values[0])

			code = code.replace('-', '_')

			if verbose:
				print(code)
			if toFile:
				with open(toFile, 'a+') as outfile:
					outfile.write(code)
			else:
				exec(code)

def polymerase_falloff_rules(data, data_arq, verbose = False, toFile = False):
	RULE_LHS = []
	RULE_RHS = []

	for dna_part1, dna_part2 in zip(data_arq['UPSTREAM'], data_arq['DOWNSTREAM']):
		if 'ter' in dna_part2:
			# data
			agents = (','.join(data['SOURCE'].iloc[0].split(',')[:-1])).replace(']', '') + ',' + dna_part2.replace(']', '') + ']'
			names = agents.split(',')

			## form the LHS
			LHS = []
			next_in_complex = False
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

				if molecule.split('-')[-1][0:3].lower() == 'ter':
					LHS.append('dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.split('-')[-2], molecule.split('-')[-1]))
				elif molecule.startswith('SMALL'):
					LHS.append('met(name = \'{:s}\', loc = \'cyt\', prot = met_link)'.format(molecule.replace('SMALL-', '')))
				else:
					LHS.append('prot(name = \'{:s}\', loc = \'cyt\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)'.format(molecule))

			## join complexes
			LHS = connectAgents(agents, LHS)

			## LHS final join
			LHS = ' +\n	'.join(LHS)
			RULE_LHS.append(LHS)

			# data
			agents = ','.join(data['SOURCE'].iloc[0].split(',')[:-1]) + '],' + dna_part2.replace(']', '')
			names = agents.split(',')

			## form the RHS
			RHS = []
			next_in_complex = False
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

				if molecule.split('-')[-1][0:3].lower() == 'ter':
					RHS.append('dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.split('-')[-2], molecule.split('-')[-1]))
				elif molecule.startswith('SMALL'):
					RHS.append('met(name = \'{:s}\', loc = \'cyt\', prot = met_link)'.format(molecule.replace('SMALL-', '')))
				else:
					RHS.append('prot(name = \'{:s}\', loc = \'cyt\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)'.format(molecule))

			## join complexes
			RHS = connectAgents(agents, RHS)

			## RHS final join
			RHS = ' +\n	'.join(RHS)
			RULE_RHS.append(RHS)

			## complete rule
			code = 'Rule(\'falloff_from_{:s}\', \n' \
				'	{:s} >> \n' \
				'	{:s}, \n' \
				'	Parameter(\'fwd_falloff_from_{:s}\', {:f}))\n'

			code = code.format(
				dna_part2.replace('[', '').replace(']', ''),
				LHS, RHS,
				dna_part2.replace('[', '').replace(']', ''),
				data_arq['RNAP_FWD_FALL_RATE'][data_arq['DOWNSTREAM'].str.match(dna_part2.replace('[', '').replace(']', ''))].values[0])

			code = code.replace('-', '_')

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

def construct_model_from_sigma_specificity_network(promoters, architecture, verbose = False, toFile = False):
	if toFile:
		with open(toFile, 'w') as outfile:
			outfile.write('from pysb import *\nModel()\n\n')

	# check promoters
	if isinstance(promoters, str):
		data_promoters = read_network(promoters)
	elif isinstance(promoters, pandas.DataFrame):
		data_promoters = promoters
	elif isinstance(promoters, numpy.array):
		columns = [
			'SOURCE',
			'TARGET',
			'FWD_DOCK_RATE',
			'RVS_DOCK_RATE',
			'FWD_SLIDE_RATE'
			]
		data_promoters = pandas.DataFrame(data = promoters, columns = columns)
	else:
		raise Exception("The format of the promoter specifities network is not yet supported.")
	data_promoters = check_interaction_network(data_promoters)

	# check architecture
	if isinstance(architecture, str):
		data_architecture = read_network(architecture)
	elif isinstance(architecture, pandas.DataFrame):
		data_architecture = architecture
	elif isinstance(architecture, numpy.array):
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
		data_architecture = pandas.DataFrame(data = architecture, columns = columns)
	else:
		raise Exception("The format of the architecture network is not yet supported.")
	data_architecture = check_genome_graph(data_architecture)

	model = Model()
	monomers_from_genome_graph(data_architecture, verbose, toFile)

	# write docking, slide, and falloff of RNA Polymerase (full form) from DNA:
	polymerase_docking_rules(data_promoters, data_architecture, verbose, toFile)
	polymerase_sliding_from_promoters_rules(data_promoters, data_architecture, verbose, toFile)
	polymerase_sliding_from_others_rules(data_promoters, data_architecture, verbose, toFile)
	polymerase_falloff_rules(data_promoters, data_architecture, verbose, toFile)

	# write docking, slide, and falloff of Ribosome (CPLX alias) from RNA:
	ribosome_docking_rules(data_architecture, verbose, toFile)
	ribosome_sliding_rules(data_architecture, verbose, toFile)
	ribosome_falloff_rules(data_architecture, verbose, toFile)

	# TODO
	# write docking, slide, and falloff of RNASE-CPLX from RNA
	# write docking, slide, and falloff of PROTEASE-CPLX from protein
	observables_from_genome_graph(data_architecture, verbose, toFile)

	if toFile:
		return None
	else:
		return model
