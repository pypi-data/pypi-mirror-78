import numpy as np

def extract_data(data, infos=None):
    """
    Method to extract portions or all of provided data volume

      (1) Extract full data volume (if infos is None)
      (2) Extract data centered at point with provided shape
      (3) Extract data at specified index (or indices) along any single axis

    :params

      (dict) infos 

        infos['point'] : normalized (z, y, x) coordinate for center of extracted array 
        infos['shape'] : shape of array to extract (centered at normalized coordinate)

          If s > 0 ==> s represents shape to extract
          If s = 0 ==> s spans full shape along specified axis
          If s < 0 ==> s spans full shape + padding

          For example, assuming data.shape = (32, 256, 256) then: 
          
          * infos['shape'] = (5, 0, 0)  ==> (5, 256, 256) array centered @ point
          * infos['shape'] = (-2, 0, 0) ==> (34, 256, 256) array centered @ point

        infos['index'] : index (or indices) for array slicing along any single axis

          * infos['index']['vals'] : index value(s)
          * infos['index']['axis'] : 0, 1, 2 or 3

          Note that infos['index']['vals'] may be provided in whole integer or normalized coords

    """
    if infos is None:
        return data[:]

    infos = check_infos(infos)

    centered = (infos['point'] == np.array([0.5, 0.5, 0.5])).all()

    # --- Early return: index slicing
    if 'index' in infos:

        # --- Convert float to int if needed
        vals = infos['index']['vals']
        if 'float' in str(vals.dtype):
            vals = np.round(vals * (data.shape[infos['index']['axis']] - 1)).astype('int')

        # --- Extract data from memory-mapped structures
        if not hasattr(data, 'take'):
            data = data[:]

        return data.take(vals, axis=infos['index']['axis'])

    # --- Early return: no slicing or padding
    if centered and (infos['shape'] == 0).all():
        return data[:]

    # --- Early return: no slicing, only padding
    if centered and (infos['shape'] <= 0).all():
        padval = np.floor(-infos['shape'] / 2).astype('int')
        padval = np.stack((padval, -infos['shape'] - padval)).T
        return pad(data[:], padval)

    # --- Create shapes / points 
    dshape = np.array(data.shape[:3])
    points = np.array(infos['point']) * (dshape - 1) 
    points = np.round(points)

    # --- Create slice bounds 
    shapes = np.array([i if i > 0 else d for i, d in zip(infos['shape'], dshape)])
    slices = points - np.floor(shapes / 2) 
    slices = np.stack((slices, slices + shapes)).T

    # --- Create padding values
    padval = np.stack((0 - slices[:, 0], slices[:, 1] - dshape)).T
    padval = padval.clip(min=0).astype('int')
    slices[:, 0] += padval[:, 0]
    slices[:, 1] -= padval[:, 1]

    # --- Create slices
    slices = [tuple(s.astype('int')) if i > 0 else (0, d) for s, i, d in zip(slices, shapes, dshape)] 
    slices = [slice(s[0], s[1]) for s in slices]

    data = data[slices[0], slices[1], slices[2]]

    # --- Pad array if needed
    data = pad(data, padval)

    return data

def check_infos(infos):

    if infos is not None:

        assert type(infos) is dict

        DEFAULTS = {
            'point': [0.5, 0.5, 0.5],
            'shape': [0, 0, 0]}

        infos = {**DEFAULTS, **infos}

        assert len(infos['point']) == 3
        assert len(infos['shape']) == 3

        infos['point'] = np.array(infos['point'])
        infos['shape'] = np.array(infos['shape'])

        if 'index' in infos:

            assert 'vals' in infos['index']
            infos['index']['vals'] = np.array(infos['index']['vals'])
            infos['index']['axis'] = infos['index'].get('axis', 0) 

    return infos

def pad(data, padval):
    """
    Method to pad data array with minimum value

    :params

      (np.ndarray) data : array to pad
      (np.ndarray) padval : 3 x 2 array of pad widths 

    """
    if not padval.any():
        return data

    pad_width = [(b, a) for b, a in zip(padval[:, 0], padval[:, 1])] + [(0, 0)]

    return np.pad(data, pad_width=pad_width, mode='constant', constant_values=data.min())
