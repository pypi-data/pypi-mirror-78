import contextlib
import gzip
import json
import logging
import os
import random

import numpy as np

from demographer.tflm import SymbolTable

from demographer.transformer_selfreport import extract_features
from demographer.transformer_selfreport import transform_features
from demographer.transformer_selfreport import load_transformers
from demographer.label_mapping import race_label_mapping, vocab_mapping

work_dir = '/export/c10/zach/demographics/models/datasets/noisy'
dev_dir = '/export/c10/zach/demographics/models/datasets/baseline'


class ComboDataset:

  UNIGRAM_VOCAB = 78066
  MAX_LENGTH = 32
  PAD = "&pad;"
  UNK = "&unk;"

  def __init__(self, datasets, confidences, setup='profile', balance_dev=False, balance_test=False):
    np.random.seed(42)

    assert len(confidences) == len(datasets)
    assert setup in ['profile', 'unigrams', 'both']

    self.setup = setup
    self.confidences = confidences
    self.names = datasets
    self.profile_data = [
        os.path.join(work_dir, "{}.json.gz".format(name)) for name in datasets]
    self.unigram_data = [
        os.path.join(work_dir, "{}.unigrams.json.gz".format(name)) for name in datasets]
    dataset_str = "__".join(sorted(datasets))
    self.suffix = "{}.{}".format(dataset_str, setup)
    self.work = work_dir
    self._lengths = []

    # if balance_dev:
    #   dev_json_file = os.path.join(dev_dir, 'balanced_dev.{}.json.gz'.format(setup))
    # else:
    #   dev_json_file = os.path.join(dev_dir, 'dev.{}.json.gz'.format(setup))
    # if balance_test:
    #   test_json_file = os.path.join(dev_dir, 'balanced_test.{}.json.gz'.format(setup))
    # else:
    #   test_json_file = os.path.join(dev_dir, 'test.{}.json.gz'.format(setup))
    self.setup_file = '{}.tmp.json.gz'.format(dataset_str)
    self.json_files = [os.path.join(work_dir, 'train.{}.json.gz'.format(self.suffix))]
    self.transformers = load_transformers()

    self.setup_dataset()

  def setup_dataset(self):

    if self.setup in ['profile', 'both']:
      for fn in self.profile_data:
        if not os.path.exists(os.path.join(self.work, fn)):
          raise ValueError("need to download data to {}".format(fn))
    if self.setup in ['unigrams', 'both']:
      for fn in self.unigram_data:
        if not os.path.exists(os.path.join(self.work, fn)):
          raise ValueError("need to download data to {}".format(fn))

    if not self._setup_files_ready():
      setup_path = os.path.join(self.work, self.setup_file)
      if os.path.exists(setup_path):
        os.remove(setup_path)
      skipped = 0

      with contextlib.ExitStack() as stack:
        profile_infns = [os.path.join(self.work, fn) for fn in self.profile_data]
        profile_infs = [stack.enter_context(gzip.open(infn)) for infn in profile_infns]

        unigram_infns = [os.path.join(self.work, fn) for fn in self.unigram_data]
        unigram_infs = [stack.enter_context(gzip.open(infn)) for infn in unigram_infns]

        outf = stack.enter_context(gzip.open(setup_path, "w"))

        profile_dataset = {}

        for i, inf in enumerate(profile_infs):
          for line in inf:
            d = json.loads(line.decode())
            user = self.get_user(d)
            userid = user['id_str']
            label = vocab_mapping[race_label_mapping[user['label']]]
            weight = user.get("confidence", 1.0) * self.confidences[i]
            if label is None:
              skipped += 1
              continue

            features = {'userid': userid, 'name': user['name'],
                        'label': label, 'weight': weight}
            profile_features = extract_features(user)
            profile_features = transform_features(self.transformers, profile_features)
            features.update(profile_features)

            profile_dataset[userid] = features

        print("skipped {} profile-only users".format(skipped))

        try:
          for i, inf in enumerate(unigram_infs):
            for line in inf:
              d = json.loads(line.decode())
              userid = d['userid']
              if userid not in profile_dataset:
                skipped += 1
                continue

              # Pop to remove
              features = profile_dataset.pop(userid)
              features['unigrams'] = d['unigrams']

              outf.write("{}\n".format(json.dumps(features)).encode('utf8'))
        except EOFError:
          logging.error("**ERROR: EOF on {}".format(inf))

        print("skipped {} profile+unigram users".format(skipped))

        for userid, features in profile_dataset.items():
          features['unigrams'] = []

          outf.write("{}\n".format(json.dumps(features)).encode('utf8'))

    self._build_vocab()

    if not self.json_ready():
      self._write_json()

    self._rng = random.Random()
    self._rng.seed(42)

  def _build_vocab(self):
    vocab_path = os.path.join(self.work, "vocab.json.gz")
    if os.path.exists(vocab_path):
      with gzip.open(vocab_path) as inf:
        obj = json.loads(inf.readline().decode())
        self._vocab = SymbolTable.from_json(obj)
        obj = json.loads(inf.readline().decode())
        self._labels = SymbolTable.from_json(obj)
        return
    else:
      raise IOError("we aren't building a new vocab for combo_dataset.py")

    # self._vocab = SymbolTable()
    # self._labels = SymbolTable()

    # # Create symbol table on training data
    # infn = os.path.join(self.work, self.setup_file)
    # with gzip.open(infn) as inf:
    #   for line in inf:
    #     try:
    #       d = json.loads(line.decode().rstrip())
    #     except Exception as e:
    #       print(line, str(e))
    #       continue
    #     self._labels.add(d['label'])
    #     length = 0
    #     for token in d['name']:
    #       self._vocab.add(token)
    #       length += 1
    #     for _ in range(ComboDataset.MAX_LENGTH - length):
    #       self._vocab.add(ComboDataset.PAD)
    #     self._lengths.append(length)

    # # Freeze symbol tables
    # self._vocab.freeze(unk=ComboDataset.UNK)
    # self._labels.freeze()

  def _encode_name(self, name):
    return [self._vocab.idx(char) for char in name]

  def get_user(self, d):
    if 'user' in d:
      return d['user']
    else:
      return d

  def _write_json(self):
    assert self._vocab.frozen, "Vocab must be frozen before writing json"

    infn = os.path.join(self.work, self.setup_file)
    outfn = self.json_files[0]
    with gzip.open(infn) as inf, gzip.open(outfn, 'w') as outf:
      for line in inf:
        d = json.loads(line.decode().rstrip())
        d['label'] = self._labels.idx(d['label'])
        # d['label'] = vocab_mapping[label_mapping[user['label']]]
        tokens = d.pop('name')
        if self.setup in ['profile', 'both']:
          tokens = self._encode_name(tokens)
          tokens = tokens[:ComboDataset.MAX_LENGTH]
          length = len(tokens)
          d['length'] = length
          tokens += [self._vocab.idx(ComboDataset.PAD)
                     for i in range(ComboDataset.MAX_LENGTH - length)]
          d['tokens'] = tokens
        if self.setup == 'profile':
          d.pop('unigrams')
        outf.write("{}\n".format(json.dumps(d)).encode('ascii'))

  def json_ready(self):
    return all([os.path.exists(fn) for fn in self.json_files])

  def _setup_files_ready(self):
    return os.path.exists(os.path.join(self.work, self.setup_file))

  def yield_json(self, json_index):
    fn = self.json_files[json_index]
    with gzip.open(fn, 'r') as inf:
      for line in inf:
        yield json.loads(line.decode().rstrip())

  @property
  def train(self):
    return self.yield_json(0)

  @property
  def labeled(self):
    return self.yield_json(0)

  @property
  def unlabeled(self):
    return []

  # @property
  # def dev(self):
  #   return self.yield_json(1)

  # @property
  # def test(self):
  #   return self.yield_json(2)

  @property
  def rng(self):
    return self._rng

  @property
  def lengths(self):
    return self._lengths

  @property
  def vocab(self):
    return self._vocab

  @property
  def labels(self):
    return self._labels


if __name__ == '__main__':
  d = ComboDataset(['baseline', 'group_person.thre035'], [1.0, 1.0], setup='profile')
  print("vocab_size: {}".format(len(d.vocab)))
  lengths = d.lengths
  if len(lengths) > 0:
    print("Lengths: mean is {}, median is {}, 90th is {} 95th is {}, max is {}".format(
        np.mean(lengths), np.median(lengths),
        np.percentile(lengths, 90), np.percentile(lengths, 95),
        np.max(lengths)))
