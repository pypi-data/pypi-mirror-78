import absl.flags
import os
import json
from collections import defaultdict

import numpy as np
import tensorflow as tf

logging = tf.logging


class NumpySerializer(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, np.integer):
      return int(obj)
    elif isinstance(obj, np.floating):
      return float(obj)
    elif isinstance(obj, np.ndarray):
      return obj.tolist()
    elif isinstance(obj, absl.flags._flag.Flag):
      return obj.value
    else:
      return super(NumpySerializer, self).default(obj)


def collapse_fetches(d):
  ''' print out fetches from session run but collapse lists '''
  new_d = {}
  for key, val in d.items():
    if isinstance(val, list) or isinstance(val, np.ndarray):
      new_d[key] = float(np.mean(val))
    elif isinstance(val, dict):
      new_d[key] = collapse_fetches(val)
    else:
      new_d[key] = val
  return new_d


def get_metrics(logits, labels, weights=None, loss_type='ce'):
  loss = get_loss(logits, labels, weights=weights, loss_type=loss_type)
  num_correct = get_num_correct(logits, labels)
  num_total = tf.shape(labels)[0]
  return loss, num_correct, num_total


def get_class_acc(logits, labels, query_val, dtype=tf.int64):
  pred = tf.argmax(logits, axis=-1)
  true = tf.cast(labels, dtype=dtype)
  query = tf.constant(query_val, shape=(), dtype=dtype)

  true_query = tf.equal(true, query)
  pred_query = tf.equal(pred, query)
  tp = tf.reduce_sum(tf.cast(
      tf.logical_and(pred_query, true_query), dtype=dtype))
  fp = tf.reduce_sum(tf.cast(
      tf.logical_and(pred_query, tf.logical_not(true_query)), dtype=dtype))
  fn = tf.reduce_sum(tf.cast(
      tf.logical_and(tf.logical_not(pred_query), true_query), dtype=dtype))
  tn = tf.reduce_sum(tf.cast(
      tf.logical_and(tf.logical_not(pred_query), tf.logical_not(true_query)), dtype=dtype))

  num_total = tp + fn
  num_correct = tp

  return {'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn,
          'num_total': num_total, 'num_correct': num_correct}


def get_class_f1_stats(logits, labels, query_val, dtype=tf.int64):
  ''' Macro F1 score for a given query label '''

  pred = tf.argmax(logits, axis=-1)
  true = tf.cast(labels, dtype=dtype)
  query = tf.constant(query_val, shape=(), dtype=dtype)

  true_query = tf.equal(true, query)
  pred_query = tf.equal(pred, query)
  tp = tf.reduce_sum(tf.cast(
      tf.logical_and(pred_query, true_query), dtype=dtype))
  fp = tf.reduce_sum(tf.cast(
      tf.logical_and(pred_query, tf.logical_not(true_query)), dtype=dtype))
  fn = tf.reduce_sum(tf.cast(
      tf.logical_and(tf.logical_not(pred_query), true_query), dtype=dtype))

  # return (tp, fp, fn)
  return {'tp': tp, 'fp': fp, 'fn': fn}


def calculate_recall(tp, fn):
  if tp + fn == 0:
    return 0.0
  return tp / float(tp + fn)


def get_f1(fetches, labels, average='macro'):
  sums = defaultdict(int)
  f1_calcs = []
  # for label, label_index in dataset.labels._v2i.items():
  for label in labels:
    pieces = []
    for stat in ["tp", "fp", "fn"]:
      key = "{}_{}".format(label, stat)
      sums[stat] += np.sum(fetches[key])
      pieces.append(np.sum(fetches[key]))

    f1_calcs.append(calculate_f1(*pieces))

  if average == 'macro':
    return np.mean(f1_calcs)
  elif average == 'micro':
    return calculate_f1(*[sums[x] for x in ['tp', 'fp', 'fn']])
  else:
    raise ValueError("unk average {}".format(average))


def calculate_f1(tp, fp, fn):
  if tp + fp == 0:
    # logging.warn("nan precision")
    p = 0
  else:
    p = tp / (tp + fp)
  if tp + fn == 0:
    # logging.warn("nan precision")
    r = 0
  else:
    r = tp / (tp + fn)

  if p + r == 0:
    return 0.
  else:
    f1 = 2 * p * r / (p + r)

  return f1


def printout(name, **kwargs):
  for key, value in sorted(kwargs.items()):
    try:
      logging.info("{} {}: {:.3f}".format(name, key, value))
    except Exception as e:
      logging.warn("failed to print {} {}: {}".format(name, key, str(e)))


def mean_absolute_error(logits, targets, weights=None):
  targets = tf.one_hot(tf.cast(targets, tf.int32), 4)
  mae = tf.abs(logits - targets)
  if weights is not None:
    mae = tf.math.multiply(mae, weights)
  return tf.reduce_mean(mae)


def get_loss(logits, targets, weights=None, loss_type='ce'):
  targets = tf.cast(targets, tf.int32)
  # ce = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=targets)
  none = tf.losses.Reduction.NONE
  ce = tf.losses.sparse_softmax_cross_entropy(labels=targets, logits=logits, reduction=none)
  # print("** after losses.sparse() ce shape is {}".format(ce.get_shape()))
  return tf.reduce_mean(ce)


# def get_loss(logits, targets, weights=None, loss_type='ce'):
#   if loss_type == 'ce':
#     loss = weighted_ce_loss(logits, targets, weights=weights)
#   elif loss_type == 'mae':
#     loss = mean_absolute_error(logits, targets, weights=weights)
#   return loss


# def weighted_ce_loss(logits, targets, weights=None):
#     targets = tf.cast(targets, tf.int32)
#     if weights is None:
#       weights = 1.0
#     ce = tf.losses.sparse_softmax_cross_entropy(
#         labels=targets, logits=logits, weights=weights)
#     return tf.reduce_mean(ce)


def get_class_loss(logits, targets, query_val):
  query = tf.constant(query_val, shape=(), dtype=targets.dtype)

  true_query = tf.cast(tf.equal(targets, query), dtype=tf.float32)
  targets = tf.cast(targets, tf.int32)
  ce = tf.nn.sparse_softmax_cross_entropy_with_logits(
      logits=logits, labels=targets)
  class_ce = true_query * ce
  return tf.reduce_mean(class_ce)


def get_num_correct(logits, targets):
  targets = tf.cast(targets, tf.int64)
  predict = tf.argmax(logits, axis=-1)
  num_correct = tf.reduce_sum(tf.cast(
      tf.equal(predict, targets), dtype=tf.float32))
  return num_correct


def add_tensorboard_summary(writer, name, value, epoch):
  s = tf.Summary(value=[tf.Summary.Value(
      tag=name, simple_value=value)])
  writer.add_summary(s, global_step=epoch)


def infer_feature_extraction(dataset, sort=True, suffix=''):
  data_path = dataset.work
  # vocab_size = len(dataset.vocab)
  test_records = os.path.join(data_path, 'test{}.tf'.format(suffix))
  # write_features(dataset.test, vocab_size, test_records, sort=sort)
  write_features(dataset.test, test_records, sort=sort)
  return test_records


def feature_extraction(dataset, sort=True, suffix='', force_preproc=False,
                       train=True, dev=True, test=True):
  data_path = dataset.work
  train_records = os.path.join(data_path, 'train.{}.tf.gz'.format(suffix))
  dev_records = os.path.join(data_path, 'dev.{}.tf.gz'.format(suffix))
  test_records = os.path.join(data_path, 'test.{}.tf.gz'.format(suffix))

  all_records = {}
  if train:
    all_records['train'] = train_records
  if dev:
    all_records['dev'] = dev_records
  if test:
    all_records['test'] = test_records

  if train and not os.path.exists(train_records) or force_preproc:
    write_features(dataset.train, train_records, sort=sort)
  if dev and not os.path.exists(dev_records):
    write_features(dataset.dev, dev_records, sort=sort)
  if test and not os.path.exists(test_records):
    write_features(dataset.test, test_records, sort=sort)

  return all_records


def write_features(examples, file_name, corpus_text_key='tokens',
                   corpus_id_key='userid', corpus_weight_key='weight',
                   corpus_label_key='label', sort=True):

  logging.info("Writing features to: {}".format(file_name))

  if sort:
    examples = sorted(examples, key=lambda x: len(x.get(corpus_text_key, [])))

  token_counts = defaultdict(int)
  has_label = 0.
  has_weight = 0.
  num_examples = 0.
  tf_gzip = tf.python_io.TFRecordCompressionType.GZIP
  with tf.python_io.TFRecordWriter(file_name, options=tf_gzip) as writer:
    for example in examples:
      num_examples += 1
      tokens = example.get(corpus_text_key, [])
      for token in tokens:
        token_counts[token] += 1
      unigrams = example.get('unigrams', [])
      length = example.get('length', len(tokens))
      label = example.get(corpus_label_key, None)
      weight = example.get(corpus_weight_key, None)
      tweet_id = example.get(corpus_id_key, 'Unk')
      meta_features = []
      for key in [
          "friends_count", "followers_count", "ratio", "listed_count",
          "statuses_count", "verified", "tweets_per_month", "months"
      ]:
        meta_features.append(float(example.get(key, 0.)))

      feature = {
          'unigrams': tf.train.Feature(
              int64_list=tf.train.Int64List(value=unigrams)),
          'words': tf.train.Feature(
              int64_list=tf.train.Int64List(value=tokens)),
          'length': tf.train.Feature(
              int64_list=tf.train.Int64List(value=[length])),
          'meta': tf.train.Feature(
              float_list=tf.train.FloatList(value=[float(x) for x in meta_features]))
      }

      if label is not None:
        has_label += 1
        feature['label'] = tf.train.Feature(
            int64_list=tf.train.Int64List(value=[label]))

      if weight is not None:
        has_weight += 1
        feature['weight'] = tf.train.Feature(
            float_list=tf.train.FloatList(value=[weight]))

      if tweet_id is not None:
        feature[corpus_id_key] = tf.train.Feature(
            bytes_list=tf.train.BytesList(value=[tweet_id.encode('ascii')]))

      record = tf.train.Example(features=tf.train.Features(
          feature=feature))
      writer.write(record.SerializeToString())

  logging.warn("wrote {} examples to {}".format(num_examples, file_name))


def run_epoch(session, fetches, train_ops=[], init_ops=[],
              fd={}, num_batches=-1):
  outputs = defaultdict(list)

  for init_op in init_ops:
    session.run(init_op)

  batch_index = 0
  while num_batches < 0 or batch_index < num_batches:
    # if not batch_index % 100: tf.logging.warn(batch_index)
    try:
      for i, train_op in enumerate(train_ops):
        fetches['train_op {}'.format(i)] = train_op

      results = session.run(fetches, feed_dict=fd)

      for key in results:
        if not key.startswith('train_op'):
          try:
            if type(results[key]) == np.ndarray:
              outputs[key] += results[key].tolist()
            elif type(results[key]) == list:
              outputs[key] += results[key]
            else:
              outputs[key].append(results[key])
          except Exception as e:
            logging.error(str(e))
            pass

    except tf.errors.OutOfRangeError:
      break

    batch_index += 1

  # print("epoch: {} iters and {} examples".format(
  #       outputs['num_iter'], outputs.get('num_total', '?')))

  return outputs
