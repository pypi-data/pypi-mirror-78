import pkg_resources

# ========================================================================
# JARVIS LOAD / SAVE API 
# =========================================================================

def manual_npy():

    from . import parser_npy

    load_funcs = {
        'npy': parser_npy.load_npy,
        'npz': parser_npy.load_npz}

    save_funcs = {
        'npy': parser_npy.save_npy,
        'npz': parser_npy.save_npz}

    return load_funcs, save_funcs

def manual_hdf5():

    from . import parser_hdf5

    load_funcs = {
        'hdf5': parser_hdf5.load_hdf5}

    save_funcs = {
        'hdf5': parser_hdf5.save_hdf5}

    return load_funcs, save_funcs

def manual_json():

    from . import parser_json

    load_funcs = {
        'json': parser_json.load_json}

    return load_funcs, {} 

def manual_dicom():

    import jarvis_dicom

    load_funcs = {
        'dcm': jarvis_dicom.load}

    return load_funcs, {} 

def manual_nifti():

    import jarvis_nifti

    load_funcs = {
        'nii': jarvis_nifti.load_nifti,
        'gz': jarvis_nifti.load_nifti}

    return load_funcs, {} 

def manual_mvk_mzl():

    import jarvis_mvk_mzl

    load_funcs = {
        'mvk': jarvis_mvk_mzl.load_mvk,
        'mzl': jarvis_mvk_mzl.load_mzl}

    return load_funcs, {}

def load():
    """
    Method to attempt loading jarvis.utils.io plugins

      (1) Load using pkg_resources entry_points (preferred)
      (2) Load using search of known plugins (if jarvis is installed inside of iPython / Jupyter)

    """
    load_funcs = {}
    save_funcs = {}

    try:

        # --- Check if load_funcs is registered
        next(pkg_resources.iter_entry_points('load_funcs'))

        # --- If non-empty, load any registered LOAD / SAVE funcs
        for entry_point in pkg_resources.iter_entry_points('load_funcs'):
            load_funcs[entry_point.name] = entry_point.load()

        for entry_point in pkg_resources.iter_entry_points('save_funcs'):
            save_funcs[entry_point.name] = entry_point.load()

    except:

        for manual_load in [
            manual_npy,
            manual_hdf5,
            manual_json,
            manual_dicom,
            manual_nifti,
            manual_mvk_mzl]:

            try:
                load_func, save_func = manual_load()
                load_funcs.update(load_func)
                save_funcs.update(save_func)
            except: pass

    return load_funcs, save_funcs
