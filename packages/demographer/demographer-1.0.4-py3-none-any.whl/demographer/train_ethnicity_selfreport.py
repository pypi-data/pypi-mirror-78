from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os
import random
import time
from six.moves import xrange
from collections import namedtuple

import sklearn
import numpy as np
import tensorflow as tf

from demographer.tflm import InputDataset
from demographer.tflm import SymbolTable

from demographer.rebalance import rebalance_classifier, stacked_threshold_classifier
from demographer.rebalance import DANIEL_DATA_PROBS, BALANCED_PROBS
from demographer.encoders_selfreport import get_encoder_template

from demographer.experiment_runner_selfreport import run_epoch
from demographer.experiment_runner_selfreport import get_metrics
from demographer.experiment_runner_selfreport import get_class_acc
from demographer.experiment_runner_selfreport import feature_extraction
from demographer.experiment_runner_selfreport import add_tensorboard_summary
from demographer.experiment_runner_selfreport import get_f1
from demographer.experiment_runner_selfreport import get_class_f1_stats

from demographer.utils import NumpySerializer

from demographer.combo_dataset import ComboDataset
from demographer.baseline_dataset import Baseline


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

flags = tf.flags
logging = tf.logging

flags.DEFINE_string("name", 'test_ethnicity_selfreport', "name for the job")
flags.DEFINE_string("json_output", None, "Json output path")  # noqa
flags.DEFINE_string("tensorboard_output", None, "Tensorboard output path")  # noqa
flags.DEFINE_string("model_output", None, "Model output path")  # noqa
flags.DEFINE_string("load_model", None, "file to load model from")
flags.DEFINE_string("eval_output", None, "where to write inferred labels to file")

flags.DEFINE_string("dataset", "Combo__balanced.7756", "Dataset class")
flags.DEFINE_string("noisy_type", "exact_group", "Dataset class")
flags.DEFINE_string("feature_type", "profile", "one of: profile,unigrams,both,neither")
flags.DEFINE_string("loss_type", "ce", "ce or mae")

flags.DEFINE_string("encoder1", "CNNEncoder", "Encoding each time step")
flags.DEFINE_string("collapser", 'max', 'Collapse across time to fixed size')
flags.DEFINE_string("encoder2", "MLPEncoder", "Further encode fixed size")

flags.DEFINE_integer("seed", 42, "RNG seed")
flags.DEFINE_integer("embed_dim", 256, "Document embedding dimension.")
flags.DEFINE_integer("hidden_dim", 256, "Number of nodes in [CR]?NN layer.")

flags.DEFINE_string("rnn_cell_type", 'lstm', "Type of RNN cell.")
flags.DEFINE_integer("cnn_filter_width", 3, "Width of CNN filter")
flags.DEFINE_integer("max_cnn_filter_width", 5, "Width of CNN filter")
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
flags.DEFINE_boolean("encoder2_bias", True, "Use bias in encoder2?")

flags.DEFINE_integer("vocab_size", 0, "Size of the vocabulary.")
flags.DEFINE_boolean("binary_labels", False, "Use binary labels?")
flags.DEFINE_integer("num_epoch", 250, "Number of training epochs.")
flags.DEFINE_integer("num_batches", -1, "If > -1, number of batches per train epoch")
flags.DEFINE_integer("train_batch_size", 256, "Size of the training batches.")
flags.DEFINE_integer("test_batch_size", 64, "Size of the testing batches.")
flags.DEFINE_boolean("use_f1", True, "Should look for 2-class f1")
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
flags.DEFINE_boolean('force_gpu_compatible', False,
                     """whether to enable force_gpu_compatible in
                     GPU_Options""")
flags.DEFINE_string("optimizer", "sgd", "Optimizer type.")
flags.DEFINE_float("lr", 0.1, "Starting learning rate.")
flags.DEFINE_float("min_lr", 0.0001, "Ending learning rate.")
flags.DEFINE_boolean("check_numerics", False, "Check numerics.")
flags.DEFINE_boolean("count_params", False,
                     "Count the total number of parameters and don't run")
flags.DEFINE_integer("num_labeled", -1, "Number of labeled examples")
flags.DEFINE_boolean("verbose", False, "Print out a lot of crap?")
flags.DEFINE_boolean("test", False, "should we use actual test data (otherwise validation)")
flags.DEFINE_boolean("rebalance", False, "rebalance to known test label probs")
flags.DEFINE_boolean("balance_dev", False, "use balanced dev set")
flags.DEFINE_boolean("balance_test", False, "use balanced test set")

FLAGS = flags.FLAGS


def get_dataset(num_labeled):
  if FLAGS.dataset == 'Baseline':
    dataset = Baseline(setup=FLAGS.feature_type)
  elif FLAGS.dataset.startswith('Combo__'):
    datasets = FLAGS.dataset[7:].split("__")
    confidences = [1.0 for _ in datasets]
    feature_type = FLAGS.feature_type
    dataset = ComboDataset(datasets, confidences, setup=feature_type,)
  else:
    raise ValueError("Unknown dataset: {}".format(FLAGS.dataset))

  train_dataset = dataset

  dev_dataset = Baseline(setup=FLAGS.feature_type,
                         balance_dev=FLAGS.balance_dev,
                         balance_test=FLAGS.balance_test,)

  checks = {'vocab': SymbolTable.to_json, 'labels': SymbolTable.to_json, 'MAX_LENGTH': int}
  for attr, func in checks.items():
    assert func(getattr(train_dataset, attr)) == func(getattr(dev_dataset, attr)), attr
  vocab_size = len(train_dataset.vocab)
  num_labels = len(train_dataset.labels)
  print("vocab_size: {}; num_labels: {}".format(vocab_size, num_labels))
  try:
    lengths = train_dataset.lengths
    print("lengths: mean = {:.1f}, median = {}, true max = {} truncated at {}".format(
        np.mean(lengths), np.median(lengths), max(lengths), train_dataset.MAX_LENGTH))
  except Exception:
    pass
  return train_dataset, dev_dataset, vocab_size, num_labels


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
  elif FLAGS.collapser == 'None':
    def collapser(tensors):
      return tensors
  else:
    raise ValueError("Unknown collapser: {}".format(FLAGS.collapser))

  return collapser


def get_model_builder(embedding_builder, encoder1,
                      collapser, encoder2, unigram_vocab_size):
  def model_builder(tokens=None, meta=None, is_training=False,
                    lengths=None, unigrams=None):

    assert (tokens is not None and meta is not None) or (unigrams is not None)
    collapsed1 = None
    if tokens is not None and meta is not None:
      embedded = embedding_builder(tokens)
      if 'RNN' in FLAGS.encoder1:
        encoded = encoder1(embedded, is_training=is_training,
                           lengths=lengths)
      elif FLAGS.encoder1 in ['WaveNet', 'ByteNet']:
        embedded = tf.layers.dense(embedded, FLAGS.hidden_dim)
        encoded = encoder1(embedded, is_training=is_training)
      else:
        encoded = encoder1(embedded, is_training=is_training)

      collapsed1 = collapser(encoded)
      collapsed1 = tf.concat([collapsed1, meta], axis=1)
    elif meta is not None:
      collapsed1 = meta

    collapsed2 = None
    if unigrams is not None:
      # hacky fix
      unigram_vocab_size = 8000
      unigrams = tf.clip_by_value(unigrams, 0, unigram_vocab_size)
      indices = tf.one_hot(unigrams, unigram_vocab_size)
      collapsed2 = tf.reduce_sum(indices, axis=1)

    if unigrams is None:
      collapsed = collapsed1
    elif tokens is None:
      collapsed = collapsed2
    else:
      collapsed = tf.concat([collapsed1, collapsed2], axis=1)

    logits = encoder2(collapsed, is_training=is_training)

    return logits

  return tf.make_template("model", model_builder)


Data = namedtuple('Data',
                  'data words meta labels lengths unigrams weights userids')


def get_data(path, features, batch_size, **kwargs):
  num_epochs = kwargs.get('num_epochs', 1)
  data = InputDataset(path, features, batch_size, num_epochs=num_epochs)
  words = data.batch.get('words', None)
  meta = data.batch.get('meta', None)
  lengths = data.batch.get('length', None)
  labels = data.batch.get('label', None)
  userids = data.batch.get('userid', None)
  if FLAGS.binary_labels:
    labels = tf.clip_by_value(labels, 0, 1)
  weights = data.batch.get('weight', 1.0)
  unigrams = data.batch.get('unigrams')
  if 'max_length' in kwargs and words is not None:
    words.set_shape([None, kwargs['max_length']])

  return Data(data, words, meta, labels, lengths, unigrams, weights, userids)


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
    assert(any(["GPU" in d.device_type for d in devices]))
    data_device = "/device:GPU:0"
    logging.info("Successfully loaded GPU")
  else:
    logging.info("Did not load GPU")

  return data_device


def get_encoder_args(encoder_type, max_length, **kwargs):
  args = {
      'max_length': max_length,
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
  writer = ExperimentWriter(
      FLAGS.json_output, FLAGS.tensorboard_output, FLAGS.__flags)
  data_device = get_data_device(FLAGS.gpu)

  # Prepare the dataset and model from flags
  train_dataset, dev_dataset, vocab_size, num_labels = get_dataset(FLAGS.num_labeled)

  if train_dataset is None:
    max_length = dev_dataset.MAX_LENGTH
    unigram_vocab_size = dev_dataset.UNIGRAM_VOCAB
  else:
    max_length = train_dataset.MAX_LENGTH
    unigram_vocab_size = train_dataset.UNIGRAM_VOCAB

  embedding_builder = get_embedding_builder(vocab_size)

  encoder1_args = get_encoder_args(
      FLAGS.encoder1,
      max_length,
  )
  encoder1 = get_encoder_template(
      FLAGS.encoder1, 'encoder1',
      **encoder1_args
  )

  collapser = get_collapser()

  print("encoder2 bias is: {}".format(FLAGS.encoder2_bias))
  encoder2_args = get_encoder_args(
      FLAGS.encoder2,
      max_length,
      output_dim=num_labels,
      depth=FLAGS.encoder2_depth,
      # use_bias=FLAGS.encoder2_bias,
  )
  encoder2 = get_encoder_template(
      FLAGS.encoder2,
      'encoder2',
      **encoder2_args
  )

  model_builder = get_model_builder(
      embedding_builder, encoder1, collapser, encoder2,
      unigram_vocab_size)

  # Feature extraction
  logging.info('Feature extraction...')

  if train_dataset is not None:
    if hasattr(train_dataset, 'suffix'):
      dataset_suffix = train_dataset.suffix
    else:
      dataset_suffix = ''
    train_paths = feature_extraction(
        train_dataset,
        sort=FLAGS.sort,
        force_preproc=FLAGS.force_preproc,
        suffix=dataset_suffix,
        train=True, dev=False, test=False)
    train_path = train_paths['train']

  if hasattr(dev_dataset, 'suffix'):
    dataset_suffix = dev_dataset.suffix
  else:
    dataset_suffix = ''
  dev_paths = feature_extraction(
      dev_dataset,
      sort=FLAGS.sort,
      force_preproc=FLAGS.force_preproc,
      suffix=dataset_suffix,
      train=False, dev=True, test=FLAGS.test)
  dev_path = dev_paths['dev']
  if FLAGS.test:
    test_path = dev_paths['test']

  FEATURES = {'label': tf.FixedLenFeature([], tf.int64)}
  if FLAGS.feature_type in ['both', 'profile']:
    FEATURES['length'] = tf.FixedLenFeature([], tf.int64)
    FEATURES['words'] = tf.VarLenFeature(tf.int64)
    FEATURES['meta'] = tf.FixedLenFeature([8], tf.float32)
    FEATURES['userid'] = tf.FixedLenFeature([], tf.string)
  # if FLAGS.feature_type == 'neither':
  #   FEATURES['meta'] = tf.FixedLenFeature([8], tf.float32)
  if FLAGS.feature_type in ['both', 'unigrams']:
    FEATURES['unigrams'] = tf.VarLenFeature(tf.int64)

  logging.info("Creating computation graph...")
  with tf.Graph().as_default(), tf.device(data_device):
    tf.set_random_seed(FLAGS.seed)

    # Train model
    if train_dataset is not None:
      train = get_data(train_path, FEATURES, FLAGS.train_batch_size,
                       max_length=train_dataset.MAX_LENGTH)

      train_logits = model_builder(tokens=train.words, meta=train.meta,
                                   is_training=True,
                                   lengths=train.lengths, unigrams=train.unigrams)

      metrics = get_metrics(train_logits, train.labels, weights=train.weights,
                            loss_type=FLAGS.loss_type)
      loss, num_correct, num_total = metrics

      reg_vars = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
      reg_loss = tf.reduce_sum(reg_vars)

      opt = tf.train.GradientDescentOptimizer(FLAGS.lr)
      train_op = opt.minimize(loss + reg_loss)

      train_fetches = {"loss": loss,
                       "reg_loss": reg_loss,
                       "num_correct": num_correct,
                       "num_total": num_total,
                       }
      for label, label_idx in train_dataset.labels._v2i.items():
        stats = get_class_acc(train_logits, train.labels, label_idx)
        train_fetches["num_total_{}".format(label)] = stats['num_total']
        train_fetches["num_correct_{}".format(label)] = stats['num_correct']
    # end if train_dataset is not None

    dev = get_data(dev_path, FEATURES, FLAGS.test_batch_size,
                   max_length=max_length)
    dev_logits = model_builder(tokens=dev.words, meta=dev.meta,
                               is_training=False,
                               lengths=dev.lengths, unigrams=dev.unigrams)
    metrics = get_metrics(dev_logits, dev.labels)
    _, dev_num_correct, dev_num_total = metrics
    dev_fetches = {"num_correct": dev_num_correct,
                   "num_total": dev_num_total,
                   }
    if FLAGS.load_model:
      dev_fetches["userids"] = dev.userids

    if FLAGS.rebalance or FLAGS.load_model:
      dev_fetches["logits"] = dev_logits
      dev_fetches["labels"] = dev.labels

    for label, label_idx in dev_dataset.labels._v2i.items():
      stats = get_class_acc(dev_logits, dev.labels, label_idx)
      dev_fetches["num_total_{}".format(label)] = stats['num_total']
      dev_fetches["num_correct_{}".format(label)] = stats['num_correct']

    eval_words = tf.placeholder(
        shape=dev.words.shape, dtype=tf.int32, name='tokens')
    eval_meta = tf.placeholder(
        shape=dev.meta.shape, dtype=tf.float32, name='meta')
    eval_logits = model_builder(eval_words, eval_meta, is_training=False)
    eval_logits = tf.identity(eval_logits, name='logits')

    if FLAGS.test:
      test = get_data(test_path, FEATURES, FLAGS.test_batch_size,
                      max_length=max_length)
      test_logits = model_builder(tokens=test.words, meta=test.meta,
                                  is_training=False,
                                  lengths=test.lengths, unigrams=test.unigrams)
      metrics = get_metrics(test_logits, test.labels)
      _, test_num_correct, test_num_total = metrics
      test_classifications = tf.equal(tf.argmax(test_logits, axis=1), test.labels)
      test_fetches = {"num_correct": test_num_correct,
                      "num_total": test_num_total,
                      "classifications": test_classifications,
                      "userids": test.userids,
                      }

      for label, label_idx in dev_dataset.labels._v2i.items():
        stats = get_class_acc(test_logits, test.labels, label_idx)
        test_fetches["num_total_{}".format(label)] = stats['num_total']
        test_fetches["num_correct_{}".format(label)] = stats['num_correct']

      if FLAGS.rebalance:
        test_fetches["logits"] = test_logits
        test_fetches["labels"] = test.labels

    if FLAGS.use_f1:
      for label, label_index in dev_dataset.labels._v2i.items():
        stats = get_class_f1_stats(dev_logits, dev.labels, label_index)
        for key, val in stats.items():
          dev_fetches["{}_{}".format(label, key)] = val

        if FLAGS.test:
          stats = get_class_f1_stats(test_logits, test.labels, label_index)
          for key, val in stats.items():
            test_fetches["{}_{}".format(label, key)] = val

    if FLAGS.check_numerics:
      logging.info("Checking numerics...")
      tf.add_check_numerics_ops()

    # if FLAGS.count_params:
    total_params = 0
    for tvar in tf.trainable_variables():
      shape = tvar.get_shape().as_list()
      total_params += np.prod(shape)
      # print(tvar.name, shape)
    logging.info("Total number of params: {}".format(total_params))

    logging.info("Graph complete. Training...")
    # Run the model
    dev_accuracies = []
    dev_f1s = []
    test_accuracies = []
    test_f1s = []
    test_mcnemars = []
    saver = tf.train.Saver(max_to_keep=FLAGS.num_epoch,)
    with tf.train.SingularMonitoredSession(config=get_proto_config()) as sess:
      if FLAGS.load_model is not None:
        saver.restore(sess.raw_session(), FLAGS.load_model)
        dev_v = run_epoch(sess, dev_fetches.copy(),
                          init_ops=[dev.data.init_op])
        userids = [userid.decode() for userid in dev_v['userids']]
        logits = dev_v['logits']

        with open(FLAGS.eval_output, "w") as outf:
          outf.write("{}\n".format(json.dumps(dev_dataset.labels._i2v)))
          for userid, logits in zip(userids, logits):
            outf.write("{}\n".format(json.dumps(
                {'userid': userid, 'logits': logits})))
        return

      writer.init_tensorboard(sess)

      epoch_start = time.time()
      for epoch in xrange(FLAGS.num_epoch):
        train_v = run_epoch(sess, train_fetches.copy(),
                            train_ops=[train_op],
                            init_ops=[train.data.init_op],
                            num_batches=FLAGS.num_batches)
        dev_v = run_epoch(sess, dev_fetches.copy(),
                          init_ops=[dev.data.init_op])
        if FLAGS.test:
          test_v = run_epoch(sess, test_fetches.copy(),
                             init_ops=[test.data.init_op])
          test_f1 = get_f1(test_v, dev_dataset.labels._v2i.keys())
          test_accuracy = np.sum(test_v['num_correct']) \
              / np.sum(test_v['num_total'])
          userids = [userid.decode() for userid in test_v['userids']]
          test_mcnemar = dict(zip(userids, test_v['classifications']))

        train_loss = np.sum(train_v['loss'])
        train_f1 = get_f1(train_v, train_dataset.labels._v2i.keys())
        dev_f1 = get_f1(dev_v, train_dataset.labels._v2i.keys())

        train_accuracy = np.sum(train_v['num_correct']) \
            / max(1, np.sum(train_v['num_total']))
        dev_accuracy = np.sum(dev_v['num_correct']) \
            / max(1, np.sum(dev_v['num_total']))

        if FLAGS.rebalance:
          dev_logits_out = np.array(dev_v['logits'])
          dev_labels = np.array(dev_v['labels'])
          stacked_thresholds = rebalance_classifier(dev_logits_out, dev_labels)
          prediction = stacked_threshold_classifier(dev_logits_out, stacked_thresholds)
          # NOTE I have actually carefully tested that my hand-written F1 matches sklearn
          dev_accuracy = sklearn.metrics.accuracy_score(dev_labels, prediction)
          dev_f1 = sklearn.metrics.f1_score(dev_labels, prediction, average='macro')

          if FLAGS.test:
            if FLAGS.balance_test:
              class_probs = BALANCED_PROBS
            else:
              class_probs = DANIEL_DATA_PROBS
            test_thresholds = rebalance_classifier(
                dev_logits_out, dev_labels, class_probs=class_probs)
            test_logits_out = np.array(test_v['logits'])
            test_labels = np.array(test_v['labels'])
            prediction = stacked_threshold_classifier(test_logits_out, test_thresholds)
            test_accuracy = sklearn.metrics.accuracy_score(test_labels, prediction)
            test_f1 = sklearn.metrics.f1_score(test_labels, prediction, average='macro')
            userids = [userid.decode() for userid in test_v['userids']]
            test_mcnemar = dict(zip(userids, (prediction == test_labels).tolist()))

        runtime = time.time() - epoch_start
        epoch_start = time.time()

        if FLAGS.verbose:
          logging.info("Epoch %d...", epoch)
          logging.info("train loss: {:.3f}".format(train_loss))
          logging.info("train examples: {}".format(np.sum(train_v['num_total'])))
          logging.info("train accuracy: {:.3f}".format(train_accuracy))
          logging.info("dev examples: {}".format(np.sum(dev_v['num_total'])))
          logging.info("dev accuracy: {:.3f}".format(dev_accuracy))
        else:
          log_max_epoch = int(np.ceil(np.log10(FLAGS.num_epoch)))
          line = "{:{width}} loss={:7.1f} train_acc={:5.2f}% dev_acc={:5.2f}% in {:4.1f}s".format(
              epoch, train_loss, train_accuracy * 100, dev_accuracy * 100, runtime,
              width=log_max_epoch)
          logging.info(line)

        class_spec = []
        train_total = np.sum(train_v['num_total'])
        for label, label_idx in train_dataset.labels._v2i.items():
          if FLAGS.binary_labels and label_idx > 1:
            continue
          acc = np.sum(train_v["num_correct_{}".format(label)]) \
              / max(1, np.sum(train_v["num_total_{}".format(label)]))
          total = np.sum(train_v["num_total_{}".format(label)])
          class_spec.append("{}={:.1f}% ({:.1f})".format(
              label[0], 100 * acc, 100 * total / train_total))
        logging.info(" Train> " + ", ".join(class_spec))

        class_spec = []
        dev_total = np.sum(dev_v['num_total'])
        for label, label_idx in train_dataset.labels._v2i.items():
          if FLAGS.binary_labels and label_idx > 1:
            continue
          acc = np.sum(dev_v["num_correct_{}".format(label)]) \
              / max(1, np.sum(dev_v["num_total_{}".format(label)]))
          total = np.sum(dev_v["num_total_{}".format(label)])
          class_spec.append("{}={:.1f}% ({:.1f})".format(
              label[0], 100 * acc, 100 * total / dev_total))
        logging.info(" Dev > " + ", ".join(class_spec))

        # writer.tensorboard_write('loss', train_loss, epoch)
        # writer.tensorboard_write('train_accuracy', train_accuracy, epoch)
        # writer.tensorboard_write('dev_accuracy', dev_accuracy, epoch)
        # writer.tensorboard_write('test_accuracy', test_accuracy, epoch)

        epoch_log = {'timestamp': time.time(),
                     'epoch': epoch,
                     'train_f1': train_f1,
                     'train_accuracy': train_accuracy,
                     'dev_f1': dev_f1,
                     'dev_accuracy': dev_accuracy,
                     }

        dev_accuracies.append(dev_accuracy)
        if FLAGS.test:
          test_accuracies.append(test_accuracy)
          test_mcnemars.append(test_mcnemar)
          epoch_log['test_accuracy'] = test_accuracy
          # epoch_log['test_mcnemar'] = test_mcnemar
          if FLAGS.use_f1:
            test_f1s.append(test_f1)
            epoch_log['test_f1'] = test_f1

        if FLAGS.use_f1:
          dev_f1s.append(dev_f1)
          if FLAGS.verbose:
            logging.info("train f1: {:.3f}".format(train_f1))
            logging.info("dev f1: {:.3f}".format(dev_f1))

        writer.json_write(epoch_log)
        # writer.tensorboard_flush()

        if FLAGS.load_model is None:
          # save model on 10% of epochs
          if FLAGS.num_epoch > 10 and (epoch + 1) % (FLAGS.num_epoch // 10) == 0:
            saver.save(sess.raw_session(),
                       FLAGS.model_output,
                       latest_filename=FLAGS.name + ".ckpt",
                       global_step=epoch)

    final_log = {'timestamp': time.time(),
                 'dev_accuracies': dev_accuracies,
                 }

    stop_epoch = calculate_early_stop_epoch(dev_accuracies)

    stopped_dev_accuracy = dev_accuracies[stop_epoch]
    final_log['stopped_dev_accuracy'] = stopped_dev_accuracy
    logging.info("Final dev accuracy: {:.3f}".format(stopped_dev_accuracy))
    if FLAGS.use_f1:
      stopped_dev_f1 = dev_f1s[stop_epoch]
      logging.info("Final dev f1: {:.3f}".format(stopped_dev_f1))
      final_log['stopped_dev_f1'] = stopped_dev_f1
      final_log['dev_f1s'] = dev_f1s

    if FLAGS.test:
      stopped_test_accuracy = test_accuracies[stop_epoch]
      stopped_test_mcnemar = test_mcnemars[stop_epoch]
      logging.info("Final test accuracy: {:.3f}".format(stopped_test_accuracy))
      final_log['stopped_test_accuracy'] = stopped_test_accuracy
      final_log['stopped_test_mcnemar'] = stopped_test_mcnemar
      final_log['test_accuracies'] = test_accuracies

      if FLAGS.use_f1:
        stopped_test_f1 = test_f1s[stop_epoch]
        logging.info("Final test f1: {:.3f}".format(stopped_test_f1))
        final_log['stopped_test_f1'] = stopped_test_f1
        final_log['test_f1s'] = test_f1s

    writer.json_write(final_log)
    writer.tensorboard_close()


def calculate_early_stop_epoch(dev_accuracies):
  '''
  We pick the early stop by finding the trio of epochs the highest mean dev acc
  we evaluate on the middle such epoch, avoiding one-off spikes
  '''
  best_epoch = 0
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
