from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import numpy as np
import os

from collections import namedtuple
from combo_dataset import ComboDataset

from demographer.demographer import Demographer
from demographer.encoders_selfreport import get_encoder_template
from demographer.experiment_runner_selfreport import feature_extraction
from demographer.experiment_runner_selfreport import get_class_acc
from demographer.experiment_runner_selfreport import get_class_f1_stats
from demographer.experiment_runner_selfreport import get_metrics
from demographer.experiment_runner_selfreport import run_epoch
from demographer.selfreport_dataset import EvalDataset
from demographer.tflm import InputDataset
from demographer.utils import tf

flags = tf.flags
FLAGS = flags.FLAGS

flags.DEFINE_string("load_model", 'demographer/models/ethnicity_selfreport/www2--Combo__exact_group.thre035--24cb07e3-124', "file to load model from")  # noqa
flags.DEFINE_string("eval_output", 'output.txt', "where to write inferred labels to file")
flags.DEFINE_string("name", 'test_job', "name for the job")
flags.DEFINE_string("json_output", None, "Json output path")
flags.DEFINE_string("tensorboard_output", None, "Tensorboard output path")
flags.DEFINE_string("model_output", None, "Model output path")

flags.DEFINE_string("dataset", "data/faketweets.txt", "Dataset class")
# flags.DEFINE_string("dataset", "Names", "Dataset class")
flags.DEFINE_string("noisy_type", "exact_group", "Dataset class")
flags.DEFINE_string("feature_type", "profile", "one of: profile,unigrams,both,neither")
flags.DEFINE_string("loss_type", "ce", "ce or mae")
flags.DEFINE_float("train_balance_ratio", 1.0, "ratio of individuals to organizations")

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
flags.DEFINE_integer("num_epoch", 50, "Number of training epochs.")
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
flags.DEFINE_float("lr", 0.5, "Starting learning rate.")
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

logging = tf.logging
Data = namedtuple('Data',
                  'data words meta labels lengths unigrams weights userids')


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


def get_dataset(num_labeled):
  # if FLAGS.dataset == 'Baseline':
  #   dataset = Baseline(setup=FLAGS.feature_type)
  # elif FLAGS.dataset == 'Noisy':
  #   dataset = NoisyDataset('group_person', setup=FLAGS.feature_type)
  # elif FLAGS.dataset == 'ConstantBits':
  #   dataset = ConstantBits()
  # elif FLAGS.dataset == 'RandomBits':
  #   dataset = RandomBits()
  # elif os.path.exists(FLAGS.dataset):
  if FLAGS.dataset.startswith('Combo__'):
    datasets = FLAGS.dataset[7:].split("__")
    confidences = [1.0 for _ in datasets]
    feature_type = FLAGS.feature_type
    dataset = ComboDataset(datasets, confidences, setup=feature_type,)
  elif os.path.exists(FLAGS.dataset):
    workdir = os.path.split(FLAGS.dataset)[0]
    dataset = EvalDataset(FLAGS.dataset, workdir)
    return None, dataset, len(dataset.vocab), len(dataset.labels)
  else:
    raise ValueError("Unknown dataset: {}".format(FLAGS.dataset))


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
  # elif FLAGS.collapser == 'Bahdanau':
  #   def collapser(tensors, lengths=None):
  #     attn = Bahdanau(FLAGS.hidden_dim, tensors, lengths)
  #
  #     alignment = tf.zeros_like(tf.slice(
  #         tensors, [0, 0, 0], [-1, -1, 0]))
  #
  #     for encoding in tf.unstack(tensors, axis=1):
  #       alignment = attn(encoding, alignment)
  #
  #     alignment = tf.expand_dims(alignment, [2])
  #     weighted_sum = tf.reduce_sum(tensors * alignment, [1])
  #     return weighted_sum
  elif FLAGS.collapser == 'None':
    def collapser(tensors):
      return tensors
  else:
    raise ValueError("Unknown collapser: {}".format(FLAGS.collapser))

  return collapser


def get_proto_config():
  config = tf.ConfigProto()
  config.allow_soft_placement = True
  # if FLAGS.gpu > 0:
  #   config.log_device_placement = True
  config.intra_op_parallelism_threads = FLAGS.num_intra_threads
  config.inter_op_parallelism_threads = FLAGS.num_inter_threads
  config.gpu_options.force_gpu_compatible = FLAGS.force_gpu_compatible
  return config


class SelfReportEthnicityDemographer(Demographer):
  name_key = 'ethnicity_selfreport'

  def __init__(self, model_dir=None, setup='', dtype='n'):
    """Initalizes a class for an Ethnicity neural classifier
    trained on noisy self-report dataset

    Constructor needs to load a classifier from tensorflow

    Args:
        model_dir: where does the model live?

    """
    # TODO: balanced option?
    # NOTE: load model here
    # if not model_dir:
    #   base_dir = os.path.dirname(sys.modules[__package__].__file__)
    #   model_dir = os.path.join(base_dir, 'models', 'ethnicity_selfreport')

    logging.set_verbosity(tf.logging.INFO)
    # writer = ExperimentWriter(
    #   FLAGS.json_output, FLAGS.tensorboard_output, FLAGS.__flags)
    data_device = get_data_device(FLAGS.gpu)

    # Prepare the dataset and model from flags
    # TODO: change get_dataset, only get dev, and move it to process_tweet
    train_dataset, dev_dataset, vocab_size, num_labels = get_dataset(-1)

    max_length = dev_dataset.MAX_LENGTH
    unigram_vocab_size = dev_dataset.UNIGRAM_VOCAB

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

    if hasattr(dev_dataset, 'suffix'):
      dataset_suffix = dev_dataset.suffix
    else:
      dataset_suffix = ''
    dev_paths = feature_extraction(
        dev_dataset,
        sort=FLAGS.sort,
        force_preproc=FLAGS.force_preproc,
        suffix=dataset_suffix,
        train=False, dev=True, test=False)
    dev_path = dev_paths['dev']

    FEATURES = {'label': tf.FixedLenFeature([], tf.int64)}
    # if FLAGS.feature_type in ['both', 'profile']:
    FEATURES['length'] = tf.FixedLenFeature([], tf.int64)
    FEATURES['words'] = tf.VarLenFeature(tf.int64)
    FEATURES['meta'] = tf.FixedLenFeature([8], tf.float32)
    FEATURES['userid'] = tf.FixedLenFeature([], tf.string)
    # if FLAGS.feature_type == 'neither':
    #   FEATURES['meta'] = tf.FixedLenFeature([8], tf.float32)
    # if FLAGS.feature_type in ['both', 'unigrams']:
    #   FEATURES['unigrams'] = tf.VarLenFeature(tf.int64)

    logging.info("Creating computation graph...")
    with tf.Graph().as_default(), tf.device(data_device):
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

      # if FLAGS.rebalance or FLAGS.load_model:
      if FLAGS.load_model:
        dev_fetches["logits"] = dev_logits
        dev_fetches["labels"] = dev.labels

      for label, label_idx in dev_dataset.labels._v2i.items():
        stats = get_class_acc(dev_logits, dev.labels, label_idx)
        dev_fetches["num_total_{}".format(label)] = stats['num_total']
        dev_fetches["num_correct_{}".format(label)] = stats['num_correct']

      # if FLAGS.test:
      #   test = get_data(test_path, FEATURES, FLAGS.test_batch_size,
      #                   max_length=max_length)
      #   test_logits = model_builder(tokens=test.words, meta=test.meta,
      #                               is_training=False,
      #                               lengths=test.lengths, unigrams=test.unigrams)
      #   metrics = get_metrics(test_logits, test.labels)
      #   _, test_num_correct, test_num_total = metrics
      #   test_classifications = tf.equal(tf.argmax(test_logits, axis=1), test.labels)
      #   test_fetches = {"num_correct": test_num_correct,
      #                   "num_total": test_num_total,
      #                   "classifications": test_classifications,
      #                   "userids": test.userids,
      #                   }
      #
      #   for label, label_idx in test_dataset.labels._v2i.items():
      #     stats = get_class_acc(test_logits, test.labels, label_idx)
      #     test_fetches["num_total_{}".format(label)] = stats['num_total']
      #     test_fetches["num_correct_{}".format(label)] = stats['num_correct']
      #
      #   if FLAGS.rebalance:
      #     test_fetches["logits"] = test_logits
      #     test_fetches["labels"] = test.labels

      if FLAGS.use_f1:
        for label, label_index in dev_dataset.labels._v2i.items():
          stats = get_class_f1_stats(dev_logits, dev.labels, label_index)
          for key, val in stats.items():
            dev_fetches["{}_{}".format(label, key)] = val

          # if FLAGS.test:
          #   stats = get_class_f1_stats(test_logits, test.labels, label_index)
          #   for key, val in stats.items():
          #     test_fetches["{}_{}".format(label, key)] = val

      # if FLAGS.check_numerics:
      #   logging.info("Checking numerics...")
      #   tf.add_check_numerics_ops()

      # if FLAGS.count_params:
      total_params = 0
      for tvar in tf.trainable_variables():
        shape = tvar.get_shape().as_list()
        total_params += np.prod(shape)
        # print(tvar.name, shape)
      logging.info("Total number of params: {}".format(total_params))

      logging.info("Graph complete. Training...")

      # Run the model
      saver = tf.train.Saver(max_to_keep=FLAGS.num_epoch, )
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


if __name__ == "__main__":
  tweets = [
      {"name": "Zach Wood-Doughty", "screen_name": "zachwooddoughty", "location": None, "url": None, "description": "PhD student at @JHUCLSP", "protected": False, "verified": False, "followers_count": 76, "friends_count": 89, "listed_count": 6, "favourites_count": 367, "statuses_count": 3013, "created_at": "Thu Dec 24 17: 07: 51 +0000 2015", },  # noqa
      {"name": "ESPN", "screen_name": "ESPN", "location": "Sports", "url": "espn.com", "description": "Best place to follow all your favorite news websites", "protected": False, "verified": True, "followers_count": 10000000, "friends_count": 42, "listed_count": 1235, "favourites_count": 123, "statuses_count": 20013, "created_at": "Thu Dec 24 17: 07: 51 +0000 2012", }  # noqa
  ]
  balanced = SelfReportEthnicityDemographer()
  for tweet in tweets:
    print(balanced.process_tweet(tweet))
