import os, glob, yaml, tarfile
from .printer import printp, printd

# ===============================================================================
# PATH MANIPULATION 
# ===============================================================================

def load_configs(name, alt_path=None, verbose=True):
    """
    Method to load Jarvis configuration file

    :params

      (str) name        : name of YML config file to load
      (str) alt_path    : alternative path to recursively search for Jarvis config directory

    """
    configs = {}

    # --- Load configs dir
    configs_dir = find_configs_dir(alt_path)
    if not os.path.exists(configs_dir):
        printd('ERROR requested Jarvis configuration dir not found', verbose=verbose)
        return {} 

    # --- Load YML file
    fname = '{}/{}.yml'.format(configs_dir, name)
    if not os.path.exists(fname):
        printd('ERROR requested YML configuration file {} not found'.format(fname), verbose=verbose)
        return {} 

    with open(fname, 'r') as y:
        configs = yaml.load(y, Loader=yaml.FullLoader)

    return configs

def find_configs_dir(alt_path=None): 
    """
    Method to find Jarvis configs directory 

      (1) Manually set $JARVIS_PATH_CONFIGS shell var
      (2) Default location $HOME/.jarvis
      (3) Recursive search against alt_path argument

    """
    # --- (1) Check ENV vars
    if os.environ.get('JARVIS_PATH_CONFIGS', '') != '':
        return os.environ['JARVIS_PATH_CONFIGS']

    # --- (2) Check default location
    configs_dir = '{}/.jarvis'.format(os.environ.get('HOME', '.'))
    if os.path.exists(configs_dir):
        return configs_dir

    # --- (3) Check alt_path
    if alt_path is None:
        return configs_dir 

    configs_dir = alt_path
    while configs_dir.count('/') > 2:

        pp = os.path.dirname(configs_dir.replace('/.jarvis', ''))
        configs_dir = '{}/.jarvis'.format(pp)

        if os.path.exists(configs_dir):
            return configs_dir

    # --- Return default location if None is present
    return '{}/.jarvis'.format(os.environ.get('HOME', '.'))

def save_configs(configs, name, alt_path=None):
    """
    Method to save Jarvis configuration file

    """
    # --- Load YML file
    configs_dir = find_configs_dir(alt_path=alt_path)
    fname = '{}/{}.yml'.format(configs_dir, name)

    os.makedirs(os.path.dirname(fname), exist_ok=True)
    with open(fname, 'w') as y:
        yaml.dump(configs, y)

def set_paths(paths, project_id, version_id=None, verbose=False):
    """
    Method to update global $HOME/.jarvis/paths.yml with new paths

    :params

      (str) project_id 
      (str) paths

    """
    # --- Load
    configs = load_configs('paths', verbose=verbose)

    # --- Configure paths
    if type(paths) is str:
        paths = {'code': paths, 'data': paths}

    assert type(paths) is dict

    remove_slash = lambda x : x[:-1] if x[-1] == '/' else x
    paths = {**{'code': '', 'data': ''}, **paths}
    paths = {k: remove_slash(v or '/') for k, v in paths.items()}

    # --- Version
    paths['code'] = path_sub_version(paths['code'], version_id)

    configs[project_id] = paths

    # --- Save
    save_configs(configs, 'paths')

    return configs[project_id] 

def get_paths(project_id, version_id=None, alt_path=None, configs=None, verbose=True):
    """
    Method to read global $HOME/.jarvis/paths.yml

    NOTE: if version_id is provided (or set as ENV), paths['code'] will be updated

    """
    # --- Load
    configs = configs or load_configs('paths', alt_path=alt_path, verbose=verbose)
    paths = {**{'code': '', 'data': ''}, **configs.get(project_id, {})}

    # --- Add version if available
    version_id = version_id or os.environ.get('JARVIS_VERSION_ID', None)
    if version_id is not None and paths['code'] != '':
        paths['code'] = path_add_version(paths['code'], version_id)

    return paths 

def path_add_version(code, version_id):
    """
    Method to intergrate version_id into code path

    """
    if version_id is None:
        return code

    if code != '':
        code = '{}/{}'.format(code, version_id)

    return code

def path_sub_version(code, version_id):
    """
    Method to remove version_id from code path

    """
    if version_id is None:
        return code

    if version_id in code:
        code = code.replace('/{}'.format(version_id), '')

    return code

def parse_args(*args, **kwargs):
    """
    Method to parse args / kwargs for:

      (1) _id   : project_id / version_id
      (1) files : yml / csv files
      (2) paths : path locations 

    NOTE: this method is used for DB and Client objects

    """
    paths = {'data': '', 'code': ''}
    files = {'csv': None, 'yml': None}

    # --- Extract values from args 
    for arg in args:
        if type(arg) is str:
            ext = arg.split('.')[-1]
            if ext in ['yml']:
                files['yml'] = arg
            if ext in ['csv', 'gz']:
                files['csv'] = arg

    _id = parse_ids(**kwargs)

    # ==============================================================
    # DETERMINE PATH LOCATIONS 
    # ==============================================================

    if 'paths' in kwargs:
        paths = kwargs.pop('paths')

    # ==============================================================
    # DETERMINE FILE LOCATIONS
    # ==============================================================

    # --- (1) Use explicit yml / csv files
    for k in ['csv', 'yml']:
        if k in kwargs:
            files[k] = kwargs.pop(k)

    # --- (2) Use prefix + subdir
    if 'prefix' in kwargs:

        subdir = kwargs.pop('subdir', 'data')
        prefix = kwargs.pop('prefix')

        if paths['code'] == '':
            alt_path = files['yml'] or files['csv'] 
            paths = get_paths(_id['project'], _id['version'], alt_path=alt_path) 

        assert paths['code'] != '', 'ERROR use of prefix/subdir requires valid project_id'

        # --- Use glob
        if '*' in prefix:
            try:
                prefix = glob.glob('{}/{}/ymls/{}.yml'.format(paths['code'], subdir, prefix))
                prefix = sorted(prefix)[0]
                prefix = os.path.basename(prefix)[:-4] 
            except:
                assert False, 'ERROR glob(..) could not find any files based on prefix'

        files['csv'] = '/{}/csvs/{}.csv.gz'.format(subdir, prefix)
        files['yml'] = '/{}/ymls/{}.yml'.format(subdir, prefix)

    # --- Clean
    if paths['code'] != '':
        for k in ['csv', 'yml']:
            if files[k] is not None:
                files[k] = files[k].replace(paths['code'], '', 1)

    return {'_id': _id, 'files': files, 'paths': paths} 

def parse_ids(**kwargs):
    """
    Method to parse project_id and version_id from kwargs and ENV variables 

    """
    _id = {'project': None, 'version': None}

    if '_id' in kwargs:
        _id = kwargs.pop('_id')

    if 'project_id' in kwargs:
        _id['project'] = kwargs.pop('project_id')
        _id['version'] = kwargs.pop('version_id', None)

    if 'JARVIS_PROJECT_ID' in os.environ:
        _id['project'] = os.environ.get('JARVIS_PROJECT_ID')
        _id['version'] = os.environ.get('JARVIS_VERSION_ID', None)

    return _id

# ===============================================================================
# AUTODETECTION CODE (DEPRECATED) 
# ===============================================================================

def autodetect(path='', pattern=None):
    """
    Method to autodetect project_id, version_id, paths and files

    """
    # --- Read defaults based on ENV variables
    project_id = os.environ.get('JARVIS_PROJECT_ID', None) 
    version_id = os.environ.get('JARVIS_VERSION_ID', None) 
    paths = get_paths(project_id, version_id)

    # --- Attempt extraction at active path for inference
    path = autodetect_active_path(path, pattern, paths, project_id, version_id)

    is_subpath = lambda x : (x in path) and (x != '')

    # --- Attempt extraction of project_id 
    if project_id is None:

        # --- Loop through available paths
        configs = load_configs('paths')
        for pid in configs:

            # --- Get expanded paths
            p = get_paths(pid, version_id=version_id, configs=configs)

            if is_subpath(p['code']) or is_subpath(p['data']):
                project_id = pid
                paths = p

                break

    # --- Attempt extraction of version_id
    if version_id is None and project_id is not None:

        if is_subpath(paths['code']) and paths['code'] != path:

            suffix = path.split(paths['code'])[1][1:]
            if '/' in suffix:
                suffix = suffix.split('/')[0]
            if len(suffix) > 1:
                if suffix[0] == 'v' and suffix[1].isnumeric():
                    version_id = suffix
                    paths['code'] = path_add_version(paths['code'], version_id)

    # --- Attempt extraction of files
    files = autodetect_files(pattern, paths, project_id, version_id)

    trim = lambda x : os.path.abspath(x).replace(paths['code'], '') if x is not None else None
    files['yml'] = trim(files['yml']) 
    files['csv'] = trim(files['csv']) 

    return project_id, version_id, paths, files

def autodetect_active_path(path, pattern, paths, project_id=None, version_id=None):
    """
    Method to determine active path to use for autodetect(...) function

    Inference is based off of the following priority:

      (1) Provided path (if exists)
      (2) JARVIS_{*}_FILE ENV variable
      (3) Current working directory

    """
    if os.path.exists(path):
        return path

    # --- Check ENV
    for ext in ['yml', 'csv']:
        fname = autodetect_filepath(ext, pattern, paths, project_id, version_id)
        if os.path.exists(fname or ''):
            return fname

    # --- Check CWD
    return os.getcwd()

def autodetect_files(pattern=None, paths=None, project_id=None, version_id=None):
    """
    Method to autodetect relative files based on ENV variables and provided patterns

    """
    # --- Infer files fully from yml if possible
    yml = autodetect_filepath('yml', pattern, paths, project_id, version_id)
    if os.path.exists(yml or ''):
        y = yaml.load(open(yml, 'r'), Loader=yaml.FullLoader)
        return y.get('files', {'csv': None, 'yml': yml})

    # --- Infer csv alone from autodetect
    csv = autodetect_filepath('csv', pattern, paths, project_id, version_id)
    return {'yml': None, 'csv': csv}

def autodetect_filepath(ext='yml', pattern=None, paths=None, project_id=None, version_id=None):
    """
    Method to autodetect full file path based on ENV variables and provided pattern

    Inference is based off of the following priority:

      (1) JARVIS_{*}_FILE ENV variable - use as full path if exists
      (2) JARVIS_{*}_FILE ENV variable - use as pattern if nonempty 
      (3) pattern = ... (provided kwarg) 
      (4) pattern = '*' 

    :params

      (bool) remove_root : if True, attempt to remove root to path

      NOTE: remove_root is NOT guaranteed to work (e.g. if JARVIS_{}_FILE is set)

    """
    fname = os.environ.get('JARVIS_{}_FILE'.format(ext.upper()), None)
    if os.path.exists(fname or ''):
        return fname 

    # --- Determine code path 
    paths = paths or {}
    paths = {**{'code': None, 'data': None}, **paths}

    if paths['code'] is None:
        paths = get_paths(project_id, version_id)

    if not os.path.exists(paths['code']):
        return None 

    # --- Search
    pattern = fname or pattern or '*'
    matches = glob.glob('{}/**/{}s/{}.{}'.format(paths['code'], ext, pattern, ext), recursive=True)
    fname = sorted(matches)[0] if len(matches) > 0 else None 

    return fname

# ===============================================================================
# TAR TOOLS 
# ===============================================================================

def unarchive(tar, path='.'):
    """
    Method to unpack *.tar(.gz) archive (and sort into appropriate folders)

    """
    with tarfile.open(tar, 'r:*') as tf:
        N = len(tf.getnames())
        for n, t in enumerate(tf):
            printp('Extracting archive ({:07d} / {:07d})'.format(n + 1, N), (n + 1) / N)
            tf.extract(t, path)
