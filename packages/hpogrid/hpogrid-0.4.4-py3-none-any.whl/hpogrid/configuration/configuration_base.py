import sys, os
import argparse
import json
import fnmatch

from hpogrid.utils import stylus
from hpogrid.components.defaults import *

kActionList = ['create', 'recreate', 'update', 'list', 'show', 'remove']  
kConfigAction = ['create', 'recreate', 'update']

class ConfigurationBase():

    def __init__(self):
        self.initialize()
        parser = self.get_parser() 
        args = parser.parse_args(sys.argv[2:3])
        action = args.action
        parser = self.get_parser(action)
        args = parser.parse_args(sys.argv[3:])

        if action in kConfigAction:
            self.configure(args, action)
        elif hasattr(self, action):
            getattr(self, action)(**vars(args))
        else:
            print('Unrecognized action: {}'.format(action))
            parser.print_help()
            exit(1)            

    def initialize(self):
        self.description = 'Manage configuration'
        self.usage = 'hpogrid <config_type> <action> <config_name> [<options>]'
        self.config_type = 'SUPPRESS'
        self.list_columns = []
        self.show_columns = []

    def get_base_parser(self):
        parser = argparse.ArgumentParser(
            description=self.description,
            usage=self.usage) 
        return parser

    def get_parser(self, action=None):
        parser = self.get_base_parser()           
        if not action:
            parser.add_argument('action', help='Action to be performed', choices=kActionList)    
        elif action == 'list':
            parser.add_argument('--expr', metavar='',
                help='Filter out config files that matches the expression')
        elif action == 'show':
            parser.add_argument('name', help='Name of config file to show')
        elif action == 'remove':
            parser.add_argument('name', help='Name of config file to remove')
        else:
            raise ValueError('Unknown method: {}'.format(action))
        return parser

    def get_base_dir(self, config_type=None, force_create=True):

        if config_type is None:
            config_type = self.config_type
            
        if config_type == 'project':
            base_dir = os.path.join(os.environ[kHPOGridEnvPath], 'project')
        else:
            base_dir = os.path.join(os.environ[kHPOGridEnvPath], 'config', config_type)

        if (not os.path.exists(base_dir)) and force_create:
            os.makedirs(base_dir, exist_ok=True)
        return base_dir

    def get_config_path(self, config_name=None, config_type=None, extension='.json'):
        if config_name is None:
            config_name = self.config_name
        if config_type is None:
            config_type = self.config_type
        base_dir = self.get_base_dir(config_type)
        config_base_name = '{}{}'.format(config_name, extension)
        config_path = os.path.join(base_dir, config_base_name)
        return config_path

    def remove(self, name):
        config_path = self.get_config_path(name)
        if os.path.exists(config_path):
            os.remove(config_path)
            print('INFO: Removed file {}'.format(config_path))
        else:
            print('ERROR: Cannot remove file {}. File does not exist.'.format(config_path))

    def get_updated_config(self, config):
        non_updated_keys = []
        for key in config:
            if config[key] is None:
                non_updated_keys.append(key)
        for key in non_updated_keys:
            config.pop(key, None)
        config_path = self.get_config_path(config['name'])
        if not os.path.exists(config_path):
            raise FileNotFoundError('Configuration file {} not found. Update aborted.'.format(config_path))
        old_config = json.load(open(config_path))
        config = {**old_config, **config}
        return config

    def _retain_only_updated_options(self):
        parser = self.get_parser('update')
        for action in parser._actions:
            if (len(action.option_strings) > 0) and (action.default != '==SUPPRESS=='):
                action.default=None
        args = parser.parse_args(sys.argv[3:])
        return args

    def configure(self, args, action='create'):
        if action == 'update':
            args = self._retain_only_updated_options()

        config = vars(args)
        
        if action == 'update':
            config = self.get_updated_config(config)

        self.process_config(config)
        config_name = config.pop('name', None)
        if config is not None:
            self.save(config, config_name, action)
        return config

    def process_config(self, config):
        for key in config:
            if isinstance(config[key], bool):
                config[key] = int(config[key])
        return config

    def save(self, config, name, action='create'):

        config_path = self.get_config_path(name)
        if (os.path.exists(config_path)) and (action=='create'):
            print('ERROR: {} configuration with name {} already exists.'
                'If you want to overwrite, use "recreate" or "update" action instead of "create".'.format(
                self.config_type, name))
        else:
            with open(config_path, 'w') as config_file:
                json.dump(config, config_file, indent=2)
            action_map = { 'create': 'Created', 'recreate': 'Recreated', 'update': 'Updated'}
            print('INFO: {} {} configuration {}'.format(action_map[action], self.config_type, config_path))
            self.show(name)

    def get_config_list(self, expr=None):
        if not expr:
            expr = '*'
        base_dir = self.get_base_dir()
        config_list = [os.path.splitext(d)[0] for d in os.listdir(base_dir) if not d.startswith('.')]
        if expr is not None:
            config_list = fnmatch.filter(config_list, expr)
        return config_list

    def load_config(self, config_name):
        config_path = self.get_config_path(config_name)
        if not (os.path.exists(config_path)):
            raise FileNotFoundError("The configuration file {} does not exist.".format(config_path))
        config = json.load(open(config_path))
        return config

    def list(self, expr=None):
        config_list = self.get_config_list(expr)
        table = stylus.create_table(config_list, self.list_columns)
        print(table)

    def show(self, name):
        config = self.load_config(name)
        table = stylus.create_table(config.items(), self.show_columns, indexed=False)
        print(table)
