# -*- coding: utf-8 -*-

'''
Project "Reconstruction of RBM from biological networks", Rodrigo Santibáñez, 2019-2020 @ NBL, UMayor
Citation:
DOI:
'''

__author__  = 'Rodrigo Santibáñez'
__license__ = 'gpl-3.0'

from pysb import *
from pysb.bng import generate_network, generate_equations
from pysb.pathfinder import set_path
from pysb.simulator import ScipyOdeSimulator, BngSimulator, CupSodaSimulator, KappaSimulator, StochKitSimulator
from pysb.util import alias_model_components
from matplotlib.pylab import linspace

import pandas
import seaborn
import matplotlib.pyplot as plt

def set_parameter(model, name, new_value):
	for i in model.parameters._elements:
		if name == i.name:
			i.value = new_value
	return model

def set_observable(model, pattern = '', alias = ''):
	model = alias_model_components(model)
	exec('Observable(\'' + alias + '\',' + pattern + ')')
	return model

class set_initial:
	def monomers(model, name, type, loc = 'cyt', new_value = 0):
		notFound = True
		for i in model.parameters._elements:
			if name.startswith('t0_met_') or name.startswith('t0_prot_') or name.startswith('t0_cplx_'):
				if name + '_' + loc.lower() == i.name:
					i.value = new_value
					notFound = False
			elif name.startswith('t0_dna_') or name.startswith('t0_rna'):
				if name == i.name:
					i.value = new_value
					notFound = False

		if notFound:
			print('Initial not found. Creating Initial...'.format(name))
		return model, notFound

	def cplx(model, name, loc = 'cyt', new_value = 0):
		model, notFound = set_initial.monomers(model, 't0_cplx_' + name, '', loc, new_value)
		if notFound:
			model = alias_model_components(model)
			exec('Initial(cplx(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = None, dw = None), ' \
				'Parameter(\'t0_cplx_{:s}_{:s}\', {:f}))'.format(name, loc.lower(), name, loc.lower(), new_value))
			exec('Observable(\'obs_cplx_{:s}_{:s}\', ' \
				'cplx(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = None, dw = None))'.format(name, loc.lower(), name, loc.lower()))
		return model

	def dna(model, name, type = '', loc = 'cyt', new_value = 0):
		model, notFound = set_initial.monomers(model, 't0_dna_' + name, type, loc, new_value)
		if notFound:
			model = alias_model_components(model)
			exec('Initial(dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', dna = None, met = None, prot = None, rna = None, up = None, dw = None), ' \
				'Parameter(\'t0_dna_{:s}\', {:f}))'.format(name, type, name, new_value))
			exec('Observable(\'obs_dna_{:s}_{:s}\', ' \
				'dna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', dna = None, met = None, prot = None, rna = None, up = ANY, dw = ANY))'.format(name, type, name, type))
		return model

	def met(model, name, loc = 'cyt', new_value = 0):
		if name[0].isdigit():
			name = '_' + name
		model, notFound = set_initial.monomers(model, 't0_met_' + name, '', loc, new_value)
		if notFound:
			model = alias_model_components(model)
			exec('Initial(met(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None), ' \
				'Parameter(\'t0_dna_{:s}_{:s}\', {:f}))'.format(name, loc.lower(), name, loc.lower(), new_value))
			exec('Observable(\'obs_met_{:s}_{:s}\', ' \
				'met(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None))'.format(name, loc.lower(), name, loc.lower()))
		return model

	def prot(model, name, loc = 'cyt', new_value = 0):
		model, notFound = set_initial.monomers(model, 't0_prot_' + name, '', loc, new_value)
		if notFound:
			model = alias_model_components(model)
			exec('Initial(prot(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = None, dw = None), ' \
				'Parameter(\'t0_prot_{:s}_{:s}\', {:f}))'.format(name, loc.lower(), name, loc.lower(), new_value))
			exec('Observable(\'obs_prot_{:s}_{:s}\', ' \
				'prot(name = \'{:s}\', loc = \'{:s}\', dna = None, met = None, prot = None, rna = None, up = None, dw = None))'.format(name, loc.lower(), name, loc.lower()))
		return model

	def rna(model, name, type = '', loc = 'cyt', new_value = 0):
		model, notFound = set_initial.monomers(model, 't0_rna_' + name, type, loc, new_value)
		if notFound:
			model = alias_model_components(model)
			exec('Initial(rna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', dna = None, met = None, prot = None, rna = None, up = None, dw = None), ' \
				'Parameter(\'t0_rna_{:s}\', {:f}))'.format(name, type, name, new_value))
			exec('Observable(\'obs_rna_{:s}_{:s}\', ' \
				'rna(name = \'{:s}\', type = \'{:s}\', loc = \'cyt\', dna = None, met = None, prot = None, rna = None, up = ANY, dw = ANY))'.format(name, type, name, type))
		return model

	def from_pattern(model, pattern, alias = 'alias_pattern', new_value = 0):
		model = alias_model_components(model)
		exec('Initial(' + pattern + ', Parameter(\'t0_' + alias + '\', ' + str(new_value) + '))')
		return model

def scipy(model, start = 0, finish = 10, points = 10):
	return ScipyOdeSimulator(model, linspace(start, finish, points+1)).run().dataframe

def bngODE(model, start = 0, finish = 10, points = 10, path = '/opt/'):
	set_path('bng', path)
	return BngSimulator(model, linspace(start, finish, points+1)).run(method = 'ode').dataframe

def cupsoda(model, start = 0, finish = 10, points = 10, path = '/opt/´'):
	set_path('cupsoda', path)
	return CupSodaSimulator(model, linspace(start, finish, points+1)).run().dataframe

def modes(sims, n_runs):
	data = []
	for i in range(n_runs):
		data.append(sims.xs(i))

	avrg = 0
	for i in range(n_runs):
		avrg += data[i]
	avrg = avrg / n_runs

	stdv = 0
	for i in range(n_runs):
		stdv += (data[i] - avrg)**2
	stdv = (stdv / (n_runs-1))**0.5

	return {'sims' : data, 'avrg' : avrg, 'stdv' : stdv}

def bngSSA(model, start = 0, finish = 10, points = 10, n_runs = 20, path = '/opt/'):
	set_path('bng', path)

	sims = BngSimulator(model, linspace(start, finish, points+1)).run(method = 'ssa', n_runs = n_runs).dataframe
	sims = modes(sims, n_runs)
	return {'sims' : sims['sims'], 'avrg' : sims['avrg'], 'stdv' : sims['stdv']}

def bngPLA(model, start = 0, finish = 10, points = 10, n_runs = 20, path = '/opt/'):
	set_path('bng', path)

	sims = BngSimulator(model, linspace(start, finish, points+1)).run(method = 'pla', n_runs = n_runs).dataframe
	sims = modes(sims, n_runs)
	return {'sims' : sims['sims'], 'avrg' : sims['avrg'], 'stdv' : sims['stdv']}

def bngNF(model, start = 0, finish = 10, points = 10, n_runs = 20, path = '/opt/'):
	set_path('bng', path)

	sims = BngSimulator(model, linspace(start, finish, points+1)).run(method = 'nf', n_runs = n_runs).dataframe
	sims = modes(sims, n_runs)
	return {'sims' : sims['sims'], 'avrg' : sims['avrg'], 'stdv' : sims['stdv']}

def kasim(model, start = 0, finish = 10, points = 10, n_runs = 20, path = '/opt/'):
	set_path('kasim', path)
	sims = KappaSimulator(model, linspace(start, finish, points+1)).run(n_runs = n_runs).dataframe
	sims = modes(sims, n_runs)
	return {'sims' : sims['sims'], 'avrg' : sims['avrg'], 'stdv' : sims['stdv']}

def stochkit(model, start = 0, finish = 10, points = 10, n_runs = 20, path = '/opt/'):
	set_path('stochkit_ssa', path)
	sims = StochKitSimulator(model, linspace(start, finish, points+1)).run(n_runs = n_runs).dataframe
	sims = modes(sims, n_runs)
	return {'sims' : sims['sims'], 'avrg' : sims['avrg'], 'stdv' : sims['stdv']}

class plot:
	def monomer(data, observable, loc = 'cyt', ax = plt, plt_kws = {}, *args, **kwargs):
		kind = kwargs.get('kind', None)
		weight = kwargs.get('weight', 1)

		observable = observable.replace('-', '_')
		if kind == 'plot':
			try:
				plt_kws['markersize'] = plt_kws.pop('s')
			except:
				pass
			ax.plot(data.index, data[observable], **plt_kws)
		elif kind == 'scatter':
			try:
				plt_kws['s'] = plt_kws.pop('markersize')
			except:
				pass
			ax.scatter(data.index, data[observable], **plt_kws)
		elif kind == 'fill_between':
			try:
				plt_kws['linewidth'] = plt_kws.pop('s')
			except:
				pass
			ax.fill_between(
				data['avrg'].index,
				data['avrg'][observable] + data['stdv'][observable] * weight,
				data['avrg'][observable] - data['stdv'][observable] * weight,
				**plt_kws)
		else:
			try:
				plt_kws['markersize'] = plt_kws.pop('s')
			except:
				pass
			ax.plot(data.index, data[observable], **plt_kws)

		try:
			ax.legend(frameon = False, loc = 'best')
		except:
			pass
		return None

	def dna(data, observable, *args, **kwargs):
		plot.monomer(data, 'obs_dna_' + observable, *args, **kwargs)
		return None

	def metabolite(data, observable, loc = 'cyt', *args, **kwargs):
		if observable[0].isdigit():
			observable = '_' + observable
		plot.monomer(data, 'obs_met_' + observable + '_' + loc.lower(), *args, **kwargs)
		return None

	def protein(data, observable, loc = 'cyt', *args, **kwargs):
		plot.monomer(data, 'obs_prot_' + observable + '_' + loc.lower(), *args, **kwargs)
		return None

	def cplx(data, observable, loc = 'cyt', *args, **kwargs):
		plot.monomer(data, 'obs_cplx_' + observable + '_' + loc.lower(), *args, **kwargs)
		return None

	def rna(data, observable, *args, **kwargs):
		plot.monomer(data, 'obs_rna_' + observable, *args, **kwargs)
		return None

	def pattern(data, observable, plt_kws = {}, *args, **kwargs):
		plt.plot(data.index, data[observable], **plt_kws)
		try:
			plt.legend(frameon = False, loc = 'right')
		except:
			pass
		return None
