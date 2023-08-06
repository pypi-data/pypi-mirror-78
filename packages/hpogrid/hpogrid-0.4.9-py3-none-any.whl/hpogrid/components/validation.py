import json
import os

try:
    from hpogrid.components.defaults import *
except:
    raise ImportError('ERROR: Cannot import hpogrid module. Try source setupenv first.')



kHPSamplingFormat = {
	'categorical': {
		'categories' : { 'type': list, 'required': True},
		'grid_search' : { 'type': int, 'required': False, 'default': 0}
	},
	'uniform': {
		'low': { 'type': (float, int), 'required': True},
		'high': { 'type': (float, int), 'required': True}
	},
	'uniformint': {
		'low': { 'type': int, 'required': True},
		'high': { 'type': int, 'required': True}
	},
	'quniform': {
		'low': { 'type': (float, int), 'required': True},
		'high': { 'type': (float, int), 'required': True},
		'q': { 'type': (float, int), 'required': True}
	},
	'loguniform': {
		'low': { 'type': (float, int), 'required': True},
		'high': { 'type': (float, int), 'required': True},
		'base': { 'type': (float, int), 'required': False}
	},
	'qloguniform': {
		'low': { 'type': (float, int), 'required': True},
		'high': { 'type': (float, int), 'required': True},
		'q': { 'type': (float, int), 'required': True},
		'base': { 'type': (float, int), 'required': False}
	},
	'normal': {
		'mu': { 'type': (float, int), 'required': True},
		'sigma': { 'type': (float, int), 'required': True}
	},
	'qnormal': {
		'mu': { 'type': (float, int), 'required': True},
		'sigma': { 'type': (float, int), 'required': True},
		'q': { 'type': (float, int), 'required': True}
	},
	'lognormal': {
		'mu': { 'type': (float, int), 'required': True},
		'sigma': { 'type': (float, int), 'required': True},
		'base': { 'type': (float, int), 'required': False}
	},
	'qlognormal': {
		'mu': { 'type': (float, int), 'required': True},
		'sigma': { 'type': (float, int), 'required': True},
		'base': { 'type': (float, int), 'required': False},
		'q': { 'type': (float, int), 'required': True}
	},
	'fixed': {
		'value': { 'type': None, 'required': True}
	}
}

kGridConfigFormat = {
	'site': {
		'required': True,
		'type': str,
		'choice': kGPUGridSiteList,
		'default': kDefaultGridSite
	},
	'container': {
		'required': True,
		'type': str,
		'default': kDefaultContainer
	},
	'retry': {
		'required': False,
		'type': int,
		'default': 0
	},
	'inDS': {
		'required': True,
		'type': str
	},
	'outDS': {
		'required': True,
		'type': str,
		'default': kDefaultOutDS
	}

}

kHPOConfigFormat = {
	'algorithm': {
		'required': True,
		'type': str,
		'choice': kSearchAlgorithms
	},
	'metric' : {
		'required': True,
		'type': str,
	},
	'mode' : {
		'required': True,
		'type': str,
		'choice': kMetricMode,
	},
	'scheduler': {
		'required': False,
		'type': str,
		'choice': kSchedulers,
		'default': kDefaultScheduler
	},
	'trials': {
		'required': False,
		'type': int,
		'default': 100
	},
	'log_dir': {
		'required': False,
		'type': str,
		'default': './log'
	},
	'verbose': {
		'required': False,
		'type': int,
		'default': 0
	}
}

def type2str(typevar):
	if isinstance(typevar, tuple):
		return ', '.join([t.__name__ for t in typevar])
	else:
		return typevar.__name__

def validate_project_env_path():
	if kProjectPath in os.environ:
		return True
	else:
		print('ERROR: Path variable {} not set.'
			'Maybe you need to source setupenv.sh first.'.format(kProjectPath))
		return False


def validate_hpogrid_env_path():
	if kHPOGridEnvPath in os.environ:
		return True
	else:
		print('ERROR: Path variable {} not set.'
			'Maybe you need to source setupenv.sh first.'.format(kHPOGridEnvPath))
		return False

def validate_hpo_config(config):
	print('Info: Validating HPO configuration...')
	config_format = kHPOConfigFormat
	for key in config_format:
		if key in config:
			# check if the value type of the config is correct
			value_type = config_format[key]['type']
			if not isinstance(config[key], value_type):
				print('ERROR: The value of {} must be of type {}'.format(key, type2str(value_type)))
				return False
			# check if the value of the config is supported
			if ('choice' in config_format[key]) and (config[key] not in config_format[key]['choice']):
				print('ERROR: The value of {} must be one of the followings')
				print(str(config_format[key]['choice']).strip('[]'))
				return False
		else:
			if config_format[key]['required']:
				print('ERROR: The required key {} is missing from the configuration'.format(key))
				return False
			# fill in default config if not specified
			if 'default' in config_format[key]:
				print('Info: Added the key {} with default value {} to the configuration '.format(
					key, str(config_format[key]['default'])))
				config[key] = config_format[key]['default']

	print('Info: Successfully validated HPO configuration')
	return True

def validate_search_space(search_space):
	print('Info: Validating search space configuration...')
	sampling_methods = kHPSamplingFormat.keys()
	kHPKeys = set(['method', 'dimension'])
	for hp in search_space:
		if (not isinstance(search_space[hp], dict)) or (set(search_space[hp].keys()) != kHPKeys):
			print('ERROR: Each hyperparameter must be defined by a dictionary containing the keys "method" and "dimension"')
			return False	
		if not isinstance(search_space[hp]['dimension'], dict):
			print('ERROR: Dimension of a hyperparameter must be a dictionary containing the parametrs of its sampling method')
			return False
		method = search_space[hp]['method']
		# check if hyperparameter sampling method is supported
		if method not in sampling_methods:
			print('ERROR: Sampling method {} is not supported'.format(method))
			return False
		for arg in kHPSamplingFormat[method]:
			if arg in search_space[hp]['dimension']:
				# check if the argument type of the sampling method is correct
				value_type = kHPSamplingFormat[method][arg]['type']
				if not isinstance(search_space[hp]['dimension'][arg], value_type):
					print('ERROR: The value of argument {} for the sampling method {} must be of type {}'.format(
						arg, method, type2str(value_type)))
					return False
			else:
				# check if a required argument for the sampling method is missing
				if (kHPSamplingFormat[method][arg]['required']):
					print('ERROR: Missing argument {} for the sampling method {}'.format(arg, method))
					return False
				# set the argument to its default value if not specified
				if ('default' in kHPSamplingFormat[method][arg]):
					print('Info: The argument {} for the sampling method {} will be set to its default value {}'.format(
						arg, method, kHPSamplingFormat[method][arg]['default']))
					search_space[hp]['dimension'][arg] = kHPSamplingFormat[method][arg]['default']
	print('Info: Successfully validated search space configuration')
	return True



def validate_grid_config(config):
	return True


def validate_job_metadata(data):
	if not isinstance(data, dict):
	    return False
	return all(key in kHPOGridMetadataFormat for key in data)