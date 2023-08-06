import sys, os
import argparse
import json

from hpogrid.components.defaults import *
from hpogrid.configuration.configuration_base import ConfigurationBase, kConfigAction
from hpogrid.utils import stylus

class ModelConfiguration(ConfigurationBase):

    def initialize(self):
        self.description = 'Manage configuration for machine learning model'
        self.usage = 'hpogrid model_config <action> <config_name> [<options>]'
        self.config_type = 'model'
        self.list_columns = ['Model Configuration']
        self.show_columns = ['Attribute', 'Value']  

    def get_parser(self, action=None):
        parser = self.get_base_parser()              
        if action in kConfigAction:  
            parser.add_argument('name', help= "Name given to the configuration file")            
            parser.add_argument('-s','--script', metavar='',
                help='Name of the training script where the function or class that defines'
                     ' the training model will be called to perform the training')
            parser.add_argument('-m','--model', metavar='',
                help='Name of the function or class that defines the training model')        
            parser.add_argument('-p','--param', metavar='',
                help='Extra parameters to be passed to the training model',
                default=kDefaultModelParam)
        else:
            parser = super().get_parser(action)
        return parser

    def process_config(self, config):
        super().process_config(config)

        if ('param' in config) and isinstance(config['param'],str):
            try:
                config['param'] = json.loads(config['param'])
            except JSONDecodeError:
                print('ERROR: Cannot decode input param into json format. Please check your input.')
                return None

        return config
    
    def show(self, name):
        config = self.load_config(name)
        table = stylus.create_formated_dict(config, self.show_columns, indexed=False)
        print(table)       
