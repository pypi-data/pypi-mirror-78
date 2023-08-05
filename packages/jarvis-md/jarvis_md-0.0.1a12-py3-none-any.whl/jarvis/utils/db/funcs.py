import os, importlib
import numpy as np

def init(fdefs='mr_train', root='', **kwargs):
    """
    Method to to prepare function definitions list 
    
    :params

      (str)  fdefs = 'mr_train', 'ct_train', ... OR

      (list) fdefs = [{

        'lambda': 'coord', 'stats', ... OR lambda function,
        'python': {'file': ..., 'name': ...}
        'kwargs': {...},
        'return': {...}

        }]

    :return

      (list) fdefs : fully initialized function definitions

    """
    if type(fdefs) is str:
        fdefs = get_default_fdefs(name=fdefs, **kwargs)

    assert type(fdefs) is list

    # --- Register custom functions 
    update(kwargs.get('FUNCS', {}))

    # --- Parse 
    fdefs_ = []

    for fdef in fdefs:

        fdef = {**{
            'lambda': None,
            'python': None,
            'kwargs': {},
            'return': {}}, **fdef}

        if type(fdef['lambda']) is str:
            fdef['lambda'] = FUNCS.get(fdef['lambda'], None)

        py = fdef.pop('python')

        if not hasattr(fdef['lambda'], '__call__') and type(py) is dict:
            assert 'file' in py 
            assert 'name' in py 
            fdef['lambda'] = init_python(py_file=py['file'], py_name=py['name'], root=root)

        # --- If no lambda function is defined, use identity function
        if fdef['lambda'] is None:
            fdef['lambda'] = lambda **kwargs : kwargs

        fdefs_.append(fdef)

    return fdefs_ 

def init_python(py_file, py_name, root):
    """
    Method to load Python module by filename

    """
    py_file = py_file.format(root=root)
    spec = importlib.util.spec_from_file_location(py_name, py_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return getattr(module, py_name, None)

def update(funcs):
    """
    Method to update FUNCS with dict of additional methods

    """
    FUNCS.update(funcs)

def calculate_coord(arr):
    """
    Method to calculate normalized coord positions

    """
    z = arr.shape[0]

    return {'coord': np.arange(z) / (z - 1)}

def calculate_stats(arr, name='!lbl', axis=(0, 1, 2, 3)):
    """
    Method to calculate image statistics across channels: mu, sd

    """
    mu = arr.mean(axis=tuple(axis))
    sd = arr.std(axis=tuple(axis))

    mu = {'{}-mu'.format(name[1:]): mu} 
    sd = {'{}-sd'.format(name[1:]): sd} 

    return {**mu, **sd}

def calculate_label(arr, name='!lbl', classes=2, axis=(1, 2, 3)):
    """
    Method to calculate if label class is present 

    """
    is_present = lambda c : np.sum(arr == c, axis=tuple(axis)) > 0 if type(arr) is not str else False

    return {'{}-{:02d}'.format(name[1:], c): is_present(c) for c in range(classes)}

def calculate_slices(arr):
    """
    Method to calculate total number of slices in volume

    """
    return {'slices': arr.shape[0]}

# ============================================================
# REGISTERED FUNCTIONS
# ============================================================

FUNCS = {
    'coord': calculate_coord,
    'stats': calculate_stats,
    'label': calculate_label,
    'slices': calculate_slices}

# ============================================================
# DEFAULT FUNCS_DEF
# ============================================================

def get_default_fdefs(name, dats=['dat'], lbls=None, classes=2, **kwargs):

    if name not in ['mr_train', 'xr_train', 'ct_train']:
        return []

    # --- Create generic label-derived stats
    fdefs = [{
        'lambda': 'coord',
        'kwargs': {'arr': lbls[0] if lbls is not None else dats[0]}}]

    if lbls is not None:
        fdefs += [{
            'lambda': 'label',
            'kwargs': {'arr': l, 'name': '!' + l, 'classes': classes}
            } for l in lbls]

    # --- Add data-specific stats (if needed)
    if name in ['mr_train', 'xr_train']:

        fdefs = fdefs[0:1] + [{
            'lambda': 'stats',
            'kwargs': {'arr': d, 'name': '!' + d}
            } for d in dats] + fdefs[1:]

    return fdefs

# ============================================================
