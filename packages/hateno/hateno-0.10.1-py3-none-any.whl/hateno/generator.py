#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import stat
import re
import functools
import copy
from math import ceil
from string import Template

from .errors import *
from .fcollection import FCollection
from .folder import Folder
from .simulation import Simulation
from . import generators as default_generators

class Generator():
	'''
	Generate some scripts to create a set of simulations.
	Initialize the list of simulations to generate.

	Parameters
	----------
	folder : Folder|string
		The folder to manage. Either a `Folder` instance or the path to the folder (used to create a `Folder` instance).
	'''

	def __init__(self, folder):
		self._folder = folder if type(folder) is Folder else Folder(folder)

		self._simulations_to_generate = []

		self._lists_regex_compiled = None
		self._lists_items_regex_compiled = None

		self._variables_generators = None

	@property
	def folder(self):
		'''
		Return the `Folder` instance.

		Returns
		-------
		folder : Folder
			The instance used by the generator.
		'''

		return self._folder

	@property
	def _lists_regex(self):
		'''
		Regex to detect the presence of lists blocks in a skeleton.

		Returns
		-------
		regex : re.Pattern
			The lists regex.
		'''

		if self._lists_regex_compiled is None:
			self._lists_regex_compiled = re.compile(r'^[ \t]*#{3} BEGIN_(?P<tag>[A-Z_]+) #{3}$.+?^(?P<content>.+?)^[ \t]*#{3} END_\1 #{3}$.+?^', flags = re.MULTILINE | re.DOTALL)

		return self._lists_regex_compiled

	@property
	def _lists_items_regex(self):
		'''
		Regex to detect the presence of lists items as variables names.

		Returns
		-------
		regex : re.Pattern
			The lists items regex.
		'''

		if self._lists_items_regex_compiled is None:
			self._lists_items_regex_compiled = re.compile(r'^(?P<list>[A-Z_]+)__(?P<index>[0-9]+)$')

		return self._lists_items_regex_compiled

	@property
	def variables_generators(self):
		'''
		Get the list of available variables generators.

		Returns
		-------
		generators : FCollection
			The collection of generators.
		'''

		if self._variables_generators is None:
			self._variables_generators = FCollection(filter_regex = r'^generator_(?P<name>[A-Za-z0-9_]+)$')
			self._variables_generators.loadFromModule(default_generators)

		return self._variables_generators

	def add(self, simulations):
		'''
		Add simulations to generate.

		Parameters
		----------
		simulations : list|dict|Simulation
			List of simulations to add.
		'''

		if type(simulations) is list:
			for simulation in simulations:
				self._simulations_to_generate.append(Simulation.ensureType(simulation, self._folder))

		else:
			self.add([simulations])

	def clear(self):
		'''
		Clear the list of simulations to generate.
		'''

		self._simulations_to_generate.clear()

	def parse(self, simulations_set = None):
		'''
		Parse a set of simulations to generate the corresponding command lines and other variables.

		Parameters
		----------
		simulations_set : list
			The set of simulations to parse. If `None`, default to the whole list.

		Returns
		-------
		variables : dict
			The list of command lines, and variables corresponding to the simulations' global settings.
		'''

		if simulations_set is None:
			simulations_set = self._simulations_to_generate

		globalsettings = self._folder.settings['globalsettings']

		variables = {
			'data_lists': {'COMMAND_LINES': [simulation.command_line for simulation in simulations_set]},
			'data_variables': {}
		}

		for globalsetting in self._folder.settings['globalsettings']:
			name_upper = 'GLOBALSETTING_'+globalsetting['name'].upper()
			variables['data_lists'][name_upper] = [simulation[globalsetting['name']] for simulation in simulations_set]

			if 'generators' in globalsetting:
				for generator_name in globalsetting['generators']:
					try:
						generator = self.variables_generators.get(generator_name)

					except FCollectionFunctionNotFoundError:
						raise VariableGeneratorNotFoundError(generator_name)

					else:
						variables['data_variables'][generator_name.upper()+'_'+name_upper] = functools.reduce(generator, variables['data_lists'][name_upper])

		return variables

	def generateScriptFromSkeleton(self, skeleton_name, output_name, lists, variables, *, make_executable = False):
		'''
		Generate a script from a skeleton, using a given set of command lines.

		Parameters
		----------
		skeleton_name : str
			Name of the skeleton file.

		output_name : str
			Name of the script to write.

		lists : dict
			Lists we can use to loop through.

		variables : dict
			Variables we can use in the whole script template.

		make_executable : boolean
			`True` to add the 'exec' permission to the script.
		'''

		with open(skeleton_name, 'r') as f:
			skeleton = f.read()

		def replaceListBlock(match):
			'''
			Replace a list block by the content of the right list.
			To be called by `re.sub()`.

			Parameters
			----------
			match : re.Match
				Match object corresponding to a list block.

			Returns
			-------
			list_content : str
				The content of the list, formatted as asked.
			'''

			try:
				list_content = ''
				loop_content_template = Template(match.group('content'))

				for index, value in enumerate(lists[match.group('tag')]):
					list_content += loop_content_template.safe_substitute(ITEM_INDEX = index, ITEM_VALUE = value)

				return list_content

			except KeyError:
				return match.group(0)

		script_content = self._lists_regex.sub(replaceListBlock, skeleton)

		variables = copy.deepcopy(variables)
		script_content_template = Template(script_content)

		for match in script_content_template.pattern.finditer(script_content_template.template):
			if match.group('braced'):
				submatch = self._lists_items_regex.match(match.group('braced'))

				if submatch:
					variables[submatch.group(0)] = lists[submatch.group('list')][int(submatch.group('index'))]

		script_content = script_content_template.safe_substitute(**variables)

		with open(output_name, 'w') as f:
			f.write(script_content)

		if make_executable:
			os.chmod(output_name, os.stat(output_name).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

	def generate(self, dest_folder, recipe, *, empty_dest = False):
		'''
		Generate the scripts to launch the simulations by subgroups.

		Parameters
		----------
		dest_folder : str
			Destination folder where scripts should be stored.

		recipe : dict
			Parameters to generate the scripts.

		empty_dest : boolean
			If `True` and if the destination folder already exists, empty it before generating the scripts. If `False` the existence of the folder raises an error.

		Raises
		------
		EmptyListError
			The list of simulations to generate is empty.

		DestinationFolderExistsError
			The destination folder already exists.

		Returns
		-------
		generated_scripts : list
			List of generated scripts, separated: one list per skeleton, in the order they are called.
		'''

		if not(self._simulations_to_generate):
			raise EmptyListError()

		if os.path.isdir(dest_folder):
			if empty_dest:
				for entry in [os.path.join(dest_folder, e) for e in os.listdir(dest_folder)]:
					(shutil.rmtree if os.path.isdir(entry) else os.unlink)(entry)

			else:
				raise DestinationFolderExistsError()

		else:
			os.makedirs(dest_folder)

		if not('max_simulations' in recipe):
			if 'max_subgroups' in recipe:
				recipe['max_simulations'] = ceil(len(self._simulations_to_generate) / recipe['max_subgroups'])

			else:
				recipe['max_simulations'] = len(self._simulations_to_generate)

		else:
			if recipe['max_simulations'] <= 0:
				recipe['max_simulations'] = len(self._simulations_to_generate)

			if 'max_subgroups' in recipe and len(self._simulations_to_generate) / recipe['max_simulations'] > recipe['max_subgroups']:
				recipe['max_simulations'] = ceil(len(self._simulations_to_generate) / recipe['max_subgroups'])

		simulations_sets = [self._simulations_to_generate[k:k+recipe['max_simulations']] for k in range(0, len(self._simulations_to_generate), recipe['max_simulations'])]

		data_lists = {}
		data_variables = {
			'JOBS_OUTPUT_FILENAME': recipe['jobs_output_filename']
		}

		if 'jobs_states_filename' in recipe:
			data_variables['JOBS_STATES_FILENAME'] = recipe['jobs_states_filename']

		if 'data_lists' in recipe:
			data_lists.update(recipe['data_lists'])

		if 'data_variables' in recipe:
			data_variables.update(recipe['data_variables'])

		n_subgroups_skeletons = len(recipe['subgroups_skeletons'])
		n_skeletons = n_subgroups_skeletons + len(recipe['wholegroup_skeletons'])

		skeletons_calls = []
		generated_scripts = [[]] * n_skeletons

		jobs_ids = [f'job-{k}' for k in range(0, len(simulations_sets))]

		if 'subgroups_skeletons' in recipe:
			skeletons_calls += [
				{
					'skeleton_name_joiner': f'-{k}.',
					'skeletons': enumerate(recipe['subgroups_skeletons']),
					'job_id': jobs_ids[k],
					'jobs_ids': jobs_ids,
					**self.parse(simulations_set)
				}
				for k, simulations_set in enumerate(simulations_sets)
			]

		if 'wholegroup_skeletons' in recipe:
			skeletons_calls.append({
				'skeleton_name_joiner': '.',
				'skeletons': [(n_subgroups_skeletons + j, s) for j, s in enumerate(recipe['wholegroup_skeletons'])],
				'job_id': '',
				'jobs_ids': jobs_ids,
				**self.parse()
			})

		if not('make_executable' in recipe):
			recipe['make_executable'] = False

		scripts_basedir = dest_folder if not('basedir' in recipe) else recipe['basedir']

		for skeletons_call in skeletons_calls:
			data_lists.update(skeletons_call['data_lists'])
			data_variables.update(skeletons_call['data_variables'])

			data_variables['JOB_ID'] = skeletons_call['job_id']
			data_lists['JOBS_IDS'] = skeletons_call['jobs_ids']

			if 'data_variables_cases' in recipe:
				for varname, varparams in recipe['data_variables_cases'].items():
					vartest = data_variables[varparams['variable']]
					data_variables[varname] = [value for bound, value in zip(varparams['bounds'], varparams['values']) if bound <= vartest][-1]

			for j, skeleton_name in skeletons_call['skeletons']:
				skeleton_basename_parts = os.path.basename(skeleton_name).rsplit('.skeleton.', maxsplit = 1)
				skeleton_tag = re.sub('[^A-Z_]+', '_', skeleton_basename_parts[0].upper())
				script_name = skeletons_call['skeleton_name_joiner'].join(skeleton_basename_parts)
				script_localpath = os.path.join(dest_folder, script_name)
				script_finalpath = os.path.join(scripts_basedir, script_name)

				self.generateScriptFromSkeleton(skeleton_name, script_localpath, data_lists, data_variables, make_executable = recipe['make_executable'])
				data_variables[skeleton_tag] = script_finalpath

				try:
					data_lists[skeleton_tag].append(script_finalpath)

				except KeyError:
					data_lists[skeleton_tag] = [script_finalpath]

				generated_scripts[j].append({'name': script_name, 'localpath': script_localpath, 'finalpath': script_finalpath})

		return generated_scripts
