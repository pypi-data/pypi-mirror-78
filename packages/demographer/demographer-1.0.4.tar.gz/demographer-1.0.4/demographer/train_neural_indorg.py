from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os
import random
import time
from six.moves import xrange
from collections import namedtuple

import numpy as np
from tensorflow.contrib.seq2seq import BahdanauAttention as Bahdanau

from demographer.tflm import InputDataset
from demographer.tflm import Optimizer

from demographer.naacl_twitter import NaaclTwitter
from demographer.indorg_dataset import HumanizrNames

from demographer.utils import NumpySerializer
from demographer.encoders import get_encoder_template

from demographer.experiment_runner import run_epoch
from demographer.experiment_runner import get_metrics
from demographer.experiment_runner import get_class_f1_stats
from demographer.experiment_runner import calculate_f1
from demographer.experiment_runner import humanizr_feature_extraction
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

flags.DEFINE_string("dataset", "HumanizrNames", "Dataset class")
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
flags.DEFINE_float("encoder1_dropout", 0.2, "dropout reg for encoder1")
flags.DEFINE_float("encoder2_l1", 0., "l1 reg for encoder2")
flags.DEFINE_float("encoder2_l2", 0., "l2 reg for encoder2")
flags.DEFINE_float("encoder2_dropout", 0., "dropout reg for encoder2")
flags.DEFINE_integer("encoder1_depth", 2, "Number of layers in encoder1.")
flags.DEFINE_integer("encoder2_depth", 2, "Number of layers in encoder2.")

flags.DEFINE_integer("vocab_size", 0, "Size of the vocabulary.")
flags.DEFINE_integer("num_epoch", 200, "Number of training epochs.")
flags.DEFINE_integer("train_batch_size", 256, "Size of the training batches.")
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
flags.DEFINE_string("optimizer", "sgd", "Optimizer type.")
flags.DEFINE_float("lr", 0.5, "Starting learning rate.")
flags.DEFINE_boolean("check_numerics", False, "Check numerics.")
flags.DEFINE_boolean("count_params", False,
                     "Count the total number of parameters and don't run")
flags.DEFINE_integer("num_labeled", -1, "Number of labeled examples")
flags.DEFINE_boolean("verbose", False, "Print out a lot of crap?")
flags.DEFINE_boolean("load_test", False, "try to load and then fail")

FLAGS = flags.FLAGS


def get_dataset(num_labeled):
  if FLAGS.dataset == 'HumanizrNames':
    dataset = HumanizrNames(FLAGS.setup, FLAGS.train_balance_ratio)
  elif FLAGS.dataset == 'NaaclTwitter':
    dataset = NaaclTwitter('mf', 'n+s')
  else:
    raise ValueError("Unknown dataset: {}".format(FLAGS.dataset))

  vocab_size = len(dataset.vocab)
  num_labels = len(dataset.labels)
  print("vocab_size: {}; num_labels: {}".format(vocab_size, num_labels))
  try:
    lengths = dataset.lengths
    print("lengths: mean = {:.1f}, median = {}, true max = {} truncated at {}".format(
        np.mean(lengths), np.median(lengths), max(lengths), dataset.MAX_LENGTH))
  except Exception as e:
    logging.error("couldn't calculate dataset lengths: {}".format(e))
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


Data = namedtuple('Data', 'data words meta labels lengths ngrams')


def get_data(path, features, batch_size, **kwargs):
  num_epochs = kwargs.get('num_epochs', 1)
  data = InputDataset(path, features, batch_size, num_epochs=num_epochs)
  words = data.batch['words']
  meta = data.batch['meta']
  lengths = data.batch['length']
  labels = data.batch.get('label', None)
  if kwargs.get('ngrams'):
    ngrams = data.batch['ngram']
  else:
    ngrams = None
  if 'max_length' in kwargs:
    words.set_shape([None, kwargs['max_length']])
    if ngrams is not None:
      ngrams.set_shape([None, kwargs['max_length']])

  return Data(data, words, meta, labels, lengths, ngrams)


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
    assert(any(["GPU" in d.device_type for d in devices])), devices
    data_device = "/GPU:0"
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

  if encoder_type in ['CNNEncoder', 'ByteNet', 'WaveNet', 'AllConv']:
    args['filter_width'] = FLAGS.cnn_filter_width
    args['cnn_activation'] = FLAGS.cnn_activation
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
  writer = ExperimentWriter(
      FLAGS.json_output, FLAGS.tensorboard_output, FLAGS.__flags)
  data_device = get_data_device(FLAGS.gpu)

  # Prepare the dataset and model from flags
  dataset, vocab_size, num_labels = get_dataset(FLAGS.num_labeled)

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
  paths = humanizr_feature_extraction(
      dataset, sort=FLAGS.sort, force_preproc=FLAGS.force_preproc,
      suffix=dataset_suffix)

  train_path, dev_path, test_path = paths

  FEATURES = {
      'length': tf.FixedLenFeature([], tf.int64),
      'words': tf.VarLenFeature(tf.int64),
      'label': tf.FixedLenFeature([], tf.int64),
      'meta': tf.FixedLenFeature([12], tf.float32),
  }

  logging.info("Creating computation graph...")
  with tf.Graph().as_default(), tf.device(data_device):
    tf.set_random_seed(FLAGS.seed)

    # Train model
    train = get_data(train_path, FEATURES, FLAGS.train_batch_size,
                     max_length=dataset.MAX_LENGTH)
    train_logits = model_builder(train.words, train.meta, is_training=True,
                                 lengths=train.lengths)
    metrics = get_metrics(train_logits, train.labels)
    loss, num_correct, num_total = metrics

    reg_vars = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
    reg_loss = tf.reduce_sum(reg_vars)

    optim_hp = Optimizer.H
    optim_hp.lr = FLAGS.lr
    optim_hp.optimizer = FLAGS.optimizer
    opt = Optimizer(config=optim_hp)
    train_op = opt.optimize(loss + reg_loss)

    train_fetches = {"loss": loss,
                     "reg_loss": reg_loss,
                     "num_correct": num_correct,
                     "num_total": num_total,
                     }

    # dev = InputDataset(dev_path, FEATURES, FLAGS.test_batch_size)
    dev = get_data(dev_path, FEATURES, FLAGS.test_batch_size,
                   max_length=dataset.MAX_LENGTH)
    dev_logits = model_builder(dev.words, dev.meta, is_training=False,
                               lengths=dev.lengths)
    metrics = get_metrics(dev_logits, dev.labels)
    _, dev_num_correct, dev_num_total = metrics
    dev_fetches = {"num_correct": dev_num_correct,
                   "num_total": dev_num_total,
                   }

    # test = InputDataset(test_path, FEATURES, FLAGS.test_batch_size)
    test = get_data(test_path, FEATURES, FLAGS.test_batch_size,
                    max_length=dataset.MAX_LENGTH)
    test_logits = model_builder(test.words, test.meta, is_training=False,
                                lengths=test.lengths)
    metrics = get_metrics(test_logits, test.labels)
    _, test_num_correct, test_num_total = metrics
    test_fetches = {"num_correct": test_num_correct,
                    "num_total": test_num_total,
                    }

    words = tf.placeholder(shape=test.words.shape, dtype=tf.int32, name='tokens')
    meta = tf.placeholder(shape=test.meta.shape, dtype=tf.float32, name='meta')
    logits = model_builder(words, meta, is_training=False)
    logits = tf.identity(logits, name='logits')

    if FLAGS.use_f1:
      train_pos_f1 = get_class_f1_stats(train_logits, train.labels,
                                        dataset.labels._v2i['positive'])
      train_neg_f1 = get_class_f1_stats(train_logits, train.labels,
                                        dataset.labels._v2i['negative'])
      dev_pos_f1 = get_class_f1_stats(dev_logits, dev.labels,
                                      dataset.labels._v2i['positive'])
      dev_neg_f1 = get_class_f1_stats(dev_logits, dev.labels,
                                      dataset.labels._v2i['negative'])
      test_pos_f1 = get_class_f1_stats(test_logits, test.labels,
                                       dataset.labels._v2i['positive'])
      test_neg_f1 = get_class_f1_stats(test_logits, test.labels,
                                       dataset.labels._v2i['negative'])
      for name, d in [('pos', train_pos_f1), ('neg', train_neg_f1)]:
        for key, val in d.items():
          train_fetches["{}_{}".format(name, key)] = val
      for name, d in [('pos', dev_pos_f1), ('neg', dev_neg_f1)]:
        for key, val in d.items():
          dev_fetches["{}_{}".format(name, key)] = val
      for name, d in [('pos', test_pos_f1), ('neg', test_neg_f1)]:
        for key, val in d.items():
          test_fetches["{}_{}".format(name, key)] = val

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

    logging.info("Graph complete. Training...")
    # Run the model
    dev_accuracies = []
    dev_f1s = []
    test_accuracies = []
    test_f1s = []
    saver = tf.train.Saver(max_to_keep=FLAGS.num_epoch,)
    with tf.train.SingularMonitoredSession(config=get_proto_config()) as sess:
      if FLAGS.load_test:
        saver.restore(sess.raw_session(), "peoples_models/full-0")
        logging.warn("success!")
      writer.init_tensorboard(sess)

      for epoch in xrange(FLAGS.num_epoch):
        epoch_start = time.time()
        train_v = run_epoch(sess, train_fetches.copy(),
                            train_ops=[train_op],
                            init_ops=[train.data.init_op])
        dev_v = run_epoch(sess, dev_fetches.copy(),
                          init_ops=[dev.data.init_op])
        test_v = run_epoch(sess, test_fetches.copy(),
                           init_ops=[test.data.init_op])
        runtime = time.time() - epoch_start

        train_loss = train_v['loss']
        train_f1 = get_f1(train_v)
        dev_f1 = get_f1(test_v)
        test_f1 = get_f1(test_v)

        train_accuracy = train_v['num_correct'] / train_v['num_total']
        dev_accuracy = dev_v['num_correct'] / dev_v['num_total']
        test_accuracy = test_v['num_correct'] / test_v['num_total']

        if FLAGS.verbose:
          logging.info("Epoch %d...", epoch)
          logging.info("train loss: {:.3f}".format(train_loss))
          logging.info("train examples: {}".format(train_v['num_total']))
          logging.info("train accuracy: {:.3f}".format(train_accuracy))
          logging.info("dev examples: {}".format(dev_v['num_total']))
          logging.info("dev accuracy: {:.3f}".format(dev_accuracy))
        else:
          log_max_epoch = int(np.ceil(np.log10(FLAGS.num_epoch)))
          line = "{:{width}} loss={:7.1f} train_acc={:5.2f}% dev_acc={:5.2f}% in {:4.1f}s".format(
              epoch, train_loss, train_accuracy * 100, dev_accuracy * 100, runtime,
              width=log_max_epoch)
          logging.info(line)

        writer.tensorboard_write('loss', train_loss, epoch)
        writer.tensorboard_write('train_accuracy', train_accuracy, epoch)
        writer.tensorboard_write('dev_accuracy', dev_accuracy, epoch)
        writer.tensorboard_write('test_accuracy', test_accuracy, epoch)

        dev_accuracies.append(dev_accuracy)
        test_accuracies.append(test_accuracy)

        if FLAGS.use_f1:
          if FLAGS.verbose:
            logging.info("train f1: {:.3f}".format(train_f1))
            logging.info("dev f1: {:.3f}".format(dev_f1))
          writer.tensorboard_write('f1', train_f1, epoch)
          writer.tensorboard_write('dev_f1', dev_f1, epoch)
          writer.tensorboard_write('test_f1', test_f1, epoch)
          dev_f1s.append(dev_f1)
          test_f1s.append(test_f1)

        epoch_log = {'timestamp': time.time(), 'epoch': epoch,
                     'train_f1': train_f1,
                     'train_accuracy': train_accuracy,
                     'dev_f1': dev_f1,
                     'dev_accuracy': dev_accuracy,
                     'test_f1': test_f1,
                     'test_accuracy': test_accuracy,
                     }
        writer.json_write(epoch_log)
        writer.tensorboard_flush()

        # if not FLAGS.load_test:
        #   saver.save(sess.raw_session(),
        #              FLAGS.model_output,
        #              latest_filename=FLAGS.name + ".ckpt",
        #              global_step=epoch)
        #   time.sleep(10)

        # After every 10 epochs, save model
        if (1 + epoch) % 10 == 0 or (1 + epoch) == FLAGS.num_epoch:
          saver.save(sess.raw_session(),
                     FLAGS.model_output,
                     latest_filename=FLAGS.name + ".ckpt",
                     global_step=epoch)

    stop_epoch = calculate_early_stop_epoch(dev_accuracies)

    stopped_dev_accuracy = dev_accuracies[stop_epoch]
    logging.info("Final dev accuracy: {:.3f}".format(stopped_dev_accuracy))
    stopped_test_accuracy = test_accuracies[stop_epoch]
    logging.info("Final test accuracy: {:.3f}".format(stopped_test_accuracy))

    if FLAGS.use_f1:
      stopped_dev_f1 = dev_f1s[stop_epoch]
      logging.info("Final dev f1: {:.3f}".format(stopped_dev_f1))
      stopped_test_f1 = test_f1s[stop_epoch]
      logging.info("Final test f1: {:.3f}".format(stopped_test_f1))

    final_log = {'timestamp': time.time(),
                 'stopped_test_accuracy': stopped_test_accuracy,
                 'stopped_dev_accuracy': stopped_dev_accuracy,
                 'dev_accuracies': dev_accuracies,
                 'test_accuracies': test_accuracies,
                 }
    if FLAGS.use_f1:
      final_log['stopped_test_f1'] = stopped_test_f1
      final_log['stopped_dev_f1'] = stopped_dev_f1
      final_log['dev_f1s'] = dev_f1s
      final_log['test_f1s'] = test_f1s

    writer.json_write(final_log)
    writer.tensorboard_close()


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
  if FLAGS.gpu > 0:
    config.log_device_placement = True
  config.intra_op_parallelism_threads = FLAGS.num_intra_threads
  config.inter_op_parallelism_threads = FLAGS.num_inter_threads
  config.gpu_options.force_gpu_compatible = FLAGS.force_gpu_compatible
  return config


if __name__ == "__main__":
  main()
