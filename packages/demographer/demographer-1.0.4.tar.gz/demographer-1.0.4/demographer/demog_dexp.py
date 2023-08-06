# Copyright 2017 Johns Hopkins University. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or  implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json
import random
import time

import numpy as np
import tensorflow as tf
from tensorflow.contrib.seq2seq import BahdanauAttention as Bahdanau

from demographer.tflm import InputDataset
from demographer.tflm import Optimizer

from demographer.encoders import get_encoder_template

from demographer.naacl_twitter import NaaclTwitter

from demographer.utils import NumpySerializer

from demographer.experiment_runner import run_epoch
from demographer.experiment_runner import get_metrics
from demographer.experiment_runner import get_class_f1_stats
from demographer.experiment_runner import calculate_f1
from demographer.experiment_runner import feature_extraction
from demographer.experiment_runner import add_tensorboard_summary

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

flags = tf.flags
logging = tf.logging

flags.DEFINE_string("json_output", 'crap.txt', "Json output path")
flags.DEFINE_string("tensorboard_output", 'crap', "Tensorboard output path")
flags.DEFINE_string("model_output", 'crap', "Model output path")

flags.DEFINE_string("dataset", "NaaclTwitter", "Dataset class")
flags.DEFINE_string("task", "mf", "Task: mf, wb, or wlb")
flags.DEFINE_string("datatype", "n", "Data: n or n+s")

flags.DEFINE_string("encoder1", "CNNEncoder", "Encoding each time step")
flags.DEFINE_string("collapser", 'max', 'Collapse across time to fixed size')
flags.DEFINE_string("encoder2", "MLPEncoder", "Further encode fixed size")

flags.DEFINE_integer("seed", 42, "RNG seed")
flags.DEFINE_integer("embed_dim", 256, "Document embedding dimension.")
flags.DEFINE_integer("hidden_dim", 256, "Number of nodes in [CR]?NN layer.")
flags.DEFINE_integer("num_layer", 2, "Number of layers in [CR]?NN.")
flags.DEFINE_string("rnn_cell_type", 'gru', "Type of RNN cell.")
flags.DEFINE_integer("cnn_filter_width", 3, "Width of CNN filter")

flags.DEFINE_float("embedding_l2", 0., "l2 regularization for embedding")
flags.DEFINE_string("cnn_activation", None, "activation_fn for CNNs")
flags.DEFINE_float("encoder1_l1", 0., "l1 reg for encoder1")
flags.DEFINE_float("encoder1_l2", 0., "l2 reg for encoder1")
flags.DEFINE_float("encoder1_dropout", 0., "dropout reg for encoder1")
flags.DEFINE_float("encoder2_l1", 0., "l1 reg for encoder2")
flags.DEFINE_float("encoder2_l2", 0., "l2 reg for encoder2")
flags.DEFINE_float("encoder2_dropout", 0., "dropout reg for encoder2")
flags.DEFINE_integer("encoder1_depth", 3, "Number of layers in encoder1.")
flags.DEFINE_integer("encoder2_depth", 2, "Number of layers in encoder2.")

# flags.DEFINE_integer("latent_dim", 128, "Latent code dimension.")
# flags.DEFINE_float("kl_weight", 0.1, "Initial weight for kl term")
# flags.DEFINE_float("kl_rate", 1.1, "rate to increase KL weight")
flags.DEFINE_integer("vocab_size", 2000, "Size of the vocabulary.")
flags.DEFINE_integer("num_epoch", 50, "Number of training epochs.")
flags.DEFINE_integer("train_batch_size", 64, "Size of the training batches.")
flags.DEFINE_integer("dev_batch_size", 64, "Size of the deving batches.")
flags.DEFINE_integer("test_batch_size", 64, "Size of the testing batches.")
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
flags.DEFINE_boolean('gpu', 0, "Whether to use gpu and log devices")
flags.DEFINE_boolean('force_gpu_compatible', True,
                     """whether to enable force_gpu_compatible in
                     GPU_Options""")
flags.DEFINE_string("optimizer", "adam", "Optimizer type.")
flags.DEFINE_float("lr", 0.0001, "Starting learning rate.")
flags.DEFINE_float("min_lr", 0.0001, "Ending learning rate.")
flags.DEFINE_boolean("check_numerics", False, "Check numerics.")
flags.DEFINE_boolean('use_train', True, "Use training data?")
flags.DEFINE_boolean('use_pretrain', False, "Use pretraining data?")

FLAGS = flags.FLAGS


def get_dataset():
  if FLAGS.dataset == 'NaaclTwitter':
    dataset = NaaclTwitter(FLAGS.task, FLAGS.datatype)
  else:
    raise ValueError("Unknown dataset: {}".format(FLAGS.dataset))

  vocab_size = len(dataset.vocab)
  num_labels = len(dataset.labels)
  print("vocab_size: {}; num_labels: {}".format(vocab_size, num_labels))
  try:
    lengths = dataset.lengths
    print("lengths: mean = {:.1f}, median = {}, max = {}".format(
        np.mean(lengths), np.median(lengths), max(lengths)))
  except Exception as e:
    logging.warn("unable to calculate lengths: {}".format(e))
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

  if 'RNN' in encoder_type:
    args['rnn_cell_type'] = FLAGS.rnn_cell_type

  return args


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
  else:
    raise ValueError("Unknown collapser: {}".format(FLAGS.collapser))

  return collapser


def get_model_builder(embedding_builder, encoder1, collapser, encoder2):
  def model_builder(inputs, lengths=None, is_training=False):
    embedded = embedding_builder(inputs)
    if 'RNNEncoder' in FLAGS.encoder1:
      encoded = encoder1(embedded, is_training=is_training, lengths=lengths)
    else:
      encoded = encoder1(embedded, is_training=is_training)

    collapsed = collapser(encoded)
    logits = encoder2(collapsed, is_training=is_training)
    return logits

  return tf.make_template("model", model_builder)


def main():
  required_flags = [FLAGS.json_output, FLAGS.tensorboard_output,
                    FLAGS.model_output]
  if any(x is None for x in required_flags):
    logging.error(
        "Must set FLAGS.json_output, FLAGS.tensorboard_output, FLAGS.model_output")
    return

  with open(FLAGS.json_output, 'w') as outf:
    d = FLAGS.__flags
    d['timestamp'] = time.time()
    outf.write(json.dumps(d, cls=NumpySerializer) + "\n")

  data_device = "/device:CPU:0"
  if FLAGS.gpu > 0:
    logging.warn("Running genseq.demog_dexp with {} gpu(s)".format(FLAGS.gpu))
    from tensorflow.python.client import device_lib
    devices = device_lib.list_local_devices()
    logging.error(devices)
    assert(any([d.device_type == 'GPU' for d in devices]))
    data_device = "/device:GPU:0"
    logging.error("Successfully loaded GPU")

  # Logging verbosity.
  logging.set_verbosity(tf.logging.INFO)

  # Initialize RNG
  random.seed(FLAGS.seed)
  np.random.seed(FLAGS.seed)

  # Prepare the dataset and model from flags
  dataset, vocab_size, num_labels = get_dataset()
  with open(os.path.join(FLAGS.model_output, "vocab.json"), "w") as outf:
    outf.write(json.dumps(dataset.vocab, cls=NumpySerializer))
  with open(os.path.join(FLAGS.model_output, "labels.json"), "w") as outf:
    outf.write(json.dumps(dataset.labels, cls=NumpySerializer))

  embedding_builder = get_embedding_builder(vocab_size)

  encoder1_args = get_encoder_args(
      FLAGS.encoder1, max_length=dataset.MAX_LENGTH)
  encoder1 = get_encoder_template(
      FLAGS.encoder1, 'encoder1', **encoder1_args)

  collapser = get_collapser()

  encoder2_args = get_encoder_args(
      FLAGS.encoder2, output_dim=num_labels, max_length=dataset.MAX_LENGTH)
  encoder2 = get_encoder_template(
      FLAGS.encoder2, 'encoder2', **encoder2_args)

  model_builder = get_model_builder(
      embedding_builder, encoder1, collapser, encoder2)

  # Feature extraction
  logging.info('Feature extraction...')
  paths = feature_extraction(
      dataset, sort=FLAGS.sort,
      force_preproc=FLAGS.force_preproc,
      pretrain=FLAGS.use_pretrain,
  )

  if FLAGS.use_pretrain:
    (pretrain_path, train_path, dev_path, test_path) = paths
  else:
    (train_path, dev_path, test_path) = paths

  FEATURES = {
      'length': tf.FixedLenFeature([], tf.int64),
      'words': tf.VarLenFeature(tf.int64),
      'label': tf.FixedLenFeature([], tf.int64)
  }

  logging.info("Creating computation graph...")
  with tf.Graph().as_default(), tf.device(data_device):
    tf.set_random_seed(FLAGS.seed)

    if FLAGS.use_pretrain:
      # Pretrain model
      with tf.name_scope('Pretrain'):
        pretrain_data = InputDataset(pretrain_path, FEATURES, FLAGS.train_batch_size)
        with tf.variable_scope('Model', reuse=None):
          pretrain_words = pretrain_data.batch['words']
          pretrain_lengths = pretrain_data.batch['length']
          pretrain_labels = pretrain_data.batch['label']
          pretrain_words.set_shape([None, dataset.MAX_LENGTH])
          pretrain_logits = model_builder(
              pretrain_words, lengths=pretrain_lengths, is_training=True)

          metrics = get_metrics(pretrain_logits, pretrain_labels)
          pretrain_loss, pretrain_num_correct, pretrain_num_total = metrics

          # pretrain_f1_stats = {label_index: get_class_f1_stats(
          #                      pretrain_logits, pretrain_labels, label_index)
          #                      for label_index in dataset.labels._i2v}

          reg_vars = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
          pretrain_reg_loss = tf.reduce_sum(reg_vars)

    # Train model
    with tf.name_scope('Train'):
      train_data = InputDataset(train_path, FEATURES, FLAGS.train_batch_size)
      train_reuse = None
      if FLAGS.use_pretrain:
        train_reuse = True
      with tf.variable_scope('Model', reuse=train_reuse):
        train_words = train_data.batch['words']
        train_lengths = train_data.batch['length']
        train_labels = train_data.batch['label']
        train_words.set_shape([None, dataset.MAX_LENGTH])
        train_logits = model_builder(
            train_words, lengths=train_lengths, is_training=True)

        metrics = get_metrics(train_logits, train_labels)
        loss, num_correct, num_total = metrics

        train_f1_stats = {label_index: get_class_f1_stats(
                          train_logits, train_labels, label_index)
                          for label_index in dataset.labels._i2v}

        reg_vars = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
        reg_loss = tf.reduce_sum(reg_vars)

      with tf.variable_scope('Optimize', reuse=None):
        optim_hp = Optimizer.H
        optim_hp.lr = FLAGS.lr
        opt = Optimizer(config=optim_hp)

        total_loss = 0

        if FLAGS.use_train:
          total_loss += loss + reg_loss

        if FLAGS.use_pretrain:
          total_loss += pretrain_loss + pretrain_reg_loss

        train_op = opt.optimize(total_loss)

    train_fetches = {"loss": loss,
                     "reg_loss": reg_loss,
                     "num_correct": num_correct,
                     "num_total": num_total,
                     }

    # Dev model
    with tf.name_scope('Dev'):
      dev_data = InputDataset(dev_path, FEATURES, FLAGS.dev_batch_size)
      with tf.variable_scope('Model', reuse=True):
        dev_words = dev_data.batch['words']
        dev_lengths = dev_data.batch['length']
        dev_labels = dev_data.batch['label']
        dev_logits = model_builder(dev_words, lengths=dev_lengths)

        metrics = get_metrics(dev_logits, dev_labels)
        _, dev_num_correct, dev_num_total = metrics

        dev_f1_stats = {label_index: get_class_f1_stats(
                        dev_logits, dev_labels, label_index)
                        for label_index in dataset.labels._i2v}

    dev_fetches = {"num_correct": dev_num_correct,
                   "num_total": dev_num_total,
                   }

    # Test model
    with tf.name_scope('Test'):
      test_data = InputDataset(test_path, FEATURES, FLAGS.test_batch_size)
      with tf.variable_scope('Model', reuse=True):
        test_words = test_data.batch['words']
        test_lengths = test_data.batch['length']
        test_labels = test_data.batch['label']
        # test_words.set_shape([None, 140])
        test_logits = model_builder(test_words, lengths=test_lengths)

        metrics = get_metrics(test_logits, test_labels)
        _, test_num_correct, test_num_total = metrics

        test_f1_stats = {label_index: get_class_f1_stats(
                         test_logits, test_labels, label_index)
                         for label_index in dataset.labels._i2v}

    test_fetches = {"num_correct": test_num_correct,
                    "num_total": test_num_total,
                    }

    inputs = tf.placeholder(
        shape=[None, dataset.MAX_LENGTH], dtype=tf.int32, name='inputs')
    logits = model_builder(inputs, is_training=False)
    logits = tf.identity(logits, name='logits')

    for fetches, stats in [(train_fetches, train_f1_stats),
                           (dev_fetches, dev_f1_stats),
                           (test_fetches, test_f1_stats)]:

      for (label_index, stats_dict) in stats.items():
        for key, val in stats_dict.items():
          fetches["{}_{}".format(label_index, key)] = val

    if FLAGS.check_numerics:
      logging.info("Checking numerics...")
      tf.add_check_numerics_ops()

    # Run the model
    dev_accuracies = []
    dev_f1s = []
    test_accuracies = []
    test_f1s = []
    saver = tf.train.Saver(max_to_keep=5)
    with tf.train.SingularMonitoredSession(config=get_proto_config()) as sess:
      writer = tf.summary.FileWriter(FLAGS.tensorboard_output, sess.graph)
      for epoch in range(FLAGS.num_epoch):
        logging.info("Epoch %d...", epoch)
        init_ops = [train_data.init_op]
        if FLAGS.use_pretrain:
          init_ops.append(pretrain_data.init_op)
        train_start = time.time()
        train_v = run_epoch(sess, train_fetches.copy(),
                            train_ops=[train_op],
                            init_ops=init_ops)
        train_end = time.time()
        dev_v = run_epoch(sess, dev_fetches.copy(),
                          init_ops=[dev_data.init_op])
        test_v = run_epoch(sess, test_fetches.copy(),
                           init_ops=[test_data.init_op])

        loss = train_v['loss']
        reg_loss = train_v['reg_loss']
        logging.info("train loss: {:.3f}".format(loss))
        # logging.info("train reg_loss: {:.3f}".format(reg_loss))
        add_tensorboard_summary(writer, 'loss', loss, epoch)

        train_f1 = get_f1(dataset, train_v)

        train_accuracy = train_v['num_correct'] / train_v['num_total']
        logging.info("train examples: {}".format(train_v['num_total']))
        logging.info("train accuracy: {:.3f}".format(train_accuracy))
        logging.info("train f1: {:.3f}".format(train_f1))
        logging.info("train runtime: {:.1f}".format(train_end - train_start))
        add_tensorboard_summary(writer, 'train_f1', train_f1, epoch)
        add_tensorboard_summary(
            writer, 'train_accuracy', train_accuracy, epoch)

        logging.info("dev examples: {}".format(dev_v['num_total']))
        dev_accuracy = dev_v['num_correct'] / max(1, dev_v['num_total'])
        logging.info("dev accuracy: {:.3f}".format(dev_accuracy))
        add_tensorboard_summary(writer, 'dev_accuracy', dev_accuracy, epoch)
        dev_accuracies.append(dev_accuracy)

        dev_f1 = get_f1(dataset, dev_v)
        logging.info("dev f1: {:.3f}".format(dev_f1))
        add_tensorboard_summary(writer, 'dev_f1', dev_f1, epoch)
        dev_f1s.append(dev_f1)

        logging.info("test examples: {}\n".format(test_v['num_total']))
        test_accuracy = test_v['num_correct'] / max(1, test_v['num_total'])
        add_tensorboard_summary(writer, 'test_accuracy', test_accuracy, epoch)
        test_accuracies.append(test_accuracy)

        test_f1 = get_f1(dataset, test_v)
        add_tensorboard_summary(writer, 'test_f1', test_f1, epoch)
        test_f1s.append(test_f1)

        with open(FLAGS.json_output, 'a') as outf:
          outline = {'timestamp': time.time(), 'epoch': epoch,
                     'train_f1': train_f1,
                     'train_accuracy': train_accuracy,
                     'dev_f1': dev_f1,
                     'dev_accuracy': dev_accuracy,
                     'test_f1': test_f1,
                     'test_accuracy': test_accuracy,
                     }
          outf.write(json.dumps(outline, cls=NumpySerializer) + '\n')

        # After every 10 epochs, save model
        if (1 + epoch) % 10 == 0 or (1 + epoch) == FLAGS.num_epoch:
          saver.save(sess.raw_session(),
                     os.path.join(FLAGS.model_output, 'model'),
                     global_step=epoch)

  with open(FLAGS.json_output, 'a') as outf:
    stop_epoch = calculate_early_stop_epoch(dev_accuracies)
    stop_epoch = min(stop_epoch, len(dev_accuracies) - 1)

    stopped_dev_accuracy = dev_accuracies[stop_epoch]
    stopped_dev_f1 = dev_f1s[stop_epoch]
    logging.info("Final dev accuracy: {:.3f}".format(stopped_dev_accuracy))
    logging.info("Final dev f1: {:.3f}".format(stopped_dev_f1))

    stopped_test_accuracy = test_accuracies[stop_epoch]
    stopped_test_f1 = test_f1s[stop_epoch]
    logging.info("Final test accuracy: {:.3f}".format(stopped_test_accuracy))
    logging.info("Final test f1: {:.3f}".format(stopped_test_f1))

    outline = {'timestamp': time.time(),
               'stopped_test_accuracy': stopped_test_accuracy,
               'stopped_test_f1': stopped_test_f1,
               'stopped_dev_accuracy': stopped_dev_accuracy,
               'stopped_dev_f1': stopped_dev_f1,
               'dev_accuracies': dev_accuracies,
               'test_accuracies': test_accuracies,
               'dev_f1s': dev_f1s,
               'test_f1s': test_f1s,
               }
    outf.write(json.dumps(outline, cls=NumpySerializer) + '\n')


def get_f1(dataset, results):
  values = []
  for label_index in dataset.labels._i2v:
    tp = results['{}_tp'.format(label_index)]
    fp = results['{}_fp'.format(label_index)]
    fn = results['{}_fn'.format(label_index)]
    values.append(calculate_f1(tp, fp, fn))
  return np.mean(values)


def calculate_early_stop_epoch(dev_accuracies):
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
  config.intra_op_parallelism_threads = FLAGS.num_intra_threads
  config.inter_op_parallelism_threads = FLAGS.num_inter_threads
  config.gpu_options.force_gpu_compatible = FLAGS.force_gpu_compatible
  return config


if __name__ == "__main__":
  main()
