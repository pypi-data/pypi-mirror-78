# -*- coding: utf-8 -*-

'''
Project "Reconstruction of RBM from biological networks", Rodrigo Santibáñez, 2019-2020 @ NBL, UMayor
Citation:
DOI:
'''

__author__  = 'Rodrigo Santibáñez'
__license__ = 'gpl-3.0'

import io
import os
import re
import numpy
import pandas
import pythoncyc
import subprocess
import itertools

def read_network(infile_path):
	with open(infile_path, 'r') as infile:
		data = pandas.read_csv(infile, delimiter = '\t', header = 0, comment = '#')

	return data

def check_metabolic_network(data):
	# find duplicated reactions (reactions must has a unique name)
	duplicated = len(data[data.duplicated(['REACTION'])].index)

	if duplicated > 0:
		data[data.duplicated(['REACTION'])].to_csv('./conflicting_reactions.txt', sep = '\t', index = False)
		data = data[~data.duplicated(['REACTION'], keep = 'first')]
		print('It was found duplicated reaction names in the network.\n' \
			'Please check the conflicting_reactions.txt and correct them if necessary.')

	return data

def check_interaction_network(data):
	# find duplicated reactions (reactions must has a unique name)
	duplicated = len(data[data.duplicated(['SOURCE', 'TARGET'])].index)

	if duplicated > 0:
		data[data.duplicated(['SOURCE', 'TARGET'])].to_csv('./conflicting_interactions.txt', sep = '\t', index = False)
		data = data[~data.duplicated(['SOURCE', 'TARGET'], keep = 'first')]
		print('It was found possible duplicated interactions in the network.\n' \
			'Please check the conflicting_interactions.txt and correct them if necessary.')

	return data

def check_genome_graph(data):
	# find duplicated reactions (reactions must has a unique name)
	duplicated = len(data[data.duplicated(['UPSTREAM', 'DOWNSTREAM'])].index)

	if duplicated > 0:
		data[data.duplicated(['UPSTREAM', 'DOWNSTREAM'])].to_csv('./conflicting_interactions.txt', sep = '\t', index = False)
		data = data[~data.duplicated(['UPSTREAM', 'DOWNSTREAM'], keep = 'first')]
		print('It was found possible duplicated interactions in the network.\n' \
			'Please check the conflicting_interactions.txt and correct them if necessary.')

	return data

def connectAgents(agents, lst):
	## look for where starts and ends a complex in the list of agents
	complexes = [(m.start()+1, m.end()-1) for m in re.finditer(r'\[[A-Za-z0-9-_, ]+\]', agents)]
	monomers = [(m.start(), m.end()) for m in re.finditer(r'[A-Za-z0-9-_]+', agents)]

	positions = []
	for cplx_pos in reversed(complexes):
		pos_i = None
		pos_f = None
		for index, kmer_pos in enumerate(monomers):
			if cplx_pos[0] == kmer_pos[0]:
				pos_i = index
			if cplx_pos[1] == kmer_pos[1]:
				pos_f = index
				positions.append((pos_i, pos_f))
				break

	## join complexes following start and end positions
	for position in positions:
		## join two agents and remove them from the LHS or the RHS list because they were merged into one position
		lst[position[0]] = ' %\n	'.join(lst[position[0]:position[1]+1])
		for index in reversed(range(position[0]+1, position[1]+1)):
			lst.pop(index)

	## create numbered links
	starter_link = 1
	for index, agent in enumerate(lst):
		count_small = agent.count('met(')
		count_prots = agent.count('prot(')
		count_dnas = agent.count('dna(')

		if count_prots > 1:
			dw = [None] * count_prots
			for prot_index in range(count_prots-1):
				dw[prot_index] = starter_link
				starter_link += 1
			up = dw[-1:] + dw[:-1]
			## and replace indexes
			c = list(zip(up, dw))
			c = [elt for sublist in c for elt in sublist]
			lst[index] = lst[index].replace('prot_link', '{}').format(*c)

		if count_small >= 1 and count_prots >= 1:
			dw = [None] * (count_small + count_prots)
			if count_small % 2 == 0:
				number = 2
			else:
				number = 3
			for met_index in numpy.arange(0, count_small + count_prots, number):
				dw[met_index] = starter_link
				dw[met_index-1] = starter_link
				starter_link += 1
			## and replace indexes
			lst[index] = lst[index].replace('met_link', '{}').format(*tuple(dw))

		if count_dnas > 1:
			dw = ['WILD'] * count_dnas
			#for dna_index in range(count_dnas-1):
				#dw[dna_index] = starter_link
				#starter_link += 1
			up = dw[-1:] + dw[:-1]
			## and replace indexes
			c = list(zip(up, dw))
			c = [elt for sublist in c for elt in sublist]
			lst[index] = lst[index].replace('bs_link', '{}').format(*c)

		if count_dnas >= 1 and count_prots >= 1: # a protein is complexed with the dna
			dw = [None] * (count_prots + count_dnas)
			for dna_index in range(count_prots + count_dnas):
				if dna_index == count_prots:
					dw[dna_index] = starter_link
					dw[dna_index-1] = starter_link
					starter_link += 1
			## and replace indexes
			lst[index] = lst[index].replace('True', 'False').replace('dna_link', '{}').format(*dw)

		## final replace
		lst[index] = lst[index].replace('prot_link', 'None')
		lst[index] = lst[index].replace('met_link', 'None')
		lst[index] = lst[index].replace('bs_link', 'WILD')
		lst[index] = lst[index].replace('dna_link', 'None')

	return lst

def checkPathwayTools(verbose = True):
	try:
		availableOrgs = pythoncyc.all_orgids()
	except:
		availableOrgs = False

	if availableOrgs:
		if verbose:
			print('PathwayTools is running. Available PGDB are: {:s}'.format(', '.join(availableOrgs)).replace('|',''))
		return True
	else:
		if verbose:
			print('PathwayTools is not running.\n' \
				'Please, execute execPathwayTools(path) or execPToolsDocker(dockername).')
		return False

def execPathwayTools(path = '/opt/pathway-tools/'):
	if not checkPathwayTools(verbose = False):
		from platform import system
		if 'Windows' in system():
			cmd = '"{:s}\ptools.bat" -lisp -python-local-only'.format(path)
		else:
			cmd = 'nohup {:s}/pathway-tools -lisp -python-local-only &'.format(path)
		cmd = re.findall(r'(?:[^\s,"]|"+(?:=|\\.|[^"])*"+)+', cmd)
		out, err = subprocess.Popen(cmd, shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
		print('PathwayTools is running in background.')
	else:
		print('Doing nothing since PathwayTools is running.')
		return None
	while not checkPathwayTools(verbose = False):
		pass
	checkPathwayTools(verbose = True)
	return None

def execPToolsDocker(dockername = 'ptools', path = '/opt'):
	# Ubuntu 20.04 and 18.04 bug
	if not checkPathwayTools(verbose = False):
		from platform import system
		if 'Linux' in system():
			pass
		else:
			return "Please run execPathwayTools()"

	if not checkPathwayTools(verbose = False):
		cmd = 'docker run --rm --detach --volume {:s}:{:s} --network host {:s}'.format(path, path, dockername)
		cmd = re.findall(r'(?:[^\s,"]|"+(?:=|\\.|[^"])*"+)+', cmd)
		out, err = subprocess.Popen(cmd, shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
		print('Docker {:s} is running (ID {:s})'.format(dockername, out.decode()[:-1]))
	else:
		print('Doing nothing since PathwayTools is running.')
		return None

	while not checkPathwayTools(verbose = False):
		pass
	checkPathwayTools(verbose = True)
	return None

def selectOrganism(code):
	if checkPathwayTools(verbose = False):
		return pythoncyc.select_organism(code)

def returnGenes(code):
	organism = selectOrganism(code)
	genes = [ x.frameid for x in organism.genes.instances ]
	return genes

def returnCommonNames(code):
	genes = returnGenes(code)
	# and common names
	common_names = []

	genes_dict = {}
	for gene in genes:
		common = getData(code, gene)['common_name']
		common_names.append(common)
		genes_dict[common] = gene

	return pandas.DataFrame(index = common_names, columns = ['gene name'], data = genes)

# a complicated function to deal with many situations when retrieving data
# some functions in PythonCyc accept lists (and return a list), but not all,
# so instead of, we traverse the input and output lists and append results to a new list
def getData(code, string, verbose = False):
	organism = selectOrganism(code)

	if verbose:
		print('query is', string)

	if isinstance(string, list) and len(string) > 1:
		info = []
		for query in string:
			if query != None:
				data = organism.get_frame_objects(query)
				if data != None:
					info.append(data[0])
				else:
					info.append(None)
			else:
				info.append(None)
		return info

	elif isinstance(string, list) and len(string) == 1:
		if string[0] != None:
			data = organism.get_frame_objects(string)
			if data != None:
				return data[0]
			else:
				return [None]
		else:
			return [None]

	elif isinstance(string, str):
		if string != None:
			data = organism.get_frame_objects([string])
			if data != None:
				return data[0]
			else:
				return [None]
		else:
			return [None]

	else:
		return [None]

def analyzeConnectivity(model, path = 'kasa'):
	import pysb
	from .export import to_kappa

	if isinstance(model, str):
		cmd = '{:s} {:s}'.format(path, model)
	elif isinstance(model, pysb.core.Model):
		import string, random
		name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
		to_kappa(model, '_{:s}.kappa'.format(name))
		cmd = '{:s} _{:s}.kappa'.format(path, name)
	else:
		raise Exception('Type of model not supported yet.')

	cmd = re.findall(r'(?:[^\s,"]|"+(?:=|\\.|[^"])*"+)+', cmd)
	out, err = subprocess.Popen(cmd, shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
	#print(out, err)

	output = out.replace(b'\r', b'').split(b'------------------------------------------------------------') # Windows compatibility
	if output[1] == b'\nevery rule may be applied\n':
		print('Every rule may be applied.')
	else:
		print('There are some non applicable rules:', output[2].decode())
	if output[2] == b'\nevery agent may occur in the model\n\n' or output[3] == b'\nevery agent may occur in the model\n\n':
		print('Every monomer and complex of monomers may occur in the model.')
		try:
			os.remove('_{:s}.kappa'.format(name))
		except:
			pass
	else:
		print('There are some non creatable agents:', output[4].decode()[:-2])

	try:
		os.remove('output/contact.dot')
		os.remove('output/influence.dot')
		os.remove('output/profiling.html')
		os.rmdir('output')
	except:
		print('Another process could be holding the files/directories and preventing its deletion.')

	return None

def analyseConnectivity(model, path = 'kasa'):
	analyzeConnectivity(model, path)

	return None

def location_keys():
	dct = {
		'CYT' : 'cytosol',
		'iMEM' : 'inner membrane',
		'PER' : 'periplasmic space',
		'MEM' : 'membrane',
		'oMEM' : 'outer membrane',
		'EX' : 'extracellular space',
		'bNUC' : 'bacterial nucleoid',
		'WALL' : 'cell wall',
		'cPROJ' : 'cell projection',
		'CYTOSK' : 'cytoskeleton',
		}

	return dct

def location_values():
	dct = {
		'unknown' : 'CYT',
		'cytosol' : 'CYT',
		'inner membrane' : 'iMEM',
		'inner membrane (sensu Actinobacteria)' : 'iMEM',
		'inner membrane (sensu Gram-negative Bacteria)' : 'iMEM',
		'periplasmic space' : 'PER',
		'membrane' : 'MEM',
		'outer membrane' : 'oMEM',
		'extracellular space' : 'EX',
		'bacterial nucleoid' : 'bNUC',
		'cell wall' : 'WALL',
		'cell projection' : 'cPROJ',
		'cytoskeleton' : 'CYTOSK',
		}

	return dct

class metabolicNetwork:
	def FromGeneList(code, genes, fmt = 'genes', precalculated = None):
		if fmt not in ['genes', 'product', 'complex']:
			raise Exception('Valid format is: \'genes\', \'product\', and \'complex\'')

		if isinstance(genes, str):
			genes = [genes]
		elif isinstance(genes, list):
			genes = genes
		else:
			raise Exception('Not supported data type yet.')

		# remove duplicated queries
		genes = sorted(set(genes))

		if precalculated is None:
			df_genes = returnCommonNames(code)
		else:
			df_genes = precalculated

		Network = ''
		# get reactions of product of gene, and complexes of product of gene:
		for gene in genes:
			rxns = []
			prods = getData(code, df_genes.loc[gene, 'gene name'])['product'] # always a list

			if prods != None:
				for prod in prods:
					enzrxns = getData(code, prod)['catalyzes'] # always a list

					if enzrxns != None:
						for enzrxn in enzrxns:
							rxns.append([prod, getData(code, enzrxn)['reaction'][0]])
		#             print(idx, '\t', name, '\t', prod, rxns)

					component_of = getData(code, prod)['component_of'] # always a list
					if component_of != None:
						for component in component_of:
							enzrxns = getData(code, component)['catalyzes']
							if enzrxns != None:
								for enzrxn in enzrxns:
									rxns.append([component, getData(code, enzrxn)['reaction'][0]])
		#                     print(idx, '\t', name, '\t', component, rxns)

							component_of = getData(code, component)['component_of'] # always a list
							if component_of != None:
								for component in component_of:
									enzrxns = getData(code, component)['catalyzes']
									if enzrxns != None:
										for enzrxn in enzrxns:
											rxns.append([component, getData(code, enzrxn)['reaction'][0]])
		#                             print(idx, '\t', name, '\t', component, rxns)

									component_of = getData(code, component)['component_of'] # always a list
									if component_of != None:
										for component in component_of:
											enzrxns = getData(code, component)['catalyzes']
											if enzrxns != None:
												for enzrxn in enzrxns:
													rxns.append([component, getData(code, enzrxn)['reaction'][0]])
		#                                     print(idx, '\t', name, '\t', component, rxns)

											# CPLX0-3964 found in this level (ECOLI)
											component_of = getData(code, component)['component_of'] # always a list
											if component_of != None:
												for component in component_of:
													enzrxns = getData(code, component)['catalyzes']
													if enzrxns != None:
														for enzrxn in enzrxns:
															rxns.append([component, getData(code, enzrxn)['reaction'][0]])
		#                                             print(idx, '\t', name, '\t', component, rxns)

			# we got all reactions from the product of a gene, now we format the network
			for prod, rxn in rxns:
				direction = getData(code, rxn)['reaction_direction']
				if direction == '|PHYSIOL-LEFT-TO-RIGHT|' or direction == '|LEFT-TO-RIGHT|':
					fwd = 1.0
					rvs = 0.0
				elif direction == '|PHYSIOL-RIGHT-TO-LEFT|' or direction == '|RIGHT-TO-LEFT|':
					fwd = 0.0
					rvs = 1.0
				elif direction == '|REVERSIBLE|':
					fwd = 1.0
					rvs = 1.0
				else:
					fwd = 1.0
					rvs = 0.0

				left = ','.join(getData(code, rxn)['left'])
				right = ','.join(getData(code, rxn)['right'])

				# location of genes products, but no complexes
				if 'genes' in fmt or 'product' in fmt:
					products = getData(code, df_genes.loc[gene, 'gene name'])['product']
					locations = []
					for product in products:
						locations.append(getData(code, product)['locations'])

				if 'genes' in fmt:
					for loc in locations[0]:
						location = getData(code, loc)['common_name']
						Network += '{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:f}\t{:f}\n'.format(gene, location, rxn, left, right, fwd, rvs)

				elif 'product' in fmt:
					for loc in locations[0]:
						location = getData(code, loc)['common_name']
						Network += '{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:f}\t{:f}\n'.format(prod, location, rxn, left, right, fwd, rvs)

				elif 'complex' in fmt:
					organism = selectOrganism(code)
					genes = organism.genes_of_protein(prod)
					monomers, stoichiometry = organism.monomers_of_protein(prod)
					locations = []
					for monomer in monomers:
						locations.append(getData(code, monomer)['locations'])

					import itertools
					locations = list(itertools.product(*locations))

					for location in locations:
						tmp = []
						for loc, coefficient in zip(location, stoichiometry):
							tmp.append([getData(code, loc)['common_name'] for x in range(coefficient)])
						loc = [x for y in tmp for x in y]

						if len(loc) > 1:
							loc = ','.join(loc)
							loc = '[{:s}]'.format(loc)
						else:
							loc = loc[0]

						cplx = []
						for gene, coefficient in zip(genes, stoichiometry):
							cplx.append([getData(code, gene)['common_name'] for x in range(coefficient)])
						cplx = [x for y in cplx for x in y]

						if len(cplx) > 1:
							cplx = ','.join(cplx)
							cplx = '[{:s}]'.format(cplx)
						else:
							cplx = cplx[0]

						Network += '{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:f}\t{:f}\n'.format(cplx, loc, rxn, left, right, fwd, rvs)

		infile = io.StringIO(Network.replace('|',''))
		header = ['GENE OR COMPLEX', 'ENZYME LOCATION', 'REACTION', 'SUBSTRATES', 'PRODUCTS', 'FWD_RATE', 'RVS_RATE']
		return pandas.read_csv(infile, delimiter = '\t', names = header)

	def FromEnzymeList(code, enzymes, fmt = 'product'):
		if fmt not in ['genes', 'product', 'complex']:
			raise Exception('Valid format is: \'genes\', \'product\', and \'complex\'')

		# check data type
		if isinstance(enzymes, str):
			enzymes = [enzymes]
		elif isinstance(enzymes, list):
			enzymes = enzymes
		else:
			raise Exception('Not supported data type yet.')

		# remove duplicated queries
		enzymes = sorted(set(enzymes))

		Network = ''
		# get reactions of gene:
		for enzyme in enzymes:
			enzrnxs = getData(code, enzyme)['catalyzes']

			if enzrnxs == None:
				print('Code {:s} is not an enzyme. ' \
					'Please check spelling or post an issue with the information of https://ecocyc.org/{:s}/NEW-IMAGE?object={:s}'.format(enzyme, code, enzyme))
			else:
				try:
					rxns = []
					for enzrxn in enzrnxs:
						rxns.append(getData(code, enzrxn)['reaction'])

					for rxn in rxns:
						# reversibility of reactions
						direction = getData(code, rxn[0])['reaction_direction']
						if direction == '|PHYSIOL-LEFT-TO-RIGHT|' or direction == '|LEFT-TO-RIGHT|':
							fwd = 1.0
							rvs = 0.0
						elif direction == '|PHYSIOL-RIGHT-TO-LEFT|' or direction == '|RIGHT-TO-LEFT|':
							fwd = 0.0
							rvs = 1.0
						elif direction == '|REVERSIBLE|':
							fwd = 1.0
							rvs = 1.0
						else:
							fwd = 1.0
							rvs = 0.0

						left = ','.join(getData(code, rxn)['left'])
						right = ','.join(getData(code, rxn)['right'])

						organism = selectOrganism(code)
						genes = organism.genes_of_protein(enzyme)
						monomers, stoichiometry = organism.monomers_of_protein(enzyme)

						# format network
						if 'gene' in fmt:
							for gene in genes:
								name = getData(code, gene)['common_name']
								products = getData(code, gene)['product']
								if isinstance(products, list):
									for product in products:
										locations = getData(code, product)['locations']
										if locations != None:
											for location in locations:
												loc = getData(code, location)['common_name']
												Network += '{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:f}\t{:f}\n'.format(name, loc, rxn[0], left, right, fwd, rvs)
										else:
											Network += '{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:f}\t{:f}\n'.format(name, 'unknown', rxn[0], left, right, fwd, rvs)

						elif 'product' in fmt:
							locations = getData(code, enzyme)['locations']
							if isinstance(locations, list):
								for location in locations:
									loc = getData(code, location)['common_name']
									Network += '{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:f}\t{:f}\n'.format(enzyme, loc, rxn[0], left, right, fwd, rvs)
							else:
								for monomer in monomers:
									locations = getData(code, monomer)['locations']
									if locations != None:
										for location in locations:
											loc = getData(code, location)['common_name']
											Network += '{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:f}\t{:f}\n'.format(enzyme, loc, rxn[0], left, right, fwd, rvs)
									else:
										Network += '{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:f}\t{:f}\n'.format(enzyme, 'unknown', rxn[0], left, right, fwd, rvs)

						elif 'complex' in fmt:
							locations = []
							for monomer in monomers:
								locations.append(getData(code, monomer)['locations'])

							if locations[0] != None:
								import itertools
								locations = list(itertools.product(*locations))

								for location in locations:
									tmp = []
									for loc, coefficient in zip(location, stoichiometry):
										tmp.append([getData(code, loc)['common_name'] for x in range(coefficient)])
									loc = [x for y in tmp for x in y]

									if len(loc) > 1:
										loc = ','.join(loc)
										loc = '[{:s}]'.format(loc)
									else:
										loc = loc[0]

									cplx = []
									for gene, coefficient in zip(genes, stoichiometry):
										cplx.append([getData(code, gene)['common_name'] for x in range(coefficient)])
									cplx = [x for y in cplx for x in y]

									if len(cplx) > 1:
										cplx = ','.join(cplx)
										cplx = '[{:s}]'.format(cplx)
									else:
										cplx = cplx[0]

									Network += '{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:f}\t{:f}\n'.format(cplx, loc, rxn[0], left, right, fwd, rvs)
							else:
								Network += '{:s}\t{:s}\t{:s}\t{:s}\t{:s}\t{:f}\t{:f}\n'.format('unknown', 'unknown', rxn[0], left, right, fwd, rvs)

				except:
					enzyme = enzyme.replace('|', '')
					print(
						'Unable to retrieve data for {:s}. ' \
						'Please, review the information at https://biocyc.org/{:s}/NEW-IMAGE?object={:s} ' \
						'and post an issue at https://github.com/networkbiolab/atlas if you believe it is a software error.'.format(enzyme, code, enzyme))

		infile = io.StringIO(Network.replace('|',''))
		header = ['GENE OR COMPLEX', 'ENZYME LOCATION', 'REACTION', 'SUBSTRATES', 'PRODUCTS', 'FWD_RATE', 'RVS_RATE']
		return pandas.read_csv(infile, delimiter = '\t', names = header)

	def addReaction(network, gene = 'spontaneous', location = [], reaction = 'RXN-', substrates = [], products = [], fwd_rate = 1.0, rvs_rate = 1.0):
		if reaction == 'RXN-':
			import string, random
			name = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
			reaction = reaction + name

		if isinstance(location, list):
			for loc in locations:
				if loc not in list(set(location_keys().keys())):
					warning = True

			if warning:
				print('At least one location could not be set. See utils.location_keys().keys() for valid identifiers of location.')
				return network

			location = [location_keys()[loc] for loc in location]
			location = ','.join(location)

		if isinstance(substrates, list):
			substrates = ','.join(substrates)

		if isinstance(products, list):
			products = ','.join(products)

		network = network.append({
			'GENE OR COMPLEX' : gene,
			'ENZYME LOCATION' : location,
			'REACTION' : reaction,
			'SUBSTRATES' : substrates,
			'PRODUCTS' : products,
			'FWD_RATE' : fwd_rate,
			'RVS_RATE' : rvs_rate
			}, ignore_index = True)

		return network

	def removeReaction(network, index = [], genes = [], reactions = []):
		if len(index) > 0:
			network = network.drop(labels = index, axis = 0)

		if len(genes) > 0:
			index = network.loc[network['GENE OR COMPLEX'].str.match(genes)].index
			network = network.drop(labels = index, axis = 0)

		if len(reactions) > 0:
			index = network.loc[network['REACTION'].str.match(reactions)].index
			network = network.drop(labels = index, axis = 0)

		return network

	def setReversibility(network, rxnLst, valLst):
		if isinstance(rxnLst, list):
			pass
		else:
			rxnLst = [rxnLst]

		if isinstance(valLst, list):
			pass
		else:
			valLst = [valLst]

		if not len(rxnLst) == len(valLst):
			raise Exception('Reactions and its rates do not have the same length')

		for reaction, rvs_rate in zip(rxnLst, valLst):
			network.loc[network['REACTION'].str.match(reaction), 'RVS_RATE'] = rvs_rate
		return network

	def setIrreversibility(network, rxnLst = [], geneLst = []):
		if isinstance(rxnLst, list):
			pass
		else:
			rxnLst = [rxnLst]

		if isinstance(geneLst, list):
			pass
		else:
			geneLst = [geneLst]

		for reaction in rxnLst:
			network.loc[network['REACTION'].str.match(reaction), 'RVS_RATE'] = 0.0

		for gene_or_cplx in geneLst:
			network.loc[network['GENE OR COMPLEX'].str.match(gene_or_cplx.replace('[', '\[').replace(']', '\]')), 'RVS_RATE'] = 0.0

		return network

	def setTransport(network, rxnLst = [], geneLst = [], fromLst = [], toLst = []):
		if isinstance(rxnLst, list):
			pass
		else:
			rxnLst = [rxnLst]

		if isinstance(geneLst, list):
			pass
		else:
			geneLst = [geneLst]

		if isinstance(fromLst, list):
			pass
		else:
			fromLst = [fromLst]

		if isinstance(toLst, list):
			pass
		else:
			toLst = [toLst]

		if len(rxnLst) > 0:
			col = 'REACTION'
			lst = rxnLst
		elif len(geneLst) > 0:
			col = 'GENE OR COMPLEX'
			lst = geneLst

		if len(lst) > 0 and len(fromLst) > 0:
			for reaction, c1 in zip(lst, fromLst):
				# check
				if c1 not in ['CYT', 'PER', 'EX']:
					break
				else:
					idx = network.loc[network[col].str.match(reaction), 'SUBSTRATES'].index
					for i in idx:
						substrates = network.loc[i, 'SUBSTRATES'].split(',')

						# remove previous compartment
						for j, met in enumerate(substrates):
							if met.startswith('PER-') or met.startswith('EX-'):
								substrates[j] = '-'.join(met.split('-')[1:])

						if c1 != 'CYT':
							network.loc[i, 'SUBSTRATES'] = ','.join([ c1 + '-' + x for x in substrates ])
						else:
							network.loc[i, 'SUBSTRATES'] = ','.join(substrates)

		if len(lst) > 0 and len(toLst) > 0:
			for reaction, c2 in zip(lst, toLst):
				# check
				if c2 not in ['CYT', 'PER', 'EX']:
					break
				else:
					idx = network.loc[network[col].str.match(reaction), 'PRODUCTS'].index
					for i in idx:
						products = network.loc[i, 'PRODUCTS'].split(',')

						# remove previous compartment
						for j, met in enumerate(products):
							if met.startswith('PER-') or met.startswith('EX-'):
								products[j] = '-'.join(met.split('-')[1:])

						if c2 != 'CYT':
							network.loc[i, 'PRODUCTS'] = ','.join([ c2 + '-' + x for x in products ])
						else:
							network.loc[i, 'PRODUCTS'] = ','.join(products)

		return network

	def setEnzymeLocation(network, geneLst, compartmentLst):
		if isinstance(geneLst, list):
			pass
		else:
			geneLst = [geneLst]

		if isinstance(compartmentLst, list):
			pass
		else:
			compartmentLst = [compartmentLst]

		if not len(geneLst) == len(compartmentLst):
			raise Exception('The genes list and the compartments list do not have the same length.')

		warning = False
		for gene, compartment in zip(geneLst, compartmentLst):
			if compartment not in list(set(location_keys().keys())):
				warning = True
			else:
				network.loc[network['GENE OR COMPLEX'].str.match(gene), 'ENZYME LOCATION'] = location_keys()[compartment]

		if warning:
			print('At least one location could not be set. See utils.location_keys().keys() for valid identifiers of location.')

		return network

	def expand_network(infile_path, path = 'expanded.txt'):
		if isinstance(infile_path, str):
			with open(infile_path, 'r') as infile:
				data = pandas.read_csv(infile, delimiter = '\t', header = 0, comment = '#')
		elif isinstance(infile_path, pandas.DataFrame):
			data = infile_path
		else:
			raise Exception('Type of data not yet supported')

		with open(path, 'w+') as outfile:
			outfile.write('SOURCE\tTARGET\tEDGE_ATTRIBUTE\tSOURCE_NODE_ATTRIBUTE\tTARGET_NODE_ATTRIBUTE\n')

		with open(path, 'a') as outfile:
			for enzyme, reaction in zip(data['GENE OR COMPLEX'], data['REACTION']):
				outfile.write('{:s}\t{:s}\tNO_ARROW\tGENE_PROD\tRXN\n'.format(enzyme, reaction))

		with open(path, 'a') as outfile:
			for reaction, substrates, fwd, rvs in zip(data['REACTION'], data['SUBSTRATES'], data['FWD_RATE'], data['RVS_RATE']):
				reversibility = 'NO_REVERSIBLE'
				if fwd != 0 and rvs != 0:
					reversibility = 'REVERSIBLE'
				for substrate in substrates.split(','):
					outfile.write('{:s}\t{:s}\t{:s}\tMET\tRXN\n'.format(substrate, reaction, reversibility))

		with open(path, 'a') as outfile:
			for reaction, products, fwd, rvs in zip(data['REACTION'], data['PRODUCTS'], data['FWD_RATE'], data['RVS_RATE']):
				reversibility = 'NO_REVERSIBLE'
				if fwd != 0 and rvs != 0:
					reversibility = 'REVERSIBLE'
				for product in products.split(','):
					outfile.write('{:s}\t{:s}\t{:s}\tRXN\tMET\n'.format(reaction, product, reversibility))

		return None

class interactionNetwork:
	def FromGeneList(code, genes, fmt = 'genes', precalculated = None):
		if fmt not in ['genes']:
			raise Exception('Valid format is: \'genes\'')

		if isinstance(genes, str):
			genes = [genes]
		elif isinstance(genes, list):
			genes = genes
		else:
			raise Exception('Not supported data type yet.')

		# remove duplicated queries
		genes = sorted(set(genes))

		if precalculated is None:
			df_genes = returnCommonNames(code)
		else:
			df_genes = precalculated

		Network = ''
		organism = selectOrganism(code)
		for gene in genes:
			prod = organism.all_products_of_gene(df_genes.loc[gene, 'gene name'])
			products = [ x.replace('|', '') for x in prod ]

			for product in products:
				monomers, stoichiometry = organism.monomers_of_protein(product)

				if len(stoichiometry) == 1 and stoichiometry[0] > 1: # homomers, e.g. lacZ tetramer
					loc = []
					for monomer in monomers:
						locations = getData(code, monomer)['locations']
						for location in locations:
							loc.append(getData(code, location)['common_name'])

					Network += '{:s}\t{:s}\t[{:s}]\t1.0\t1.0\n'.format(gene, gene, ','.join(loc * 2))
					for idx in range(3, stoichiometry[0]+1):
						Network += '{:s}\t[{:s}]\t[{:s}]\t1.0\t1.0\n'.format(
							gene, ','.join([gene for x in range(idx-1)]), ','.join(loc * idx))

				elif len(stoichiometry) > 1: # heteromers, each index is the stoichiometry of a component
					genes = []
					for monomer, coefficient in zip(monomers, stoichiometry):
						tmp = organism.genes_of_protein(monomer)
						gene = getData(code, tmp[0])['common_name']
						genes.append(gene)

						if coefficient > 1: # assembly of homomers from the heteromer, e.g. A+A, B+B
							locations = getData(code, monomer)['locations']
							for location in locations:
								loc = [getData(code, location)['common_name']]
								Network += '{:s}\t{:s}\t[{:s}]\t1.0\t1.0\n'.format(gene, gene, ','.join(loc * 2))
								for idx in range(3, coefficient+1):
									Network += '{:s}\t[{:s}]\t[{:s}]\t1.0\t1.0\n'.format(
										gene, ','.join([gene for x in range(idx-1)]), ','.join(loc * idx))

					for a,b in itertools.combinations(range(len(stoichiometry)), 2): # assembly of homomers, e.g AA + BB
						tmp = [getData(code, x)['locations'] for x in monomers]
						tmp = list(itertools.product(*tmp))

						for loc in tmp:
							names = []
							for location in loc:
								names.append(getData(code, location)['common_name'])

							loc = ','.join([names[a] for x in range(stoichiometry[a])] + [names[b] for x in range(stoichiometry[b])])
							if stoichiometry[a] == 1 and stoichiometry[b] == 1:
								Network += '{:s}\t{:s}\t[{:s}]\t1.0\t1.0\n'.format(
									','.join([genes[a] for x in range(stoichiometry[a])]),
									','.join([genes[b] for x in range(stoichiometry[b])]), loc)

							elif stoichiometry[a] == 1 and stoichiometry[b] > 1:
								Network += '{:s}\t[{:s}]\t[{:s}]\t1.0\t1.0\n'.format(
									','.join([genes[a] for x in range(stoichiometry[a])]),
									','.join([genes[b] for x in range(stoichiometry[b])]), loc)

							elif stoichiometry[a] > 1 and stoichiometry[b] == 1:
								Network += '[{:s}]\t{:s}\t[{:s}]\t1.0\t1.0\n'.format(
									','.join([genes[a] for x in range(stoichiometry[a])]),
									','.join([genes[b] for x in range(stoichiometry[b])]), loc)

							elif stoichiometry[a] > 1 and stoichiometry[b] > 1:
								Network += '[{:s}]\t[{:s}]\t[{:s}]\t1.0\t1.0\n'.format(
									','.join([genes[a] for x in range(stoichiometry[a])]),
									','.join([genes[b] for x in range(stoichiometry[b])]), loc)

					# enumeration of all ordered mechanisms of assembly: e.g. ABC -> A+B+C, A+C+B, B+A+C, B+C+A, C+A+B, C+B+A
					new = [[x] * y for x,y in zip(genes, stoichiometry)]
					new = [x for y in new for x in y]

					tmp = [[x] * y for x,y in zip(monomers, stoichiometry)]
					tmp = [x for y in tmp for x in y]
					tmp = [getData(code, x)['locations'] for x in tmp]
					tmp = list(itertools.product(*tmp))

					for locs in tmp:
						for new2, loc2 in zip(itertools.permutations(new), itertools.permutations(locs)):
							names = []
							for loc in loc2:
								names.append(getData(code, loc)['common_name'])

							for idx in range(1,len(new2)-1):
								Network += '{:s}\t[{:s}]\t[{:s}]\t1.0\t1.0\n'.format(
									new2[idx+1], ','.join([x for x in new2[0:idx+1]]), ','.join(names[0:idx+2]))

		infile = io.StringIO(Network.replace('|',''))
		header = ['SOURCE', 'TARGET', 'LOCATION', 'FWD_RATE', 'RVS_RATE']
		df = pandas.read_csv(infile, delimiter = '\t', names = header)
		return df[~df.duplicated(['SOURCE', 'TARGET', 'LOCATION'], keep = 'first')].reset_index(drop = True)

	def addInteraction(network, source = ['A'], target = ['B'], fwd_rate = 1.0, rvs_rate = 1.0, location = 'CYT'):
		if location not in location_keys().keys():
			print('Valid location acronyms are: {:s}'.format(','.join(location_keys().keys())))

		if isinstance(source, list):
			source = '[' + ','.join(source) + ']'

		if isinstance(target, list):
			target = '[' + ','.join(target) + ']'

		if isinstance(location, list):
			location = '[' + ','.join([location_keys()[x] for x in location]) + ']'
		elif isinstance(location, str):
			location = location_keys()[location]

		network = network.append({
			'SOURCE' : source,
			'TARGET' : target,
			'FWD_RATE' : fwd_rate,
			'RVS_RATE' : rvs_rate,
			'LOCATION' : location
			}, ignore_index = True)

		return network

	def removeInteraction(network, index = []):
		return network.drop(labels = index, axis = 0)
