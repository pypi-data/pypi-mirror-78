kHPOGridEnvPath = 'HPOGRID_BASE_PATH'

kProjectConfigNameJson = 'project_config.json'
kProjectConfigNameYaml = 'project_config.yaml'

kiDDSConfigName = 'idds_config.json'
kiDDSSearchSpaceName = 'search_space.json'
kiDDSHPinput = 'input_hyperparameters.json'
kiDDSHPoutput = 'output.json'

kConfigAction = ['create', 'recreate', 'update']

kAlgoMap = {
    'random': 'tune',
    'bayesian': 'hyperopt'
}

kConfigPaths = {
    'project': 'projects',
    'hpo': 'config/hpo',
    'search_space': 'config/search_space',
    'model': 'config/model',
    'grid': 'config/grid'
}

kSearchAlgorithms = ['hyperopt', 'skopt', 'bohb', 'ax', 'tune', 'random', 'grid', 'bayesian', 'nevergrad']
kSchedulers = ['asynchyperband', 'bohbhyperband', 'pbt']
kMetricMode = ['min', 'max']
kDefaultSearchAlgorithm = 'random'
kDefaultMetric = 'loss'
kDefaultMode = 'min'
kDefaultScheduler = 'asynchyperband'
kDefaultLogDir = './log'
kDefaultTrials = 100
kDefaultMaxConcurrent = 3
kDefaultStopping = '{"training_iteration": 1}'
kDefaultSchedulerParam = '{}'
kDefaultAlgorithmParam = '{}'
kDefaultModelParam = '{}'
kDefaultVerbosity = 0

kConfigFormat = {
    'hpo':{
        'algorithm': {
            'required': False,
            'type': str,
            'choice': kSearchAlgorithms,
            'default': 'random'
        },
        'metric' : {
            'required': True,
            'type': str,
        },
        'mode' : {
            'required': True,
            'type': str,
            'choice': kMetricMode,
        },
        'scheduler': {
            'required': False,
            'type': str,
            'choice': kSchedulers,
            'default': kDefaultScheduler
        },
        'trials': {
            'required': False,
            'type': int,
            'default': 100
        },
        'log_dir': {
            'required': False,
            'type': str,
            'default': './log'
        },
        'verbose': {
            'required': False,
            'type': int,
            'default': 0
        }
    }
}


kHPOConfigFormat = {
    'algorithm': {
        'required': False,
        'type': str,
        'choice': kSearchAlgorithms,
        'default': 'random'
    },
    'metric' : {
        'required': True,
        'type': str,
    },
    'mode' : {
        'required': True,
        'type': str,
        'choice': kMetricMode,
    },
    'scheduler': {
        'required': False,
        'type': str,
        'choice': kSchedulers,
        'default': kDefaultScheduler
    },
    'trials': {
        'required': False,
        'type': int,
        'default': 100
    },
    'log_dir': {
        'required': False,
        'type': str,
        'default': './log'
    },
    'verbose': {
        'required': False,
        'type': int,
        'default': 0
    }
}


kConfigDefaults = {
    'hpo':{
        "algorithm": "random",
        "metric": "loss",
        "mode": "min",
        "scheduler": "asynchyperband",
        "log_dir": "./log",
        "n_trial": 100,
        "max_concurrent": 3,
        "stopping": {"training_iteration": 1},
        "scheduler_param": None,
        "algorithm_param": None,
        "model_param": None
    },
    'grid': {
        "site": ['ANALY_MANC_GPU_TEST', 'ANALY_MWT2_GPU', 'ANALY_BNL_GPU_ARC'],
        "container": '/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/aml/hyperparameter-optimization/alkaid-qt/hpogrid:latest'
    }
}




kDefaultOutDS = 'user.${{RUCIO_ACCOUNT}}.hpogrid.{HPO_PROJECT_NAME}.out.$(date +%Y%m%d%H%M%S)'

kHPOGridMetadataFormat = ['project_name', 'metric', 'mode', 'task_time_s', 'result', 'hyperparameters', 'best_config', 'start_datetime', 'end_datetime', 'start_timestamp']


''''
Grid Site Related
'''

try:
    from hpogrid.utils.grid_site_info import GridSiteInfo
    kGPUGridSiteList = GridSiteInfo.list_sites()
    kGPUGridSiteList += ['ANALY_CERN-PTEST','ANY']
except:
    kGPUGridSiteList = None

kStableGPUGridSiteList = ['ANALY_MANC_GPU_TEST', 'ANALY_MWT2_GPU', 'ANALY_BNL_GPU_ARC']
kDefaultGridSite = ','.join(kStableGPUGridSiteList)

kGPUSiteNGPU = {
    'ANALY_MANC_GPU_TEST': 10, #single queue, no submission parameters, 1 GPU per job
    'ANALY_QMUL_GPU_TEST': 6, # GPUNumber=x for now is hardcoded in the dev APF JDL,number of GPUs per job limited by cgroups, K80=2*K40, so total of 6 gpu slots avalable.
    'ANALY_MWT2_GPU': 8, #single queue, no submission parameters, 1 GPU per job
    'ANALY_BNL_GPU_ARC': 12, #also shared with Jupyter users who have priority
    'ANALY_INFN-T1_GPU': 2 #single queue, no submission parameters, 1 GPU per job
}

kDefaultContainer = '/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/aml/hyperparameter-optimization/alkaid-qt/hpogrid:latest'
kDefaultContainer2 = '/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/clcheng/hyperparameter-optimization-on-the-grid:latest'
kDefaultContainer3 = 'docker://gitlab-registry.cern.ch/aml/hyperparameter-optimization/alkaid-qt/hpogrid:latest'
kDefaultContainer4 = 'docker://gitlab-registry.cern.ch/aml/hyperparameter-optimization/alkaid-qt/hpogrid:base'

kGridSiteMetadataFileName = 'userJobMetadata.json'

kWorkDir = './'
kDataDir = './'