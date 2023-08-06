import contextlib
import gzip
import json
import logging
import os
import random

# import pdb; pdb.set_trace()

import numpy as np

from demographer.tflm import SymbolTable

from demographer.transformer_selfreport import extract_features
from demographer.transformer_selfreport import transform_features
from demographer.transformer_selfreport import load_transformers

work_dir = '/export/c10/zach/demographics/models/datasets/baseline'


class Baseline:

  UNIGRAM_VOCAB = 78066
  MAX_LENGTH = 32
  PAD = "&pad;"
  UNK = "&unk;"

  def __init__(self, setup='profile', balance_train=False, balance_dev=False, balance_test=False):
    np.random.seed(42)

    assert setup in ['profile', 'unigrams', 'both']
    balancing = [balance_train, balance_dev, balance_test]
    balance_str = "".join(str(int(x)) for x in balancing)

    self.setup_type = setup
    self.suffix = "{}.bal{}".format(setup, balance_str)
    self.work = work_dir
    self._lengths = []
    self.names = ("train", "dev", "test")

    # self.profile_files = ['baseline_{}.profile.json.gz'.format(name) for name in self.names]
    # self.unigram_files = ['baseline.unigrams.json.gz', 'daniel.unigrams.json.gz']
    # self.setup_files = ['{}.tmp.json.gz'.format(name) for name in self.names]
    # self.json_files = ['{}.{}.json.gz'.format(name, self.suffix) for name in self.names]

    profile_prefixes = ["balanced" if bal else "baseline" for bal in balancing]

    self.profile_files = ['{}_{}.profile.json.gz'.format(prefix, name)
                          for prefix, name in zip(profile_prefixes, self.names)]
    print(self.profile_files)
    self.unigram_files = ['baseline.unigrams.json.gz', 'daniel.unigrams.json.gz']
    self.setup_files = ['{}.{}.tmp.json.gz'.format(name, self.suffix) for name in self.names]
    self.json_files = ['{}.{}.json.gz'.format(name, self.suffix) for name in self.names]
    # if balance_dev:
    #   dev_json_file = os.path.join(dev_dir, 'balanced_dev.{}.json.gz'.format(setup))
    # else:
    #   dev_json_file = os.path.join(dev_dir, 'dev.{}.json.gz'.format(setup))
    # if balance_test:
    #   test_json_file = os.path.join(dev_dir, 'balanced_test.{}.json.gz'.format(setup))
    # else:
    #   test_json_file = os.path.join(dev_dir, 'test.{}.json.gz'.format(setup))

    self.transformers = load_transformers()
    self.setup()

  def setup(self):

    if self.setup in ['profile', 'both']:
      for fn in self.profile_data:
        if not os.path.exists(os.path.join(self.work, fn)):
          raise ValueError("need to download data to {}".format(fn))
    if self.setup in ['unigrams', 'both']:
      for fn in self.unigram_data:
        if not os.path.exists(os.path.join(self.work, fn)):
          raise ValueError("need to download data to {}".format(fn))

    if not self._setup_files_ready():

      for setup_file in self.setup_files:
        setup_path = os.path.join(self.work, setup_file)
        if os.path.exists(setup_path):
          os.remove(setup_path)
      skipped = 0

      with contextlib.ExitStack() as stack:
        # inf = stack.enter_context(gzip.open(os.path.join(self.work, Baseline.RAW_DATA), "rt"))
        profile_infns = {self.names[i]: os.path.join(self.work, self.profile_files[i])
                         for i in range(len(self.names))}
        profile_infs = {name: stack.enter_context(gzip.open(profile_infns[name]))
                        for name in self.names}

        # unigram_infn = os.path.join(self.work, self.unigram_file)
        # unigram_inf = stack.enter_context(gzip.open(unigram_infn))

        unigram_infns = [os.path.join(self.work, fn) for fn in self.unigram_files]
        unigram_infs = [stack.enter_context(gzip.open(infn)) for infn in unigram_infns]

        outfns = {self.names[i]: os.path.join(self.work, self.setup_files[i])
                  for i in range(len(self.names))}
        outfs = {name: stack.enter_context(gzip.open(outfns[name], "wb")) for name in self.names}

        profile_dataset = {}
        user_splits = {}

        for split, inf in profile_infs.items():
          for line in inf:
            d = json.loads(line.decode())
            user = self.get_user(d)
            userid = user['id_str']
            user_splits[userid] = split
            label = user['label']
            weight = user.get("confidence", 1.0)
            if split is None or label is None:
              skipped += 1
              continue

            features = {'userid': userid, 'name': user['name'],
                        'label': label, 'weight': weight}
            profile_features = extract_features(user)
            profile_features = transform_features(self.transformers, profile_features)
            features.update(profile_features)

            profile_dataset[userid] = features

        print("skipped {} profile-only users".format(skipped))

        for i, inf in enumerate(unigram_infs):
          for line in inf:
            d = json.loads(line.decode())
            userid = d['userid']
            if userid not in profile_dataset:
              skipped += 1
              continue
            split = user_splits[userid]

            features = profile_dataset.pop(userid)
            features['unigrams'] = d['unigrams']

            outfs[split].write("{}\n".format(json.dumps(features)).encode('utf8'))

        print("skipped {} profile+unigram users".format(skipped))

        for userid, features in profile_dataset.items():
          split = user_splits[userid]
          features['unigrams'] = []

          outfs[split].write("{}\n".format(json.dumps(features)).encode('utf8'))

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

    self._vocab = SymbolTable()
    self._labels = SymbolTable()

    # Create symbol table on training data
    infn = os.path.join(self.work, self.setup_files[0])
    with gzip.open(infn) as inf:
      for line in inf:
        try:
          d = json.loads(line.decode().rstrip())
        except Exception as e:
          print(line, str(e))
          continue
        self._labels.add(d['label'])
        length = 0
        for token in d['name']:
          self._vocab.add(token)
          length += 1
        for _ in range(Baseline.MAX_LENGTH - length):
          self._vocab.add(Baseline.PAD)
        self._lengths.append(length)

    # Freeze symbol tables
    self._vocab.freeze(unk=Baseline.UNK)
    self._labels.freeze()
    with gzip.open(vocab_path, "w") as outf:
      obj = SymbolTable.to_json(self._vocab)
      outf.write("{}\n".format(json.dumps(obj)).encode('utf8'))
      obj = SymbolTable.to_json(self._labels)
      outf.write("{}\n".format(json.dumps(obj)).encode('utf8'))

  def _encode_name(self, name):
    return [self._vocab.idx(char) for char in name]

  def get_user(self, d):
    if 'user' in d:
      return d['user']
    else:
      return d

  def _write_json(self):
    assert self._vocab.frozen, "Vocab must be frozen before writing json"

    for i in range(len(self.json_files)):
      infn = os.path.join(self.work, self.setup_files[i])
      outfn = os.path.join(self.work, self.json_files[i])
      with gzip.open(infn) as inf, gzip.open(outfn, 'w') as outf:
        for line in inf:
          d = json.loads(line.decode().rstrip())
          d['label'] = self._labels.idx(d['label'])
          tokens = d.pop('name')
          if self.setup_type in ['profile', 'both']:
            tokens = self._encode_name(tokens)
            tokens = tokens[:Baseline.MAX_LENGTH]
            length = len(tokens)
            d['length'] = length
            tokens += [self._vocab.idx(Baseline.PAD)
                       for i in range(Baseline.MAX_LENGTH - length)]
            d['tokens'] = tokens
          if self.setup_type == 'profile':
            d.pop('unigrams')

          outf.write("{}\n".format(json.dumps(d)).encode('ascii'))

  def json_ready(self):
    return all([os.path.exists(os.path.join(self.work, split))
                for split in self.json_files])

  def _setup_files_ready(self):
    return all([os.path.exists(os.path.join(self.work, split))
                for split in self.setup_files])

  def yield_json(self, json_index):
    fn = os.path.join(self.work, self.json_files[json_index])
    with gzip.open(fn, 'r') as inf:
      try:
        for i, line in enumerate(inf):
          yield json.loads(line.decode().rstrip())
      except OSError as e:
        if i <= 1:
          raise e
        else:
          logging.warn("baseline_dataset.py:yield_json:{}".format(str(e)))

  @property
  def train(self):
    return self.yield_json(0)

  @property
  def labeled(self):
    return self.yield_json(0)

  @property
  def unlabeled(self):
    return []

  @property
  def dev(self):
    return self.yield_json(1)

  @property
  def test(self):
    return self.yield_json(2)

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
  # for setup in ['both', 'profile', 'unigrams']:
  for setup in ['profile']:
    d = Baseline(setup, balance_dev=True, balance_test=True)
    print("vocab_size: {}".format(len(d.vocab)))
    lengths = d.lengths
    if len(lengths) > 0:
      print("Lengths: mean is {}, median is {}, 90th is {} 95th is {}, max is {}".format(
          np.mean(lengths), np.median(lengths),
          np.percentile(lengths, 90), np.percentile(lengths, 95),
          np.max(lengths)))
