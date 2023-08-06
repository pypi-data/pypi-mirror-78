import sys, os
import argparse
import json

from hpogrid.components.defaults import *
from hpogrid.components import validation
from hpogrid.utils import stylus
from hpogrid.configuration.configuration_base import ConfigurationBase, kConfigAction

class SearchSpaceConfiguration(ConfigurationBase):

    def initialize(self):
        self.description = 'Manage configuration for hyperparameter search space'
        self.usage = 'hpogrid search_space <action> <config_name> <search_space_definition>'
        self.config_type = 'search_space'
        self.list_columns = ['Search Space Configuration']
        self.show_columns = ['Hyperparameters', 'Search Space']  


    def get_parser(self, action=None):
        parser = self.get_base_parser()               
        if action in kConfigAction:     
            parser.add_argument('name', 
                help='Name given to the configuration file')  
            parser.add_argument('search_space', 
                help='A json decodable string defining the search space')  
        else:
            parser = super().get_parser(action)
        return parser

    def configure(self, args, action='create'):

        config = vars(args)
        config_name = config.pop('name', None)
        search_space = config.pop('search_space', None)

        try:
            search_space = json.loads(search_space)
        except JSONDecodeError:
            print('ERROR: Cannot to decode input string into json format. Please check your input.')
            return None

        if action == 'update':
            config_path = self.get_config_path(config_name)
            if not os.path.exists(config_path):
                raise FileNotFoundError('Search space file {} not found. Update aborted.'.format(config_path))
            old_serach_space = json.load(open(config_path))
            search_space = {**old_serach_space, **search_space}
        
        if validation.validate_search_space(search_space):
            self.save(search_space, config_name, action)
        return search_space
    
    def show(self, name):
        config = self.load_config(name)
        table = stylus.create_formated_dict(config, self.show_columns, indexed=False)
        print(table)    