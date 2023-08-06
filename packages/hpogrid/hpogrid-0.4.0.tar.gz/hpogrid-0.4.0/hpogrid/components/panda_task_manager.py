import sys, os
import ssl
import json
#import re
import fnmatch

from tqdm import tqdm
import argparse
import datetime
import pandas as pd
from pdb import set_trace



try:
    from urllib.parse import urlencode
    from urllib.parse import urljoin
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError, URLError
except ImportError:
    from urllib import urlencode
    from urllib2 import urlopen, Request, HTTPError, URLError
    from urlparse import urljoin

import pandas as pd 
from tabulate import tabulate
from colorama import Fore, Back, Style

try:
    from pandatools import PBookCore
    from pandatools import Client
    from pandatools.PBookCore import PsubUtils
except:
    raise ImportError('No module named \'pandatools\'. Please do '
        '\'setupATLAS\' and \'lsetup panda\' first ')


kPandaTaskManagerMethods = ['show', 'kill', 'retry', 'killAndRetry']

kPanDA_URL = 'https://bigpanda.cern.ch/'
kPanDA_TaskURL = 'https://bigpanda.cern.ch/tasks/'
kPanDA_JobURL = 'https://bigpanda.cern.ch/jobs/'

kPanDAVerifyPath = {
    'cafile' : '/etc/pki/tls/cert.pem',
    'capath' : '/etc/pki/tls/certs',
}

kHeaders = {'Accept': 'application/json', 'Content-Type':'application/json'}


kTaskActiveSuperstatusList = ['running', 'submitting', 'registered', 'ready']
KTaskFinalSuperstatusList = ['finished', 'failed', 'done', 'broken', 'aborted']
kStandardColumns = ['jeditaskid', 'status', 'pctfinished','taskname']
kOutputColumns = ['jeditaskid', 'status', 'taskname', 'computingsite', 'site', 'metastruct']

kStatusLen = 8
kLine = '_'*90
kStrf = '{jeditaskid:>10}  {status:<{l}}  {pctfinished:>5} {taskname}'
kHead = kStrf.format(l=kStatusLen, status='Status', jeditaskid='JediTaskID',
    pctfinished='Fin%', taskname='TaskName') +'\n' + kLine

RED = '\033[0;91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
BLINK = '\033[5m'
kColorDict = {
    'running': BLUE + BOLD,
    'submitting': CYAN,
    'registered': MAGENTA,
    'ready': MAGENTA,
    'pending': MAGENTA,
    'done': GREEN,
    'finished': YELLOW,
    'broken': RED + BOLD ,
    'exhausted': RED,
    'aborted': RED,
    'failed': RED,
    }


class PandaTaskManager():

    def __init__(self, enable_parser=False):
        print('INFO: Verifying Grid Proxy...')
        self.pbook = PBookCore.PBookCore()
        print('INFO: Verification is Sucessful.')
        self.context = ssl.SSLContext()
        #self.context = ssl._create_unverified_context()
        self.context.load_verify_locations(**kPanDAVerifyPath)

        # call functions via hpogrid executable
        if enable_parser:
            self.run_parser()

    def run_parser(self):
        base_parser = self.get_parser()
        args = base_parser.parse_args(sys.argv[2:3])
        method = args.method
        method_parser = self.get_parser(method)
        if not method_parser:
            print('Unrecognized method: {}'.format(method))
            base_parser.print_help()
            exit(1)
        args = method_parser.parse_args(sys.argv[3:])
        getattr(self, method)(args)

    def get_parser(self, method=None):
        parser = None
        if method == None:
            parser = argparse.ArgumentParser()
            parser.add_argument('method', help='Method to call',
                choices=kPandaTaskManagerMethods)    
        elif method == 'show':
            parser = argparse.ArgumentParser(description='show PanDA task status',
                        formatter_class=argparse.RawDescriptionHelpFormatter)      
            parser.add_argument('-u','--username',
                help='filter tasks by username')
            parser.add_argument('-l','--limit', type=int, default=1000,
                help='the maximum number of tasks to query')
            parser.add_argument('-d', '--days', type=int, default=30,
                help='filter tasks within the recent N days')
            parser.add_argument('-n', '--taskname', 
                help='filter tasks by taskname (accept wildcards)')
            parser.add_argument('-i', '--jeditaskid',
                help='only show the task with the specified jeditaskid')
            parser.add_argument('-m', '--metadata', action='store_true',
                help='print out the metadata of a task')
            parser.add_argument('-s', '--sync', action='store_true',
                help='force no caching on the PanDA server')
            parser.add_argument('-r', '--range',
                help='filter tasks by jeditaskid range')
            parser.add_argument('-o', '--output',
                help='output result with the filename if specified')
            parser.add_argument('-c', '--outcol',
                help='data columns to be saved in output',
                default=kOutputColumns)
        elif (method in ['kill', 'retry', 'killAndRetry']):
            parser = argparse.ArgumentParser(description='kill/retry a PanDA task',
                        formatter_class=argparse.RawDescriptionHelpFormatter)   
            parser.add_argument('jeditaskid', help='jeditaskid of the task')   

        return parser

    def get_response(self, req, out_json=True):
        response = urlopen(req, context=self.context).read().decode('utf-8')
        if out_json:
            response = json.loads(response)
        return response

    def get_request(self, base_url, params, headers=kHeaders):
        url = '{0}?{1}'.format(base_url, urlencode(params))
        req = Request(url, headers=headers)
        return req

    def get_request_url(self, req):
        url = req.get_full_url()
        return url


    def query_by_jeditaskid(self, taskids):
        params = {
            'json': 1,
            'status': 'done',
            'extra': 'metastruct'
        }
        if not isinstance(taskids, list):
            taskids = [taskids]
        response = []
        pbar = tqdm(taskids)
        for tid in pbar:
            pbar.set_description("Processing taskid %s" % tid)
            params['jeditaskid'] = tid
            req = self.get_request(kPanDA_TaskURL, params)
            response += self.get_response(req)
        return response



    def query_tasks(self, taskname=None, jeditaskid=None, username=None, limit=1000,
        status=None, superstatus=None, days=30, sync=False, metadata=False, **args):
        if username is None:
            username = self.pbook.username

        params = { 
        'json': 1,
        'limit':limit,
        'jeditaskid': jeditaskid,
        'username': username,
        'taskname': taskname,
        'status': status,
        'superstatus': superstatus,
        'days': days
        }

        params = {k: v for k, v in params.items() if v is not None}
    
        if sync:
            params['sync'] = int(time.time())
        
        if metadata:
            params['extra'] = 'metastruct'
            params['status'] = 'done'
        

        print('INFO: Showing only max {} tasks in last {} days.'
            ' One can set "--days N" to see tasks in last N days,'
            ' and "--limit M" to see at most M latest tasks'
            .format(limit, days))

        response = None
        req = self.get_request(kPanDA_TaskURL, params)
        response = self.get_response(req)

        n_jobs = len(response)
        if metadata and (n_jobs > 100):
            print('INFO: Fetching metadata for {} jobs '
                'which is greater than the maximum limit (100). '
                'Will need to fetch metadata individually which '
                'will be slower...\n'
                'TIPS: Try to filter tasks by their task name to '
                'remove irrelevant tasks'.format(n_jobs))
            overflow_task_ids = [res['jeditaskid'] for res in response[100:]]
            params['limit'] = 100
            req = self.get_request(kPanDA_TaskURL, params)
            response = self.get_response(req)
            response += self.query_by_jeditaskid(overflow_task_ids)

        return response

    def set_status_color(self, params):
        status = params['status']
        color = kColorDict.get(status,ENDC)
        params['status'] = color+status+ENDC
        nonprlen = len(color) + len(ENDC)
        params['l'] = kStatusLen+nonprlen

    def getUserJobMetadata(self, task_id):
        _, metadata = Client.getUserJobMetadata(task_id)
        return metadata

    def print_standard(self, datasets):
        filtered_data = []
        print(kHead)
        for task in datasets:
            params = { k:task[k] for k in kStandardColumns if not k.startswith('pct')}
            params_pct = { k:'{0}%'.format(task['dsinfo'][k]) for k in kStandardColumns if k.startswith('pct')}
            params.update(params_pct)
            filtered_data.append(params.copy())
            self.set_status_color(params)
            print(kStrf.format(**params))

    def print_metadata(self, datasets):
        for data in datasets:     
            if 'jobs_metadata' in data:
                print('INFO: Printing metadata for JediTaskID:',data['jeditaskid'])
                print(next(iter(data['jobs_metadata'])))

    # filter task by jeditaskid range
    def filter_range(self, datasets, frange):
        r = frange.split('-')
        if frange[0] == '-':
            datasets = [ds for ds in datasets if int(ds['jeditaskid']) <= int(r[1])]
        elif frange[-1] == '-':
            datasets = [ds for ds in datasets if int(ds['jeditaskid']) >= int(r[0])]
        else:
            datasets = [ds for ds in datasets if int(ds['jeditaskid']) in range(int(r[0]),int(r[1]))]   
        return datasets

    def filter_datasets(self, datasets, col=kOutputColumns, out_type=list):
        df = pd.DataFrame(datasets)
        df = df.filter(col).transpose()
        if out_type is list:
            df_dict = df.to_dict()
            return [df_dict[key] for key in df_dict]
        elif out_type is dict:
            return df.to_dict()
        else:
            raise TypeError('output data type {} is not supported'.format(out_type))

    def save_datasets(self, datasets, out_path, col=kOutputColumns):
        with open(out_path, 'w') as outfile:
            out_dataset = self.filter_datasets(datasets, col, out_type=dict)
            json.dump(out_dataset, outfile)

    # show task status
    def show(self, args):
        params = vars(args)
        output = params.pop('output', None)
        outcol = params.pop('outcol', None)
        print('INFO: Fetching PanDA Tasks...')
        datasets = self.query_tasks(**params)

        # filter tasks by jetitaskid range
        if args.range is not None:
            datasets = self.filter_range(datasets, args.range) 

        if args.metadata:
            self.print_metadata(datasets)
        else:
            self.print_standard(datasets)

        if output:
            self.save_datasets(datasets, output, col=outcol)


    def get_active_tasks(self):
        return pbookCore.get_active_tasks()

    def kill(self, args):
        taskid = int(args.jeditaskid)
        self.pbook.kill(taskid)

    def retry(self, args):
        taskid = int(args.jeditaskid)
        self.pbook.retry(taskid)

    def killAndRetry(self, args):
        taskid = int(args.jeditaskid)
        self.pbook.killAndRetry(taskid)



    '''
    def deprecated_query(self, params):
                req = self.get_request(kPanDA_JobURL, params)
        response_status = self.get_response(req)['jobs']
        params['fields'] = 'metastruct'
        req = self.get_request(kPanDA_JobURL, params)
        response_metadata = self.get_response(req)['jobs']
        set_trace()
        response = []
        for (status, metadata) in zip(response_status, response_metadata):
            response.append({**status,**metadata})
    '''