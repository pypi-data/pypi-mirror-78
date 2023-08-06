# -*- coding: utf-8 -*-

'''
Project "Reconstruction of RBM from biological networks", Rodrigo Santibáñez, 2019-2020 @ NBL, UMayor
Citation:
DOI:
'''

__author__  = 'Rodrigo Santibáñez'
__license__ = 'gpl-3.0'

from .construct_model_from_metabolic_network import *
from .construct_model_from_interaction_network import *
from .construct_model_from_genome_graph import *
from .construct_model_from_sigma_specificity_network import *

import re
import pandas

from pysb import *
from pysb.core import *
from pysb.util import alias_model_components

def _combine_two_models(model1, model2, verbose = False):
	# find monomers in common and uniques
	monomer_names1 = []
	for monomer in model1.monomers:
		monomer_names1.append(monomer.name)

	monomer_names2 = []
	for monomer in model2.monomers:
		monomer_names2.append(monomer.name)

	commons = list(set(monomer_names1).intersection(monomer_names2))
	uniques = list(set(monomer_names1).symmetric_difference(monomer_names2))

	if verbose:
		print('common Monomers are: ' + ', '.join(commons))
		print('unique Monomers are: ' + ', '.join(uniques))

	new_monomers = []
	for unique in uniques:
		for monomer in model1.monomers:
			if unique == monomer.name:
				new_monomers.append(str(monomer))
		for monomer in model2.monomers:
			if unique == monomer.name:
				new_monomers.append(str(monomer))

	for common in commons:
		for monomer in model1.monomers:
			if common == monomer.name:
				sites_in_model1 = monomer.sites
				names_in_model1 = monomer.site_states['name']
				if (common == 'dna' or common == 'rna'):
					types_in_model1 = monomer.site_states['type']
				else:
					loc_in_model1 = monomer.site_states['loc']
		for monomer in model2.monomers:
			if common == monomer.name:
				sites_in_model2 = monomer.sites
				names_in_model2 = monomer.site_states['name']
				if (common == 'dna' or common == 'rna'):
					types_in_model2 = monomer.site_states['type']
				else:
					loc_in_model2 = monomer.site_states['loc']

		if (common == 'dna' or common == 'rna'):
			new_monomers.append(
				"Monomer('{:s}', {:s}, {{'name': {:s}, 'loc' : ['cyt'], 'type': {:s}}})".format(
					str(common),
					str(sorted(set(sites_in_model1 + sites_in_model2))),
					str(sorted(set(names_in_model1 + names_in_model2))),
					str(sorted(set(types_in_model1 + types_in_model2)))))
		else:
			new_monomers.append(
				"Monomer('{:s}', {:s}, {{'name': {:s}, 'loc': {:s}}})".format(
					str(common),
					str(sorted(set(sites_in_model1 + sites_in_model2))),
					str(sorted(set(names_in_model1 + names_in_model2))),
					str(sorted(set(loc_in_model1 + loc_in_model2)))))

	new_rules = []
	for rule in model1.rules:
		new_rules.append(str(rule))
	for rule in model2.rules:
		new_rules.append(str(rule))

	new_parameters = []
	for parameter in model1.parameters:
		new_parameters.append(str(parameter))
	for parameter in model2.parameters:
		new_parameters.append(str(parameter))

	new_initials = []
	for initial in model1.initials:
		new_initials.append(str(initial))
	for initial in model2.initials:
		new_initials.append(str(initial))

	new_observables = []
	for observable in model1.observables:
		new_observables.append(str(observable))
	for observable in model2.observables:
		new_observables.append(str(observable))

	#model2.monomers = ComponentSet()
	#model2.parameters = ComponentSet()
	#model2.initials = []
	#model2.rules = ComponentSet()
	#model2.observables = ComponentSet()

	model = Model()

	for new_monomer in new_monomers:
		if verbose:
			print(new_monomer)
		exec(new_monomer)

	df = pandas.DataFrame(data = [ x.split('\'') for x in new_parameters ])
	unique_parameters = [ '\''.join(df.loc[idx]) for idx in df.drop_duplicates([1]).index ]
	for new_parameter in unique_parameters:
		if verbose:
			print(new_parameter)
		exec(new_parameter)

	#alias_model_components(model2)

	df = pandas.DataFrame(data = [ x.split('t0') for x in new_initials ])
	unique_initials = [ 't0'.join(df.loc[idx]) for idx in df.drop_duplicates([1]).index ]
	for new_initial in unique_initials:
		if verbose:
			print(new_initial)
		exec(new_initial)

	for new_rule in sorted(set(new_rules)):
		if verbose:
			print(new_rule)
		exec(new_rule)

	for new_observable in sorted(set(new_observables)):
		if verbose:
			print(new_observable)
		exec(new_observable)

	return model

def combine_models(models, verbose = False):
	if isinstance(models, list):
		pass
	else:
		return models

	model2 = models[-1]
	for model1 in models[0:-1]:
		model2 = _combine_two_models(model1, model2, verbose = verbose)

	return model2

def get_parameter(model, name, verbose = False):
	#print(model.parameters._map[name])
	return model.parameters._map[name]

def replace_parameter(model, name, new_value, verbose = False):
	for i in model.parameters._elements:
		if name == i.name:
			i.value = new_value
	return model

def get_rule(model, name, verbose = False):
	for rule in model.rules:
		if name.replace('-','_') == rule.name:
			#print(rule)
			break

	return rule

def remove_rule(model, name, verbose = False, return_old_rule = False):
	alias_model_components(model)

	# find the rule to delete
	lst = []
	for idx, rule in enumerate(model.rules._map.keys()):
		if rule != name:
			lst.append(model.rules[idx])
		else:
			oldRule = model.rules[idx]

	# remove all rules from model and add all except the rule to delete
	model.rules = ComponentSet()
	for rule in lst:
		model.rules.add(rule)

	if return_old_rule:
		return model, lst, oldRule
	else:
		return model

def replace_rule(model, name, new_rule, verbose = False):
	model = remove_rule(model, name, verbose = verbose)

	if isinstance(new_rule, Rule):
		new_rule = str(new_rule)
	elif isinstance(new_rule, str):
		pass
	else:
		raise "Data type not supported"

	exec(new_rule)
	model.reset_equations()
	if verbose:
		print('Original rule {:s} replaced by {:s}'.format(name, new_rule))

	return model

def modify_rule(model, name, oldString, newString, verbose = False):
	model, lst, oldRule = remove_rule(model, name, return_old_rule = True)

	exec(str(oldRule).replace(oldString, newString))
	model.reset_equations()

	return model

def modify_rules(model, names, oldString, newString, verbose = False):
	if isinstance(names, list):
		pass
	else:
		names = [names]

	for name in names:
		model = modify_rule(model, name, oldString, newString, verbose = verbose)

	return model

def add_regulation(model, name = '', conditions = [], replace = False, verbose = False):
	for rule in model.rules:
		if name.replace('-','_') == rule.name:
			reactant_pattern = str(rule.reactant_pattern)
			product_pattern = str(rule.product_pattern)
			break

	alias_model_components(model)
	monomers = []
	regulators = []
	for condition in conditions:
		cond_monomers = condition.split(',')

		LHS = []
		next_in_complex = False
		for monomer in cond_monomers:
			if monomer[0] == '[': # we are dealing with the first monomer of a complex
				molecule = monomer[1:]
				next_in_complex = True
			elif monomer[-1] == ']': # we are dealing with the last monomer of a complex
				molecule = monomer[:-1]
				next_in_complex = False
			elif next_in_complex: # we are dealing with a monomer part of a complex
				molecule = monomer
			else:
				molecule = monomer

			if molecule.split('-')[-1][0:3].lower() in ['pro', 'rbs', 'cds', 'ter']:
				LHS.append('dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.split('-')[-2], molecule.split('-')[-1]))
			elif molecule.startswith('BS-'):
				LHS.append('dna(name = \'{:s}\', type = \'BS\', loc = \'cyt\', prot = dna_link, up = bs_link, dw = bs_link)'.format(molecule.replace('BS-', '')))
				regulators.append(molecule.split('-')[1])
			elif molecule.startswith('SMALL'):
				LHS.append('met(name = \'{:s}\', loc = \'cyt\', prot = met_link)'.format(molecule.replace('SMALL-', '')))
			else:
				LHS.append('prot(name = \'{:s}\', loc = \'cyt\', dna = dna_link, met = met_link, up = prot_link, dw = prot_link)'.format(molecule))

		LHS = connectAgents(condition, LHS)
		LHS = ' '.join(LHS)
		monomers.append(LHS)

	reactant_pattern = ' +\n\t'.join(monomers + [reactant_pattern])
	product_pattern = ' +\n\t'.join(monomers + [product_pattern])
	regulators = '_and_'.join(regulators)
	name = '{:s}_regulated_by_{:s}'.format(name, regulators)

	code = 'Rule(\'{:s}\',\n\t{:s} |\n\t{:s},\n\tParameter(\'fwd_{:s}\', 0),\n\tParameter(\'rvs_{:s}\', 0))'.format(name, reactant_pattern, product_pattern, name, name)
	code = code.replace('-', '_')

	if verbose:
		print(code)
	exec(code)

	if replace:
		model = remove_rule(model, name, verbose = verbose)

	return model

def add_rule(model, new_rule):
	alias_model_components(model)
	exec(new_rule)

	return model
