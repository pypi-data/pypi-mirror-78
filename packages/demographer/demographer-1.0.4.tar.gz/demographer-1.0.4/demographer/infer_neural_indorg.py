from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os
import random
import time
from collections import namedtuple

import numpy as np

from tensorflow.contrib.seq2seq import BahdanauAttention as Bahdanau
from demographer.tflm import InputDataset
from demographer.indorg_temp_dataset import TempHumanizrNames
from demographer.encoders import get_encoder_template
from demographer.utils import NumpySerializer
from demographer.experiment_runner import run_epoch
from demographer.experiment_runner import calculate_f1
from demographer.experiment_runner import infer_feature_extraction
from demographer.experiment_runner import add_tensorboard_summary

from demographer.utils import tf
if tf is None:
  raise ImportError("Need to install tensorflow")

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

flags = tf.flags
logging = tf.logging

flags.DEFINE_string("name", 'crud', "name for the job")
flags.DEFINE_string("json_output", 'experiments/crap/crud.json', "Json output path")
flags.DEFINE_string(
    "tensorboard_output", 'experiments/crap/tensorboard/crud', "Tensorboard output path")
flags.DEFINE_string("model_output", 'experiments/crap/models/crud', "Model output path")

flags.DEFINE_string("input_path", "small.json", "Dataset for inferring")
flags.DEFINE_string("setup", "balanced", "How to set up Humanizr dataset")
flags.DEFINE_float("train_balance_ratio", 1.0, "ratio of individuals to organizations")

flags.DEFINE_string("encoder1", "CNNEncoder", "Encoding each time step")
flags.DEFINE_string("collapser", 'max', 'Collapse across time to fixed size')
flags.DEFINE_string("encoder2", "MLPEncoder", "Further encode fixed size")

flags.DEFINE_integer("seed", 42, "RNG seed")
flags.DEFINE_integer("embed_dim", 256, "Document embedding dimension.")
flags.DEFINE_integer("hidden_dim", 256, "Number of nodes in [CR]?NN layer.")

flags.DEFINE_string("rnn_cell_type", 'lstm', "Type of RNN cell.")
flags.DEFINE_integer("cnn_filter_width", 3, "Width of CNN filter")
flags.DEFINE_integer("max_cnn_filter_width", 7, "Width of CNN filter")
flags.DEFINE_boolean("cnn_layer_norm", False, "Use layer norm before conv")
flags.DEFINE_string("cnn_pre_activation", "relu", "CNN pre-act")
flags.DEFINE_integer("bytenet_num_dilation_layers", 5, "Width of CNN filter")

flags.DEFINE_float("embedding_l2", 0., "l2 regularization for embedding")
flags.DEFINE_string("cnn_activation", None, "activation_fn for CNNs")
flags.DEFINE_float("encoder1_l1", 0., "l1 reg for encoder1")
flags.DEFINE_float("encoder1_l2", 0., "l2 reg for encoder1")
flags.DEFINE_float("encoder1_dropout", 0., "dropout reg for encoder1")
flags.DEFINE_float("encoder2_l1", 0., "l1 reg for encoder2")
flags.DEFINE_float("encoder2_l2", 0., "l2 reg for encoder2")
flags.DEFINE_float("encoder2_dropout", 0., "dropout reg for encoder2")
flags.DEFINE_integer("encoder1_depth", 2, "Number of layers in encoder1.")
flags.DEFINE_integer("encoder2_depth", 2, "Number of layers in encoder2.")

flags.DEFINE_integer("vocab_size", 0, "Size of the vocabulary.")
flags.DEFINE_boolean("binary_labels", False, "Use binary labels?")
flags.DEFINE_boolean("use_raw_bytes", False, "Use Raw bytes for LangID?")
# flags.DEFINE_integer("num_epoch", 50, "Number of training epochs.")
# flags.DEFINE_integer("train_batch_size", 256, "Size of the training batches.")
flags.DEFINE_integer("test_batch_size", 64, "Size of the testing batches.")
flags.DEFINE_boolean("use_f1", False, "Should look for 2-class f1")
flags.DEFINE_boolean("sort", True, "If examples should be sorted by length.")
flags.DEFINE_boolean("force_preproc", False, "Whether to force preprocessing.")
flags.DEFINE_integer('num_intra_threads', 0,
                     """Number of threads to use for intra-op
                     parallelism. If set to 0, the system will pick
                     an appropriate number.""")
flags.DEFINE_integer('num_inter_threads', 0,
                     """Number of threads to use for inter-op
                     parallelism. If set to 0, the system will pick
                     an appropriate number.""")
flags.DEFINE_integer('gpu', 0, "Whether to use gpu and log devices")
flags.DEFINE_boolean('force_gpu_compatible', True,
                     """whether to enable force_gpu_compatible in
                     GPU_Options""")
flags.DEFINE_string("optimizer", "adam", "Optimizer type.")
flags.DEFINE_float("lr", 1e-5, "Starting learning rate.")
flags.DEFINE_float("min_lr", 0.0001, "Ending learning rate.")
flags.DEFINE_boolean("check_numerics", False, "Check numerics.")
flags.DEFINE_boolean("count_params", False,
                     "Count the total number of parameters and don't run")
flags.DEFINE_integer("num_labeled", -1, "Number of labeled examples")
flags.DEFINE_boolean("verbose", False, "Print out a lot of crap?")
flags.DEFINE_boolean("test", False,
                     "should we use actual test data (otherwise validation)")
# flags.DEFINE_boolean("load_test", True, "try to load and then fail")

FLAGS = flags.FLAGS


def get_dataset(data_path):
  dataset = TempHumanizrNames(data_path)

  vocab_size = len(dataset.vocab)
  num_labels = len(dataset.labels)
  # print("vocab_size: {}; num_labels: {}".format(vocab_size, num_labels))
  # try:
  #   lengths = dataset.lengths
  #   print("lengths: mean = {:.1f}, median = {}, true max = {} truncated at {}".format(
  #       np.mean(lengths), np.median(lengths), max(lengths), dataset.MAX_LENGTH))
  # except:
  #   pass
  return dataset, vocab_size, num_labels


def get_embedding_builder(vocab_size):
  if FLAGS.embed_dim <= 0:
    def embedding_builder(inputs):
      return tf.one_hot(inputs, vocab_size)
  else:
    if FLAGS.embedding_l2 > 0:
      embed_reg = tf.contrib.layers.l2_regularizer(scale=FLAGS.embedding_l2)
    else:
      embed_reg = None

    def embedding_builder(inputs):
      return tf.contrib.layers.embed_sequence(
          inputs, vocab_size, FLAGS.embed_dim,
          regularizer=embed_reg)

  return embedding_builder


def get_collapser():
  if FLAGS.collapser == "sum":
    def collapser(tensors):
      return tf.reduce_sum(tensors, axis=1)
  elif FLAGS.collapser == 'max':
    def collapser(tensors):
      return tf.reduce_max(tensors, axis=1)
  elif FLAGS.collapser == 'avg':
    def collapser(tensors):
      return tf.reduce_mean(tensors, axis=1)
  elif FLAGS.collapser == 'flatten':
    def collapser(tensors):
      return tf.contrib.layers.flatten(tensors)
  elif FLAGS.collapser == 'Bahdanau':
    def collapser(tensors, lengths=None):
      attn = Bahdanau(FLAGS.hidden_dim, tensors, lengths)

      alignment = tf.zeros_like(tf.slice(
          tensors, [0, 0, 0], [-1, -1, 0]))

      for encoding in tf.unstack(tensors, axis=1):
        alignment = attn(encoding, alignment)

      alignment = tf.expand_dims(alignment, [2])
      weighted_sum = tf.reduce_sum(tensors * alignment, [1])
      return weighted_sum
  elif FLAGS.collapser == 'None':
    def collapser(tensors):
      return tensors
  else:
    raise ValueError("Unknown collapser: {}".format(FLAGS.collapser))

  return collapser


def get_model_builder(embedding_builder, encoder1, collapser, encoder2):
  def model_builder(tokens, meta, is_training=False, lengths=None):
    embedded = embedding_builder(tokens)
    if 'RNN' in FLAGS.encoder1:
      encoded = encoder1(embedded, is_training=is_training,
                         lengths=lengths)
    elif FLAGS.encoder1 in ['WaveNet', 'ByteNet']:
      embedded = tf.layers.dense(embedded, FLAGS.hidden_dim)
      encoded = encoder1(embedded, is_training=is_training)
    else:
      encoded = encoder1(embedded, is_training=is_training)

    collapsed = collapser(encoded)
    collapsed = tf.concat([collapsed, meta], axis=1)
    logits = encoder2(collapsed, is_training=is_training)

    return logits

  return tf.make_template("model", model_builder)


Data = namedtuple('Data', 'data words meta lengths ngrams ids')


def get_data(path, features, batch_size, **kwargs):
  num_epochs = kwargs.get('num_epochs', 1)
  data = InputDataset(path, features, batch_size, num_epochs=num_epochs)
  words = data.batch['words']
  meta = data.batch['meta']
  lengths = data.batch['length']
  ids = data.batch['id']
  # labels = data.batch.get('label', None)
  if kwargs.get('ngrams'):
    ngrams = data.batch['ngram']
  else:
    ngrams = None
  if 'max_length' in kwargs:
    words.set_shape([None, kwargs['max_length']])
    if ngrams is not None:
      ngrams.set_shape([None, kwargs['max_length']])

  return Data(data, words, meta, lengths, ngrams, ids)


class ExperimentWriter:
  def __init__(self, json_outfn, tensorboard_outfn, config):
    if json_outfn is None or tensorboard_outfn is None:
      raise ValueError("ExperimentWriter requires output paths")
    assert type(config) is dict, "Flags/config should be a dict"

    self.json_outfn = json_outfn
    self.tensorboard_outfn = tensorboard_outfn
    if not FLAGS.count_params:
      with open(self.json_outfn, 'a') as outf:
        config['timestamp'] = time.time()
        outf.write(json.dumps(config, cls=NumpySerializer) + "\n")
    self.tb_writer = None

  def init_tensorboard(self, sess):
    self.tb_writer = tf.summary.FileWriter(self.tensorboard_outfn, sess.graph)

  def tensorboard_write(self, name, tensor, epoch):
    add_tensorboard_summary(self.tb_writer, name, tensor, epoch)

  def tensorboard_flush(self):
    self.tb_writer.flush()

  def tensorboard_close(self):
    self.tb_writer.close()

  def json_write(self, d):
    with open(self.json_outfn, 'a') as outf:
      outf.write(json.dumps(d, cls=NumpySerializer) + '\n')


def get_data_device(gpus):
  data_device = "/device:CPU:0"
  if gpus > 0:
    from tensorflow.python.client import device_lib
    devices = device_lib.list_local_devices()
    assert(any([d.device_type == 'GPU' for d in devices]))
    data_device = "/device:GPU:0"
    logging.info("Successfully loaded GPU")
  else:
    logging.info("Did not load GPU")

  return data_device


def get_encoder_args(encoder_type, dataset, **kwargs):
  args = {
      'max_length': dataset.MAX_LENGTH,
      'hidden_dim': FLAGS.hidden_dim,
      'l1': FLAGS.encoder1_l1,
      'l2': FLAGS.encoder1_l2,
      'dropout': FLAGS.encoder1_dropout,
      'depth': FLAGS.encoder1_depth,
  }
  args.update(kwargs)

  if encoder_type in ['CNNEncoder', 'ByteNet', 'WaveNet', 'NickCNN', 'AllConv']:
    args['filter_width'] = FLAGS.cnn_filter_width
    args['cnn_activation'] = FLAGS.cnn_activation
    if encoder_type == 'NickCNN':
      args['max_filter_width'] = FLAGS.max_cnn_filter_width
    if encoder_type == 'ByteNet':
      args['bytenet_num_dilation_layers'] = FLAGS.bytenet_num_dilation_layers
    if encoder_type == 'CNNEncoder':

      cnn_preact = FLAGS.cnn_pre_activation
      if cnn_preact == 'relu':
        args['cnn_pre_activation'] = tf.nn.relu
      elif cnn_preact == 'elu':
        args['cnn_pre_activation'] = tf.nn.elu
      args['layer_norm'] = FLAGS.cnn_layer_norm

  if 'RNN' in encoder_type:
    args['rnn_cell_type'] = FLAGS.rnn_cell_type

  return args


def main():

  # Initialize
  random.seed(FLAGS.seed)
  np.random.seed(FLAGS.seed)
  logging.set_verbosity(tf.logging.INFO)
  data_device = get_data_device(FLAGS.gpu)

  # Prepare the dataset and model from flags
  dataset, vocab_size, num_labels = get_dataset(FLAGS.input_path)

  embedding_builder = get_embedding_builder(vocab_size)

  encoder1_args = get_encoder_args(
      FLAGS.encoder1,
      dataset,
  )
  encoder1 = get_encoder_template(
      FLAGS.encoder1, 'encoder1',
      **encoder1_args
  )

  collapser = get_collapser()

  encoder2_args = get_encoder_args(
      FLAGS.encoder2,
      dataset,
      output_dim=num_labels,
  )
  encoder2 = get_encoder_template(
      FLAGS.encoder2,
      'encoder2',
      **encoder2_args
  )

  model_builder = get_model_builder(
      embedding_builder, encoder1, collapser, encoder2)

  # Feature extraction
  logging.info('Feature extraction...')

  if hasattr(dataset, 'suffix'):
    dataset_suffix = dataset.suffix
  else:
    dataset_suffix = ''
  test_path = infer_feature_extraction(
      dataset, sort=FLAGS.sort,
      suffix=dataset_suffix)

  FEATURES = {
      'length': tf.FixedLenFeature([], tf.int64),
      'words': tf.VarLenFeature(tf.int64),
      # 'label': tf.FixedLenFeature([], tf.int64),
      'id': tf.FixedLenFeature([], tf.int64),
      'meta': tf.FixedLenFeature([12], tf.float32),
  }

  logging.info("Creating computation graph...")
  with tf.Graph().as_default(), tf.device(data_device):
    tf.set_random_seed(FLAGS.seed)

    test = get_data(test_path, FEATURES, FLAGS.test_batch_size,
                    max_length=dataset.MAX_LENGTH)
    test_logits = model_builder(test.words, test.meta, is_training=False,
                                lengths=test.lengths)
    test_fetches = {
        "logits": test_logits,
        "ids": test.ids,
        "words": test.words,
    }

    if FLAGS.check_numerics:
      logging.info("Checking numerics...")
      tf.add_check_numerics_ops()

    if FLAGS.count_params:
      total_params = 0
      for tvar in tf.trainable_variables():
        shape = tvar.get_shape().as_list()
        total_params += np.prod(shape)
      logging.info("Total number of params: {}".format(total_params))
      return

    # Run the model
    saver = tf.train.Saver()
    with tf.train.SingularMonitoredSession(config=get_proto_config()) as sess:
      # TODO point
      saver.restore(sess.raw_session(), "demographer/models/indorg_neural/full-0")
      test_v = run_epoch(sess, test_fetches.copy(),
                         init_ops=[test.data.init_op])

      logits = test_v['logits']
      ids = test_v['ids']
      # words = test_v['words']

      output_file = FLAGS.input_path[:-4] + 'labeled.json'
      with open(output_file, "w") as outf:
        for i in range(logits.shape[0]):
          label_i = np.argmax(logits[i])
          label_conf = logits[i][label_i] / np.sum(logits[i])
          out_obj = {
              "id": int(ids[i]),
              "label": dataset.labels.val(str(label_i)),
              "conf": label_conf,
          }
          outf.write("{}\n".format(json.dumps(out_obj, cls=NumpySerializer)))


def get_f1(fetches):
  for key in ['pos_tp', 'pos_fn', 'neg_tp', 'neg_fn', 'pos_fp', 'neg_fp']:
    if key not in fetches:
      return 0.0

  pos_f1 = calculate_f1(fetches['pos_tp'], fetches['pos_fp'],
                        fetches['pos_fn'])
  neg_f1 = calculate_f1(fetches['neg_tp'], fetches['neg_fp'],
                        fetches['neg_fn'])
  f1 = (pos_f1 + neg_f1) / 2
  return f1


def calculate_early_stop_epoch(dev_accuracies):
  '''
  We pick the early stop by finding the trio of epochs the highest mean dev acc
  we evaluate on the middle such epoch, avoiding one-off spikes
  '''
  best_epoch = 1
  best_min_acc = -1
  for i in range(1, len(dev_accuracies) - 1):
    min_acc = min(dev_accuracies[i - 1: i + 2])
    if min_acc > best_min_acc:
      best_min_acc = min_acc
      best_epoch = i
  return best_epoch


def get_proto_config():
  config = tf.ConfigProto()
  config.allow_soft_placement = True
  # if FLAGS.gpu > 0:
  #   config.log_device_placement = True
  config.intra_op_parallelism_threads = FLAGS.num_intra_threads
  config.inter_op_parallelism_threads = FLAGS.num_inter_threads
  config.gpu_options.force_gpu_compatible = FLAGS.force_gpu_compatible
  return config


if __name__ == "__main__":
  main()
