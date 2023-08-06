import os
import sys
import json
import yaml
import shutil
import tarfile
import argparse
import numpy as np
import multiprocessing
from typing import List, Dict
from contextlib import contextmanager

from hpogrid.components.defaults import *

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)

def local_setup():
    os.environ['HPOGRID_DATA_DIR'] = os.getcwd()
    os.environ['HPOGRID_WORK_DIR'] = os.getcwd()
        
def grid_site_setup():
    os.environ['ENABLE_HPOGRID_RUN'] = 'TRUE'
    # there is probably a better way to get the working directory but 
    # for now just follow https://twiki.cern.ch/twiki/bin/viewauth/AtlasComputing/SingularityInAtlas
    # to use os.getcwd()
    os.environ['HPOGRID_DATA_DIR'] = os.getcwd()
    os.environ['HPOGRID_WORK_DIR'] = os.getcwd()

def get_workdir():
    return os.environ.get('HPOGRID_WORK_DIR', os.getcwd())

def get_datadir():
    return os.environ.get('HPOGRID_DATA_DIR', os.getcwd())

def is_grid_job_running():
    return os.environ.get('ENABLE_HPOGRID_RUN', None)=='TRUE'

def set_base_path(path:str) -> None:
    os.environ[kHPOGridEnvPath] = path

def get_base_path():
    if kHPOGridEnvPath not in os.environ:
        print('WARNING: {} environment variable not set.'
            'Set to current working directory by default.'.format(kHPOGridEnvPath))
        self.set_base_path(os.getcwd())
    return os.environ.get(kHPOGridEnvPath, os.getcwd())

def set_script_path(proj_name, undo=False):
    project_path = get_project_path(proj_name)
    script_path = os.path.join(project_path, 'scripts')
    
    if (script_path in sys.path) and (undo==True):
        sys.path.remove(script_path)
        os.environ["PYTHONPATH"].replace(script_path+":","")
        
    if (script_path not in sys.path) and (undo==False):
        sys.path.append(script_path)
        os.environ["PYTHONPATH"] = script_path + ":" + os.environ.get("PYTHONPATH", "")

def get_project_path(proj_name):
    if is_grid_job_running():
        proj_path = get_datadir()
    else:
        base_path = get_base_path()
        proj_path = os.path.join(base_path, 'project', proj_name)
    if not os.path.exists(proj_path):
        raise RuntimeError('Project "{}" not found.'.format(proj_name))
    return proj_path

def load_configuration(config_input:[Dict, str]) -> Dict:
    if isinstance(config_input, dict):
        return config_input
    elif isinstance(config_input, str):
        with open(config_input, 'r') as file:
            ext = os.path.splitext(config_input)[1]
            if ext in ['.txt', '.yaml']:
                config = yaml.safe_load(file)
            elif ext == '.json':
                config = json.load(file)
            else:
                raise ValueErrror('The configuration file has an unsupported '
                              'file extension: {}\n Supported file extensions '
                              'are .txt, .yaml or .json'.format(ext))
        return config
    else:
        raise ValueError('Unknown configuration format: {}'.format(type(config_input)))

def get_project_config(proj_name):
    project_path = get_project_path(proj_name)
    config_path = os.path.join(project_path, 'config', kProjectConfigNameJson)
    if not os.path.exists(config_path):
        raise FileNotFoundError('Missing project configuration file: {}'.format(config_path))
    config = load_configuration(config_path)
    return config

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def get_physical_devices(device_type='GPU'):
    import tensorflow as tf
    physical_devices = tf.config.list_physical_devices('GPU')
    return physical_devices

def get_n_gpu():
    import torch
    return torch.cuda.device_count()

def get_n_cpu():
    return multiprocessing.cpu_count()


def extract_tarball(in_path:str, out_path:str) ->List[str]:
    tarfiles = [ f for f in os.listdir(in_path) if f.endswith('tar.gz')]
    extracted_files = []
    for f in tarfiles:
        tar = tarfile.open(f, "r:gz")
        print('untaring the file {}'.format(f))
        tar.extractall(path=out_path)
        extracted_files += tar.getnames()
        tar.close()
    return extracted_files

def remove_files(files:List[str]):
    for f in files:
        if os.path.isfile(f):
            os.remove(f)
        elif os.path.isdir(f):
            shutil.rmtree(f)        
