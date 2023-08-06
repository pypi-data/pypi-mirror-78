import os
from collections import defaultdict

import numpy as np
import tensorflow as tf

logging = tf.logging


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


def get_metrics(logits, labels):
  loss = get_loss(logits, labels)
  num_correct = get_num_correct(logits, labels)
  num_total = tf.shape(labels)[0]
  return loss, num_correct, num_total


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


def calculate_f1(tp, fp, fn):
  p = tp / max(1, tp + fp)
  r = tp / max(1, tp + fn)
  f1 = 2 * p * r / max(1, p + r)
  # print("p: {:.3f}, r: {:.3f}".format(p, r))
  if np.isnan(f1):
    return 0.0
  return f1


def printout(name, **kwargs):
  for key, value in sorted(kwargs.items()):
    try:
      logging.info("{} {}: {:.3f}".format(name, key, value))
    except Exception as e:
      logging.warn("failed to print {} {}: {}".format(name, key, e))


def get_loss(logits, targets):
  targets = tf.cast(targets, tf.int32)
  ce = tf.nn.sparse_softmax_cross_entropy_with_logits(
      logits=logits, labels=targets)
  return tf.reduce_mean(ce)


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


def write_features(examples, file_name, corpus_text_key="tokens",
                   corpus_label_key='label', sort=True):

  logging.info("Writing features to: {}".format(file_name))

  if sort:
    examples = sorted(examples, key=lambda x: len(x[corpus_text_key]))

  token_counts = defaultdict(int)
  has_label = 0.
  num_examples = 0.
  with tf.python_io.TFRecordWriter(file_name) as writer:
    for example in examples:
      num_examples += 1
      tokens = example[corpus_text_key]
      for token in tokens:
        token_counts[token] += 1
      length = example.get('length', len(tokens))
      label = example.get(corpus_label_key, None)
      num_ones = example.get('num_ones', None)
      feature = {
          'words': tf.train.Feature(int64_list=tf.train.Int64List(value=tokens)),
          'length': tf.train.Feature(int64_list=tf.train.Int64List(value=[length]))
      }
      if label is not None:
        has_label += 1
        feature['label'] = tf.train.Feature(
            int64_list=tf.train.Int64List(value=[label]))
      if num_ones is not None:
        feature['num_ones'] = tf.train.Feature(
            int64_list=tf.train.Int64List(value=[num_ones]))

      record = tf.train.Example(features=tf.train.Features(
          feature=feature))
      writer.write(record.SerializeToString())

  # print("token counts:", token_counts)
  print('for fn {}, {} of {} examples had label'.format(
      file_name, has_label, num_examples))


def feature_extraction(dataset, sort=True, force_preproc=False,
                       pretrain=True):
  data_path = dataset.workdir
  # vocab_size = len(dataset.vocab)
  if pretrain:
    pretrain_records = os.path.join(data_path, 'pretrain.tf')
  train_records = os.path.join(data_path, 'train.tf')
  dev_records = os.path.join(data_path, 'dev.tf')
  test_records = os.path.join(data_path, 'test.tf')
  if pretrain:
    all_records = (pretrain_records, train_records, dev_records, test_records)
  else:
    all_records = (train_records, dev_records, test_records)
  if not all(os.path.exists(x) for x in all_records) or force_preproc:
    if pretrain:
      write_features(dataset.pretrain, pretrain_records, sort=sort)
    write_features(dataset.train, train_records, sort=sort)
    write_features(dataset.dev, dev_records, sort=sort)
    write_features(dataset.test, test_records, sort=sort)
  return all_records


def infer_feature_extraction(dataset, sort=True, suffix=''):
  data_path = dataset.work
  vocab_size = len(dataset.vocab)
  test_records = os.path.join(data_path, 'test{}.tf'.format(suffix))
  write_humanizr_features(dataset.test, vocab_size, test_records, sort=sort)
  return test_records


def humanizr_feature_extraction(dataset, sort=True, suffix='',
                                force_preproc=False):
  data_path = dataset.work
  vocab_size = len(dataset.vocab)
  train_records = os.path.join(data_path, 'train{}.tf'.format(suffix))
  dev_records = os.path.join(data_path, 'dev{}.tf'.format(suffix))
  test_records = os.path.join(data_path, 'test{}.tf'.format(suffix))
  all_records = (train_records, dev_records, test_records)
  if not all(os.path.exists(x) for x in all_records) or force_preproc:
    write_humanizr_features(dataset.train, vocab_size, train_records, sort=sort)
    write_humanizr_features(dataset.dev, vocab_size, dev_records, sort=sort)
    write_humanizr_features(dataset.test, vocab_size, test_records, sort=sort)
  return all_records


def write_humanizr_features(examples, vocab_size, file_name,
                            corpus_text_key='tokens', corpus_id_key='id',
                            corpus_label_key='label', sort=True):

  logging.info("Writing features to: {}".format(file_name))

  if sort:
    examples = sorted(examples, key=lambda x: len(x[corpus_text_key]))

  token_counts = defaultdict(int)
  has_label = 0.
  num_examples = 0.
  with tf.python_io.TFRecordWriter(file_name) as writer:
    for example in examples:
      num_examples += 1
      tokens = example[corpus_text_key]
      for token in tokens:
        token_counts[token] += 1
      length = example.get('length', len(tokens))
      label = example.get(corpus_label_key, None)
      tweet_id = example.get(corpus_id_key, None)
      meta_features = []
      for key in [
          "friends_count", "followers_count", "ratio", "listed_count",
          "statuses_count", "descr_high", "collective_pronouns",
          "personal_pronouns", "rep_punc", "verified",
          "tweets_per_month", "months"
      ]:
          meta_features.append(float(example.get(key, 0.)))

      feature = {'words': tf.train.Feature(int64_list=tf.train.Int64List(value=tokens)),
                 'length': tf.train.Feature(int64_list=tf.train.Int64List(value=[length])),
                 'meta': tf.train.Feature(
          float_list=tf.train.FloatList(value=[float(x) for x in meta_features]))
      }
      if label is not None:
        has_label += 1
        feature['label'] = tf.train.Feature(
            int64_list=tf.train.Int64List(value=[label]))
      if tweet_id is not None:
        feature['id'] = tf.train.Feature(
            int64_list=tf.train.Int64List(value=[tweet_id]))

      record = tf.train.Example(features=tf.train.Features(
          feature=feature))
      writer.write(record.SerializeToString())


def run_epoch(session, fetches, train_ops=[], init_ops=[],
              fd={}, num_batches=-1):

  outputs = defaultdict(float)

  for init_op in init_ops:
    session.run(init_op)

  batch_index = 0
  while num_batches < 0 or batch_index < num_batches:
    # if not batch_index % 100: tf.logging.warn(batch_index)
    try:
      for i, train_op in enumerate(train_ops):
        fetches['train_op {}'.format(i)] = train_op

      results = session.run(fetches, feed_dict=fd)
      outputs['num_iter'] += 1

      for key in results:
        if not key.startswith('train_op'):
          try:
            outputs[key] += results[key]
          except Exception as e:
            logging.warn("run_epoch: {}".format(e))
            pass

    except tf.errors.OutOfRangeError:
      break

    batch_index += 1

  # print("epoch: {} iters and {} examples".format(
  #       outputs['num_iter'], outputs.get('num_total', '?')))

  return outputs
