from tensorflow.contrib import rnn as contrib_rnn
from tensorflow.python.ops.rnn_cell_impl import GRUCell

import tensorflow as tf

DEFAULTS = {
    "l1": 0,
    "l2": 0,
    "dropout": 0,
    "max_length": None,
    "layer_norm": False,
}


def get_dilations(max_length, depth):
  max_dilation = max_length & (~ max_length + 1)
  dilations = [min(2 ** i, max_dilation) for i in range(depth)]
  return dilations


def get_kernel_regularizer(l1, l2):
  reg_list = []
  if l1 > 0.:
    l1 = tf.contrib.layers.l1_regularizer(scale=l1)
    reg_list.append(l1)
  if l2 > 0.:
    l2 = tf.contrib.layers.l2_regularizer(scale=l2)
    reg_list.append(l2)
  if len(reg_list) > 0:
    sum_reg = tf.contrib.layers.sum_regularizer(reg_list)
  else:
    sum_reg = None
  return sum_reg


def get_encoder_template(encoder_type, name, **kwargs):
  args = DEFAULTS.copy()
  args.update(kwargs)

  if encoder_type == 'RNNEncoder':
    return tf.make_template(
        name, RNNEncoder,
        max_len=args['max_length'],
        hidden_dim=args['hidden_dim'],
        depth=args['depth'],
        dropout=args['dropout'],
        cell=args['rnn_cell_type'],
    )

  elif encoder_type == 'BiRNNEncoder':
    return tf.make_template(
        name, BiRNNEncoder,
        max_len=args['max_length'],
        hidden_dim=args['hidden_dim'],
        depth=args['depth'],
        dropout=args['dropout'],
        cell=args['rnn_cell_type'],
    )

  elif encoder_type == 'MLPEncoder':
    return tf.make_template(
        name, MLPEncoder,
        hidden_dim=args['hidden_dim'],
        output_dim=args.get('output_dim', args['hidden_dim']),
        depth=args['depth'],
        dropout=args['dropout'],
        l1=args['l1'],
        l2=args['l2'],
        use_bias=args.get("use_bias", True),
    )

  elif encoder_type == 'CNNEncoder':
    activation = args.get('cnn_activation', None)
    pre_activation = args.get('cnn_pre_activation', None)
    layer_norm = args['layer_norm']
    dilations = get_dilations(args['max_length'], args['depth'])

    return tf.make_template(
        name, CNNEncoder,
        num_filters=args['hidden_dim'],
        filter_width=args['filter_width'],
        conv_activation=activation,
        layer_norm=layer_norm,
        preact=pre_activation,
        dilations=dilations,
        dropout=args['dropout'],
        l1=args['l1'],
        l2=args['l2'],
    )

  elif encoder_type == 'None':
    return tf.make_template("NoneEncoder", lambda x: x)

  raise ValueError("Unknown {} type: {}".format(name, encoder_type))


def CNNEncoder(inputs,
               is_training,
               num_filters=None,
               filter_width=None,
               dilations=[1, 2],
               layer_norm=False,
               preact=None,
               conv_activation=None,
               use_bias=True,
               l1=0., l2=0., dropout=0.,
               dtype=tf.float32, name='CNNEncoder'):
  x = inputs
  regularizer = get_kernel_regularizer(l1, l2)
  for i, dilation in enumerate(dilations):
    layer_name = "{}-Layer{}".format(name, i)
    dilation = (dilation,)

    if is_training and dropout > 0.0:
      x = tf.nn.dropout(x, 1. - dropout)

    if layer_norm:
      x = tf.contrib.layers.layer_norm(x, layer_name + '_LN')

    if preact is not None:
      x = preact(x)

    x = tf.layers.conv1d(
        x, num_filters, filter_width,
        dilation_rate=dilation, padding='SAME',
        kernel_regularizer=regularizer,
        use_bias=use_bias,
        activation=conv_activation,
        name=layer_name)

  return x


def MLPEncoder(inputs,
               is_training,
               hidden_dim=64, depth=1,
               output_dim=64, use_bias=True,
               activation=tf.nn.relu,
               final_activation=None,
               dropout=0.0, l1=0.0, l2=0.0,
               dtype=tf.float32, name='MLPEncoder'):
  def mlp_layer(layer_input, output_dim, activation, layer_index):
    layer_name = "{}-Layer{}".format(name, layer_index)

    with tf.variable_scope(layer_name):
      if is_training and dropout > 0.0:
        layer_input = tf.nn.dropout(layer_input, 1. - dropout)
      regularizer = get_kernel_regularizer(l1, l2)
      outputs = tf.layers.dense(
          layer_input, output_dim, use_bias=use_bias,
          kernel_regularizer=regularizer,
          activation=activation)

    return outputs

  if depth == 1:
    state = mlp_layer(inputs, output_dim, final_activation, 0)
  else:
    state = mlp_layer(inputs, hidden_dim, activation, 0)

    for i in range(1, depth - 1):
      state = mlp_layer(state, hidden_dim, activation, i)

    state = mlp_layer(state, output_dim, final_activation, depth - 1)

  return state


def get_rnn_cell(cell_type, depth, hidden_dim, dropout, is_training):
  cells = []
  for _ in range(depth):
    if cell_type == 'lstm':
      cell = tf.nn.rnn_cell.LSTMCell(hidden_dim)
    elif cell_type == 'gru':
      cell = GRUCell(hidden_dim)
    else:
      err = "Unrecognized rnn cell type: '{}'".format(cell_type)
      raise ValueError(err)

    keep_prob = 1.0
    if is_training:
      keep_prob = 1.0 - dropout
    cells += [contrib_rnn.DropoutWrapper(cell, keep_prob)]
  return contrib_rnn.MultiRNNCell(cells)


def RNNEncoder(inputs, lengths, is_training=False,
               max_len=None,
               hidden_dim=64, depth=1, dropout=0.0,
               dtype=tf.float32, cell='lstm', name='RNNEncoder'):
  encoder_cell = get_rnn_cell(cell, depth, hidden_dim, dropout,
                              is_training)
  (fw_encoder_outputs, fw_encoder_state) = (
      tf.nn.dynamic_rnn(
          cell=encoder_cell, inputs=inputs, sequence_length=lengths,
          time_major=False, dtype=dtype)
  )

  state = tf.concat(fw_encoder_outputs, axis=1)

  if lengths is not None:
    mask = tf.sequence_mask(lengths, max_len, dtype=tf.float32)
    mask = tf.tile(tf.expand_dims(mask, 2), [1, 1, hidden_dim])
    state = state * mask

  return state


def BiRNNEncoder(inputs, lengths, is_training=False, max_len=None,
                 hidden_dim=64, depth=1, dropout=0.0, dtype=tf.float32,
                 cell='lstm', name='BiRNNEncoder'):

  fw_encoder_cell = get_rnn_cell(cell, depth, hidden_dim, dropout,
                                 is_training)
  bw_encoder_cell = get_rnn_cell(cell, depth, hidden_dim, dropout,
                                 is_training)

  (outputs, output_states) = (
      tf.nn.bidirectional_dynamic_rnn(
          cell_fw=fw_encoder_cell,
          cell_bw=bw_encoder_cell,
          inputs=inputs,
          sequence_length=lengths,
          time_major=False,
          dtype=dtype)
  )
  state = tf.concat(outputs, axis=2)

  if lengths is not None:
    mask = tf.sequence_mask(lengths, max_len, dtype=tf.float32)
    mask = tf.tile(tf.expand_dims(mask, 2), [1, 1, 2 * hidden_dim])
    state = state * mask
  return state
