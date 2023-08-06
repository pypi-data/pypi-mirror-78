import sys, os
import argparse
import json
from json import JSONDecodeError

from hpogrid.components.defaults import *
from hpogrid.configuration.configuration_base import ConfigurationBase, kConfigAction

class HPOConfiguration(ConfigurationBase):

    def initialize(self):
        self.description = 'Manage configuration for hyperparameter optimization'
        self.usage = 'hpogrid hpo_config <action> <config_name> [<options>]'
        self.config_type = 'hpo'
        self.list_columns = ['HPO Configuration']
        self.show_columns = ['Attribute', 'Value']    

    def get_parser(self, action=None):
        parser = self.get_base_parser()        
        if action in kConfigAction:
            parser.add_argument('name', help= "Name given to the configuration file")
            parser.add_argument('-a','--algorithm', 
                                help='Algorithm for hyperparameter optimization', 
                                default=kDefaultSearchAlgorithm, choices=kSearchAlgorithms)
            parser.add_argument('-m', '--metric', metavar='',
                                help='Evaluation metric to be optimized', 
                                default=kDefaultMetric)
            parser.add_argument('-o', '--mode', 
                                help='Mode of optimization (either "min" or "max")', 
                                default=kDefaultMode, choices=kMetricMode)
            parser.add_argument('-s','--scheduler', 
                                help='Trial scheduling method for hyperparameter optimization',
                                default=kDefaultScheduler, choices=kSchedulers)
            parser.add_argument('-n','--num_trials', metavar='',
                                help='Number of trials (search points)', 
                                type=int, default=kDefaultTrials)
            parser.add_argument('-c','--max_concurrent', metavar='',
                                help='Maximum number of trials to be run concurrently', 
                                type=int, default=kDefaultMaxConcurrent)            
            parser.add_argument('-l', '--log_dir', metavar='',
                                help='Logging directory',
                                default=kDefaultLogDir)
            parser.add_argument('-v','--verbose', action='store_true', 
                                help='Check to enable verbosity')
            parser.add_argument('--stop', metavar='',
                                help='Stopping criteria for the training',
                                default=kDefaultStopping)
            parser.add_argument('-r','--resource', metavar='',
                                help='Resource allocated to each trial')            
            parser.add_argument('--scheduler_param', metavar='',
                                help='Extra parameters given to the trial scheduler', 
                                default=kDefaultSchedulerParam)
            parser.add_argument('--algorithm_param', metavar='',
                                help='Extra parameters given to the hyperparameter optimization algorithm',
                                default=kDefaultAlgorithmParam)
        else:
            parser = super().get_parser(action)
        return parser

    def process_config(self, config):
        super().process_config(config)

        json_interp = ['stop', 'scheduler_param', 'algorithm_param', 'resource']
        for key in json_interp:
            if (key in config) and isinstance(config[key],str):
                try:
                    config[key] = json.loads(config[key])
                except JSONDecodeError:
                    print('ERROR: Cannot decode the value of {} into json format.'
                        'Please check your input.'.format(key))
                    return None                

        return config