import numpy as np
import tensorflow as tf
from tensorflow.keras import losses, metrics, backend

# =================================================================
# DISABLE EAGER EXEC FOR MASKED LOSS FUNCTIONS
# =================================================================

# --- TF2.1
# model.compile(..., experimental_run_tf_function=False)

# --- TF2.2
# NOTES: works however metrics do not calculate
# if tf.__version__[:3] == '2.2':
#     tf.compat.v1.disable_eager_execution()

# =================================================================

# =================================================================
# CUSTOM KERAS LOSSES
# =================================================================

def bce(weights, scale=1.0):

    loss = losses.BinaryCrossentropy(from_logits=True)

    def bce(y_true, y_pred):

        return loss(y_true=y_true, y_pred=y_pred, sample_weight=weights) * scale

    return bce 

def sce(weights, scale=1.0):

    loss = losses.SparseCategoricalCrossentropy(from_logits=True)

    def sce(y_true, y_pred):

        return loss(y_true=y_true, y_pred=y_pred, sample_weight=weights) * scale

    return sce 

def mse(weights, scale=1.0):

    loss = losses.MeanSquaredError()

    def mse(y_true, y_pred):

        return loss(y_true=y_true, y_pred=y_pred, sample_weight=weights) * scale

    return mse

def mae(weights, scale=1.0):

    loss = losses.MeanAbsoluteError()

    def mae(y_true, y_pred):

        return loss(y_true=y_true, y_pred=y_pred, sample_weight=weights) * scale

    return mae

def sl1(weights, scale=1.0, delta=1.0):

    loss = losses.Huber(delta=delta)

    def sl1(y_true, y_pred):

        return loss(
            y_true=tf.expand_dims(y_true, axis=-1), 
            y_pred=tf.expand_dims(y_pred, axis=-1),
            sample_weight=weights) * scale

    return sl1

def dsc(weights=None, scale=1.0, epsilon=1, cls=1):
    """
    Method for generalized multi-class (up to 9) Dice score calculation

    :params

      (int) cls : class to use to for Dice score calculation (default = 1)

    """
    def calc_dsc(y_true, y_pred, c):
        """
        Method to calculate Dice coefficient

        """
        true = y_true[..., 0] == c
        pred = tf.math.argmax(y_pred, axis=-1) == c 

        if weights is not None:
            true = true & (weights[..., 0] != 0) 
            pred = pred & (weights[..., 0] != 0)

        A = tf.math.count_nonzero(true & pred) * 2
        B = tf.math.count_nonzero(true) + tf.math.count_nonzero(pred) + epsilon

        return (A / B) * scale

    def dsc_1(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 1) 

    def dsc_2(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 2) 

    def dsc_3(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 3) 

    def dsc_4(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 4) 

    def dsc_5(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 5) 

    def dsc_6(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 6) 

    def dsc_7(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 7) 

    def dsc_8(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 8) 

    def dsc_9(y_true, y_pred):
        return calc_dsc(y_true, y_pred, 9) 

    funcs = {
        1: dsc_1,
        2: dsc_2,
        3: dsc_3,
        4: dsc_4,
        5: dsc_5,
        6: dsc_6,
        7: dsc_7,
        8: dsc_8,
        9: dsc_9}

    assert cls < 10, 'ERROR only up to 9 classes implemented in custom.dsc() currently'

    return [funcs[i] for i in range(1, cls + 1)]

# =================================================================
# CUSTOM KERAS LOSSES
# =================================================================

def acc(weights=None, epsilon=1e-6):
    """
    Method to implement masked accuracy on raw softmax cross-entropy logits

    NOTE: weights tensor is treated as a mask (values binarized)

    """

    def accuracy(y_true, y_pred):

        y_pred = tf.expand_dims(backend.argmax(y_pred), axis=-1)

        y_true = tf.cast(y_true, tf.int64)
        y_pred = tf.cast(y_pred, tf.int64)

        num = y_true == y_pred
        den = y_true > -1

        if weights is not None:
            num = num & (weights != 0) 
            den = den & (weights != 0) 

        num = tf.math.count_nonzero(num)
        den = tf.math.count_nonzero(den)

        num = tf.cast(num, tf.float32)
        den = tf.cast(den, tf.float32) + epsilon

        return num / den

    return accuracy

def softmax_ce_sens(weights=None, threshold=0.5, epsilon=1e-6):
    """
    Method to implement masked sensitivity (recall) on raw softmax cross-entropy logits

    NOTE: weights tensor is treated as a mask (values binarized)

    """
    def softmax_ce_sens(y_true, y_pred):

        p = tf.nn.softmax(y_pred)
        tp = (p[..., 1:] > threshold) & (y_true == 1)

        if weights is not None:
            tp = tp & (weights != 0)
            y_true = (y_true == 1) & (weights != 0)

        num = tf.math.count_nonzero(tp) 
        den = tf.math.count_nonzero(y_true)

        num = tf.cast(num, tf.float32)
        den = tf.cast(den, tf.float32) + epsilon

        return num / den

    return softmax_ce_sens 

def softmax_ce_ppv(weights=None, threshold=0.5, epsilon=1e-6):
    """
    Method to implement masked PPV (precision) on raw softmax cross-entropy logits

    NOTE: weights tensor is treated as a mask (values binarized)

    """
    def softmax_ce_ppv(y_true, y_pred):

        p = tf.nn.softmax(y_pred)
        pp = p[..., 1:] > threshold
        tp = pp & (y_true == 1)

        if type(weights) is not float:
            tp = tp & (weights != 0)
            pp = pp & (weights != 0)

        num = tf.math.count_nonzero(tp) 
        den = tf.math.count_nonzero(pp)

        num = tf.cast(num, tf.float32)
        den = tf.cast(den, tf.float32) + epsilon

        return num / den

    return softmax_ce_ppv

# =================================================================
# CUSTOM SIGMOID CROSS-ENTROPY 
# =================================================================

def focal_sigmoid_ce(weights=1.0, scale=1.0, gamma=2.0, alpha=0.25):
    """
    Method to implement focal sigmoid (binary) cross-entropy loss

    """
    def focal_sigmoid_ce(y_true, y_pred):

        # --- Calculate standard cross entropy with alpha weighting
        loss = tf.nn.weighted_cross_entropy_with_logits(
            labels=y_true, logits=y_pred, pos_weight=alpha)

        # --- Calculate modulation to pos and neg labels 
        p = tf.math.sigmoid(y_pred)
        modulation_pos = (1 - p) ** gamma
        modulation_neg = p ** gamma

        mask = tf.dtypes.cast(y_true, dtype=tf.bool)
        modulation = tf.where(mask, modulation_pos, modulation_neg)

        return tf.math.reduce_mean(modulation * loss * weights * scale)

    return focal_sigmoid_ce

def sigmoid_ce_sens(weights=1.0, threshold=0.5, epsilon=1e-6):
    """
    Method to implement sensitivity (recall) on raw sigmoid (binary) cross-entropy logits

    """
    def sigmoid_ce_sens(y_true, y_pred):

        p = tf.math.sigmoid(y_pred)
        tp = (p > threshold) & (y_true == 1)

        num = tf.math.count_nonzero(tp) 
        den = tf.math.count_nonzero(y_true)

        num = tf.cast(num, tf.float32)
        den = tf.cast(den, tf.float32) + epsilon

        return num / den

    return sigmoid_ce_sens

def sigmoid_ce_ppv(weights=1.0, threshold=0.5, epsilon=1e-6):
    """
    Method to implement PPV (precision) on raw sigmoid (binary) cross-entropy logits

    """
    def sigmoid_ce_ppv(y_true, y_pred):

        p = tf.math.sigmoid(y_pred)
        tp = (p > threshold) & (y_true == 1)

        num = tf.math.count_nonzero(tp) 
        den = tf.math.count_nonzero(p > threshold)

        num = tf.cast(num, tf.float32)
        den = tf.cast(den, tf.float32) + epsilon

        return num / den

    return sigmoid_ce_ppv

# =================================================================
# CUSTOM LAYERS AND FUNCTIONS 
# =================================================================

def flatten(x):
    """
    Method to flatten all defined axes (e.g. not None)

    WARNING: If possible, layers.Flatten(...) is preferred for speed and HDF5 serialization compatibility

    """
    # --- Calculate shape
    ll = x._shape_as_list()
    ss = [s for s in tf.shape(x)]

    shape = []
    adims = []

    for l, s in zip(ll, ss):
        if l is None:
            shape.append(s)
        else:
            shape.append(1)
            adims.append(l)

    shape[-1] = np.prod(adims)

    return tf.reshape(x, shape)
