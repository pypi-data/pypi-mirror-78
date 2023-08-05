import numpy as np

def montage(arr, N=None, squeeze=True, rgb=False):
    """
    Method to create a tiled N x N montage of input volume arr 

    """
    if type(arr) is not np.ndarray:
        return arr

    arr = arr.squeeze().copy()

    # --- Create 4D volume
    if arr.ndim == 2:
        arr = np.expand_dims(arr, axis=0)

    if arr.ndim == 3:
        if rgb:
            arr = np.expand_dims(arr, axis=0)
        else:
            arr = np.expand_dims(arr, axis=-1)

    assert arr.ndim == 4

    # --- Normalize if RGB
    if rgb:
        lo = np.min(arr, axis=(1, 2, 3), keepdims=True)
        hi = np.max(arr, axis=(1, 2, 3), keepdims=True)
        arr = (arr - lo) / (hi - lo)

    z, y, x, c = arr.shape

    N = N or int(np.ceil(np.sqrt(z)))
    Z = int(np.ceil(z / N ** 2))
    M = np.zeros((Z, N * y, N * x, c), dtype=arr.dtype)

    n = 0
    for z_ in range(Z):
        for y_ in range(N):
            for x_ in range(N):

                yy = y_ * y
                xx = x_ * x
                M[z_, yy:yy + y, xx:xx + x, :] = arr[n]

                n += 1
                if n >= z: 
                    break
            if n >= z: 
                break
        if n >= z: 
            break

    if squeeze and not rgb:
        M = M[..., 0]

    return M

def interleave(arrs, **kwargs):
    """
    Method to interleave a 5D array 

    :params

      (np.ndarray) arrs : stack of 4D arrays to interleave

    """
    # --- Create 5D volume
    if arrs.ndim == 4:
        arrs = np.expand_dims(arrs, axis=-1)

    # --- Create montages
    z = arrs.shape[1]
    mnts = [montage(arrs[:, i], **kwargs) for i in range(z)]

    s = mnts[0].shape
    M = np.empty((s[0] * z, s[1], s[2]), dtype=arrs.dtype)

    for i in range(z):
        M[i::z] = mnts[i]

    return M
