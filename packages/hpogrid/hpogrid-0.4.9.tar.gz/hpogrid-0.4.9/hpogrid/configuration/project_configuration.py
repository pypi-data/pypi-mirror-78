import sys, os
import argparse
import json
import yaml
import shutil

from distutils import dir_util
from datetime import datetime
from json import JSONDecodeError
from pdb import set_trace

from hpogrid.utils import stylus, helper
from hpogrid.components.defaults import *
from hpogrid.configuration.configuration_base import ConfigurationBase, kConfigAction

kConfigList = ['scripts_path', 'model_config', 'search_space', 'hpo_config', 'grid_config']

class ProjectConfiguration(ConfigurationBase):

    def initialize(self):
        self.description = 'Manage a project for hyperparamter optimization'
        self.usage = 'hpogrid project <action> <project_name> [<options>]'
        self.config_type = 'project'
        self.list_columns = ['Project Title']
        self.show_columns = ['Attribute', 'Value']  
        self.project_config = {}


    def get_parser(self, action=None):
        parser = self.get_base_parser()           
        if action in kConfigAction:          
            parser.add_argument('name', help= "Name given the project")
            parser.add_argument('-p','--scripts_path', metavar='',
                help='Path to where the training scripts'
                ' (or the directory containing the training scripts) are located')
            parser.add_argument('-o','--hpo_config', metavar='',
                help='Name of the hpo configuration to use')
            parser.add_argument('-g','--grid_config', metavar='',
                help='Name of the grid configuration to use')
            parser.add_argument('-m','--model_config', metavar='',
                help='Name of the model configuration to use')
            parser.add_argument('-s','--search_space', metavar='',
                help='Name of the search space configuration to use')
        else:
            parser = super().get_parser(action)
        return parser

    def get_updated_config(self, config):
        return config

    def process_config(self, config):
        self.project_config = config

        print('INFO: Loading configurations...')
        # check if path to training scripts exists
        if (config['scripts_path'] is not None):
            scripts_path = config['scripts_path']
            if not os.path.exists(scripts_path):
                print('ERROR: Path to training scripts {} does not exist.'
                       'Copy to project will be skipped.'.format(scripts_path))
                config['scripts_path'] = None
        else:
            print('INFO: Path to training scripts is not specified. Skipping...')

        config_type_map = {
            'hpo_config': 'hpo',
            'grid_config': 'grid',
            'model_config': 'model',
            'search_space': 'search space'
        }

        # check if input configuration files exist
        for key in config_type_map:
            if (key in config) and (config[key] is not None):
                config_type = config_type_map[key].replace(' ','_')
                config_path = self.get_config_path(config[key], config_type)
                if not os.path.exists(config_path):
                    raise FileNotFoundError('ERROR: Path to {} configuration {} does not exist.'.format(config_type, config_path))
                with open(config_path,'r') as config_file:
                    config[key] = json.load(config_file)
                print('INFO: Loaded {} configuration from {} '.format(config_type_map[key], config_path))
            else:
                print('INFO: Path to {} configuration is not specified. Skipping...'.format(config_type_map[key]))

        return config

    def get_project_path(self, proj_name):
        return self.get_config_path(proj_name, self.config_type, extension='')

    def save(self, config, name, action='create'):
        proj_name = name
        proj_path = self.get_project_path(proj_name)
        if (os.path.exists(proj_path)):
            if  action == 'create':
                print('ERROR: Project titled {} already exists. If you want to overwrite,'
                    ' use "recreate" or "update" action instead of "create".'.format(proj_name))
                return None
            elif action == 'recreate':
                backup_dir = self.get_config_path('backup', self.config_type, extension='')
                os.makedirs(backup_dir, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                backup_proj_name = os.path.join(backup_dir, '{}_{}'.format(proj_name, timestamp))
                shutil.move(proj_path, backup_proj_name)
                print('INFO: Recreating project. Original project moved to backup directory {}.'.format(
                    backup_proj_name))
        # create project directories
        scripts_dir = os.path.join(proj_path, 'scripts')
        config_dir = os.path.join(proj_path, 'config')
        os.makedirs(proj_path, exist_ok=True)        
        os.makedirs(scripts_dir, exist_ok=True)
        os.makedirs(config_dir, exist_ok=True)

        # copy training scripts to the project directory
        if ('scripts_path' in config) and (config['scripts_path'] is not None):
            # copy contents of directory to project/scrsipts/
            if os.path.isdir(config['scripts_path']):
                dir_util.copy_tree(config['scripts_path'], scripts_dir)
            else:
                shutil.copy2(config['scripts_path'], scripts_dir)
            print('INFO: From {} copied training scripts to {}'.format(config['scripts_path'], scripts_dir))

        
        project_config = {}
        project_config['project_name'] = proj_name
        
        if action == 'update':
            project_config.update(helper.get_project_config(proj_name))
            
        for key in kConfigList:
            if (key in config) and (config[key] is not None):
                project_config[key] = config[key]
    
        project_config_path_json = os.path.join(config_dir, kProjectConfigNameJson)
        project_config_path_yaml = os.path.join(config_dir, kProjectConfigNameYaml)
        
        with open(project_config_path_json,'w') as proj_config_file:
            json.dump(project_config, proj_config_file, indent=2)
            print('INFO: Created project configuration: {}'.format(project_config_path_json))
        with open(project_config_path_yaml,'w') as proj_config_file:
            yaml.dump(project_config, proj_config_file, default_flow_style=False, sort_keys=False)
            print('INFO: Created project configuration: {}'.format(project_config_path_yaml))
            
        search_space = project_config['search_space']    
        idds_search_space_path = os.path.join(config_dir, kiDDSSearchSpaceName)
        with open(idds_search_space_path, 'w') as idds_search_space_file:
            json.dump(search_space, idds_search_space_file)
            print('INFO: Created iDDS search space file: {}'.format(idds_search_space_path))
            
    def get_config_list(self, expr=None):
        project_list = [ s for s in super().get_config_list() if s is not 'backup']
        return project_list

    def remove(self, name):
        proj_path = self.get_project_path(name)
        if os.path.exists(proj_path):
            print('WARNING: To avoid accidental deletion of important files. '
                'Please delete your project manually at:\n{}'.format(proj_path))
        else:
            print('ERROR: Cannot remove project in {}. Path does not exist.'.format(proj_path))

    def show(self, name):
        proj_path = self.get_project_path(name)
        if os.path.exists(proj_path):
            config = helper.get_project_config(name)
            print(yaml.dump(config, allow_unicode=True, default_flow_style=False, sort_keys=False))
        else:
            print('ERROR: Project {} does not exist.'.format(name))