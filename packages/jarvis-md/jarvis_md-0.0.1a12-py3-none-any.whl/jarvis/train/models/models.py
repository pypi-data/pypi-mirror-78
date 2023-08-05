import os, glob
import tensorflow as tf
from tensorflow.keras import layers
from ...utils.general import *

# =================================================================
# TRAIN METHODS
# =================================================================

def train(model, client, steps, save_freq=1000, tf_board=True, output_dir='.', **kwargs):
    """
    Wrapper method to run model.fit_generator(...)

      (1) Run 100 steps per epoch (default)
      (2) Run N number of epoch(s) until save_freq is obtained
      (3) Serialize model as *.hdf5
      (4) Repeat until total steps is achieved

    Default parameters for model.fit_generator() function:

      * steps_per_epoch=100
      * validation_steps=100
      * validation_freq=5

    """
    # --- Initialize arguments
    DEFAULTS = {
        'steps_per_epoch': 100,
        'validation_steps': 100,
        'validation_freq': 5,
        'validation_data': None}

    kwargs = {**DEFAULTS, **kwargs}
    kwargs['epochs'] = int(round(save_freq / kwargs['steps_per_epoch']))

    if kwargs['validation_data'] is not None:
        kwargs['validation_freq'] = int(round(kwargs['validation_steps'] * 5 / kwargs['steps_per_epoch']))
    else: 
        kwargs.pop('validation_steps')
        kwargs.pop('validation_freq')

    # --- Prepare directories
    for name in ['hdf5', 'logs']:
        os.makedirs('{}/{}'.format(output_dir, name), exist_ok=True)

    # --- Load existing weights if any
    hdfs = glob.glob('{}/hdf5/*.hdf5'.format(output_dir))
    N = len(hdfs[0].split('model_')[-1][:-5]) if len(hdfs) > 0 else 3
    model_flen = lambda N : '{}/hdf5/model_{:0%id}.hdf5' % N 
    model_name = lambda step, N : model_flen(N).format(output_dir, step)

    if len(hdfs) > 0:
        offset = max([int(s[-(N+5):-5]) for s in hdfs])
        printd('Loading existing model: {}'.format(model_name(offset, N)))
        model.load_weights(model_name(offset, N))
        offset += 1

    else:
        model.save(model_name(0, N))
        offset = 0

    # --- Add tensorboard
    if tf_board:
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir='{}/logs'.format(output_dir))
        if 'callbacks' not in kwargs:
            kwargs['callbacks'] = [tensorboard_callback]
        else:
            kwargs['callbacks'].append(tensorboard_callback)

    # --- Loop
    n = int(round(steps / (kwargs['epochs'] * kwargs['steps_per_epoch'])))

    client.to_yml('{}/client.yml'.format(output_dir))

    for step in range(offset, offset + n):

        model.fit(**kwargs)
        model.save(model_name(step, N))
        client.to_yml('{}/client.yml'.format(output_dir))

def resave(model, fname=None, output_dir='.'):
    """
    Method to resave built model with weights in the most recent *.hdf5 archive

    """
    # --- Load existing weights if any
    hdfs = glob.glob('{}/hdf5/*.hdf5'.format(output_dir))
    N = len(hdfs[0].split('model_')[-1][:-5]) + 5 if len(hdfs) > 0 else 3
    model_flen = lambda N : '{}/hdf5/model_{:0%id}.hdf5' % N 
    model_name = lambda step, N : model_flen(N).format(output_dir, step)

    if len(hdfs) > 0:
        offset = max([int(s[-7:-5]) for s in hdfs])
        printd('Loading existing model: {}'.format(model_name(offset, N)))
        model.load_weights(model_name(offset, N))

        fname = fname or model_name(offset, N)
        printd('Saving updated model: {}'.format(fname))
        model.save(fname)

    else:
        printd('ERROR no existing model weights found')

# =================================================================
# MODEL BUILDING METHODS
# =================================================================

def create_block_components(names=None, dims=2):

    # --- padding == same, z-size == 1
    kwargs_z1 = {
        'kernel_size': (1, 3, 3) if dims == 2 else (3, 3, 3),
        'padding': 'same',
        'kernel_initializer': 'he_normal'}

    # --- padding = valid, z-size == 2
    kwargs_z2 = {
        'kernel_size': (2, 1, 1),
        'padding': 'valid',
        'kernel_initializer': 'he_normal'}

    # --- padding = valid, z-size == 2
    kwargs_z3 = {
        'kernel_size': (3, 1, 1),
        'padding': 'valid',
        'kernel_initializer': 'he_normal'}

    # --- padding = same, z-size = 1, filters = 7
    kwargs_f7 = {
        'kernel_size': (1, 7, 7) if dims == 2 else (7, 7, 7),
        'padding': 'same',
        'kernel_initializer': 'he_normal'}

    # --- Define block components
    conv_z1 = lambda x, filters, strides : layers.Conv3D(filters=filters, strides=strides, **kwargs_z1)(x)
    conv_z2 = lambda x, filters, strides : layers.Conv3D(filters=filters, strides=strides, **kwargs_z2)(x)
    conv_z3 = lambda x, filters, strides : layers.Conv3D(filters=filters, strides=strides, **kwargs_z3)(x)
    conv_f7 = lambda x, filters, strides : layers.Conv3D(filters=filters, strides=strides, **kwargs_f7)(x)
    tran_z1 = lambda x, filters, strides : layers.Conv3DTranspose(filters=filters, strides=strides, **kwargs_z1)(x)
    conv_fc = lambda x, filters : (x)

    norm = lambda x : layers.BatchNormalization()(x)
    relu = lambda x : layers.LeakyReLU()(x)

    # --- Return local vars
    names = names or ('conv_z1', 'conv_z2', 'conv_z3', 'conv_f7', 'tran_z1', 'conv_fc', 'norm', 'relu')
    lvars = locals()

    return [lvars.get(n) for n in names] 

def create_blocks(names=None, dims=2, strides=None):

    # --- Create components
    conv_z1, conv_z2, conv_z3, conv_f7, tran_z1, conv_fc, norm, relu = create_block_components(names=None, dims=dims)

    # --- Define stride-1, stride-2 blocks
    if strides is None:
        strides = (1, 2, 2) if dims == 2 else (2, 2, 2)

    conv1 = lambda filters, x : relu(norm(conv_z1(x, filters, strides=1)))
    conv7 = lambda filters, x : relu(norm(conv_f7(x, filters, strides=1)))
    convZ = lambda filters, x : relu(norm(conv_z2(x, filters, strides=1)))
    conv2 = lambda filters, x : relu(norm(conv_z1(x, filters, strides=strides)))
    tran2 = lambda filters, x : relu(norm(tran_z1(x, filters, strides=strides))) 

    proj2 = lambda filters, x : conv_z2(x, filters, strides=1)
    proj3 = lambda filters, x : conv_z3(x, filters, strides=1)

    # --- Return local vars
    names = names or ('conv1', 'conv7', 'convZ', 'conv2', 'tran2', 'proj2', 'proj3')
    lvars = locals()

    return [lvars.get(n) for n in names] 

def rename_layers(model):
    """
    Method to rename all layers with '/' to '_'

    NOTE: this is needed to serialize as HDF5

    """
    for layer in model.layers:
        if layer.name.find('/') > -1:
            layer._name = layer._name.replace('/', '_')

    return model
