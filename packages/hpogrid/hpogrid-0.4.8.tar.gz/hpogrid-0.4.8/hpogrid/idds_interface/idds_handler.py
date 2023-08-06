import os
import sys
import glob
import argparse
import json
from typing import Optional

from pdb import set_trace

from hpogrid.components.defaults import *
from hpogrid.utils import helper, stylus

class iDDSHandler():
    def __init__(self):

        # submit grid job via hpogrid executable
        if len(sys.argv) > 1:
            self.run_parser()

    def get_parser(self):
        parser = argparse.ArgumentParser(
                    formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('proj_name', help='the project to submit a grid job')               
        parser.add_argument('-s','--site', help='site to submit the job to '
            '(this will override the grid config site setting)', choices=kGPUGridSiteList)
        return parser

    def run_parser(self):
        parser = self.get_parser()
        if os.path.basename(sys.argv[0]) == 'hpogrid':
            args = parser.parse_args(sys.argv[2:])
        else:
            args = parser.parse_args(sys.argv[1:])
        iDDSHandler.submit_job(args.proj_name, args.site)
        
    @staticmethod
    def submit_job(project_name:str, site:Optional[str]=None):
        config = helper.get_project_config(project_name)
        project_path = helper.get_project_path(project_name)
        search_space_path = os.path.join('config', kiDDSSearchSpaceName)
        
        project_name = config['project_name']
        evaluation_container = config['grid_config']['container']
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
        generator_options['infile'] = os.path.join(kWorkDir, '%IN')
        generator_options['outfile'] = os.path.join(kWorkDir, '%OUT')
        generator_options['library'] = library
        if method:
            generator_options['method'] = method
        generator_cmd = 'hpogrid generate ' + stylus.join_options(generator_options)
        
        # format idds options
        idds_options = {}
        idds_options['searchSpaceFile'] = search_space_path
        idds_options['steeringExec'] = (r"'run --rm -v \"$(pwd)\":{workdir} {container} "
        r"/bin/bash -c \"{cmd}\" '").format(workdir=kWorkDir, container=kDefaultContainer, cmd=generator_cmd)
        idds_options['evaluationExec'] = '"hpogrid idds_run {project_name}"'.format(project_name=project_name)
        idds_options['evaluationContainer'] = evaluation_container
        idds_options['evaluationInput'] = kiDDSHPinput
        idds_options['evaluationOutput'] = kiDDSHPoutput
        idds_options['evaluationMeta'] = kGridSiteMetadataFileName
        idds_options['nParallelEvaluation'] = max_concurrent
        idds_options['maxPoints'] = max_point
        if in_ds:
            idds_options['trainingDS'] = in_ds
        idds_options['outDS'] = out_ds
        
        if not site:
            site = config['grid_config']['site']
        if (site != 'ANY'):
            idds_options['site'] = site
        
        command = stylus.join_options(idds_options)
        with helper.cd(project_path):
            # submit idds hpo jobs
            os.system("phpo {}".format(command))
        
        
        
        
        
        
        
        
        
        
        
        
        