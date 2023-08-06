import os
import sys
import glob
import argparse
import json
from typing import Optional
import tempfile
from hpogrid.components.defaults import *
from hpogrid.utils import helper, stylus
from hpogrid.components import environment_settings
from hpogrid.components.validation import validate_project_config

def transpose_config(config):
    config = validate_project_config(config)
    project_name = config['project_name']
    evaluation_container = config['grid_config']['container']
    search_space = config['search_space']
    library = config['hpo_config']['algorithm']
    method = config['hpo_config']['algorithm_param'].get('method', None)
    max_point = config['hpo_config']['num_trials']
    max_concurrent = config['hpo_config']['max_concurrent']
    in_ds = config['grid_config']['inDS']
    out_ds = config['grid_config']['outDS']
    if '{HPO_PROJECT_NAME}' in out_ds:
        out_ds = out_ds.format(HPO_PROJECT_NAME=project_name)

    # format generator command
    generator_options = {}
    generator_options['n_point'] = '%NUM_POINTS'
    generator_options['max_point'] = '%MAX_POINTS'
    generator_options['infile'] = os.path.join(kiDDSBasePath, '%IN')
    generator_options['outfile'] = os.path.join(kiDDSBasePath, '%OUT')
    generator_options['library'] = library
    if (library == 'nevergrad') and method:
        generator_options['method'] = method
    generator_cmd = 'hpogrid generate {}'.format(stylus.join_options(generator_options))

    # format idds configuration
    idds_config = {}
    idds_config['steeringExec'] = ("run --rm -v \"$(pwd)\":{idds_base_path} {container} " +\
    "/bin/bash -c \"{cmd}\" ").format(idds_base_path=kiDDSBasePath, container=kDefaultContainer, cmd=generator_cmd)
    idds_config['evaluationExec'] = "\"pip install --upgrade hpogrid & " + \
                                    "hpogrid run {project_name} --mode idds\"".format(project_name=project_name)
    idds_config['evaluationContainer'] = evaluation_container
    idds_config['evaluationInput'] = kiDDSHPinput
    idds_config['evaluationOutput'] = kiDDSHPoutput
    idds_config['evaluationMeta'] = kGridSiteMetadataFileName
    idds_config['nParallelEvaluation'] = max_concurrent
    idds_config['maxPoints'] = max_point
    if in_ds:
        idds_config['trainingDS'] = in_ds
    idds_config['outDS'] = out_ds
    return idds_config, search_space


def get_search_points():
    if not environment_settings.is_idds_job():
        raise RuntimeError('Cannot get search points for non-idds environment')
    
    workdir = helper.get_workdir()
    search_point_path = os.path.join(workdir, kiDDSHPinput)
    if not os.path.exists(search_point_path):
        raise FileNotFoundError('No such file or directory: \'{}\''.format(search_point_path))
    with open(search_point_path,'r') as search_point_file:
        search_points = json.load(search_point_file)
    return search_points

def create_idds_output_from_metadata(metadata):
    idds_output = {}
    idds_output['status'] = 0
    loss = []
    metric = summary['metric']
    for result in summary['result']:
        loss.append(result[sumetric])
    if len(loss) == 1:
        loss = loss[0]
    idds_output['loss'] = loss
    idds_output['message'] = ''
    return idds_output


def save_idds_output_from_metadata(metadata):
    if not environment_settings.is_idds_job():
        raise RuntimeError('save_output should not be called in non-idds environment')    
        
    output = create_idds_output_from_metadata(metadata)
    workdir = helper.get_workdir()
    idds_output_path = os.path.join(workdir, kiDDSHPoutput)
    with open(idds_output_path, 'w') as idds_output_file:
        print('INFO: Saved idds output at {}'.format(idds_output_path))
        json.dump(idds_output, idds_output_file, cls=helper.NpEncoder)
        
        
        
        
        
        
        