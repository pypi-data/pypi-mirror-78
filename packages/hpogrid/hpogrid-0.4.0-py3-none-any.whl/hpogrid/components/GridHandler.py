import os
import sys
import glob
import argparse
import json

from hpogrid.components.defaults import *
from hpogrid.utils import helper, stylus

class GridHandler():
    def __init__(self):

        # submit grid job via hpogrid executable
        if len(sys.argv) > 1:
            self.run_parser()

    def get_parser(self):
        parser = argparse.ArgumentParser(
                    formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('proj_name', help='the project to submit a grid job')               
        parser.add_argument('-n','--n_jobs', type=int, help='number of jobs to submit',
            default=1)
        parser.add_argument('-s','--site', help='site to submit the job to '
            '(this will override the grid config site setting)', choices=kGPUGridSiteList)
        parser.add_argument('-t','--time', help='same as maxCpuCount in prun which '
            'specifies the maximum cpu time for a job (prevent being killed by'
            'looping job detection)', type=int, default=-1)
        return parser

    def run_parser(self):
        parser = self.get_parser()
        if os.path.basename(sys.argv[0]) == 'hpogrid':
            args = parser.parse_args(sys.argv[2:])
        else:
            args = parser.parse_args(sys.argv[1:])
        GridHandler.submit_job(args.proj_name, args.n_jobs, args.site, args.time)
                
    @staticmethod
    def submit_job(proj_name, n_jobs=1, site=None, time=-1):

        grid_config = helper.get_project_config(proj_name)['grid_config']

        options = {}

        options['containerImage'] = grid_config['container']

        options['exec'] = '"hpogrid grid_run {}"'.format(proj_name)

        if not grid_config['retry']:
            options['disableAutoRetry'] = ''

        extra = {'forceStaged':'', 
                 'useSandbox': '',
                 'noBuild': ''}
                 
        extra['alrb'] = ''

        options.update(extra)
        # no longer valid with alrb
#        options['ctrWorkdir'] = kWorkDir
#        options['ctrDatadir'] = kDataDir

        if grid_config['inDS']:
            options['inDS'] = grid_config['inDS']

        if '{HPO_PROJECT_NAME}' in grid_config['outDS']:
            grid_config['outDS'] = grid_config['outDS'].format(HPO_PROJECT_NAME=proj_name)
        options['outDS'] = grid_config['outDS']
        if time != -1:
            options['maxCpuCount'] = str(time)

        if not site:
            site = grid_config['site']
        if (site != 'ANY'):
            options['site'] = site
            if 'GPU' in site:
                options['cmtConfig'] = 'nvidia-gpu'
            else:
                options['nCore'] = '8'
        
        # options['workDir'] = project_path # does not really work
        project_path = helper.get_project_path(proj_name)

        # construct prun command
        command = stylus.join_options(options)
        #from pdb import set_trace
        #set_trace()
        # switch to working directory to send files to WNs
        with helper.cd(project_path):
            # submit grid jobs
            for _ in range(n_jobs):
                os.system("prun {}".format(command))
