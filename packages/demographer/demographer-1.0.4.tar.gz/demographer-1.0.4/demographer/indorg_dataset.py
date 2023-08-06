import os
import sys
import json
import gzip
import random

import numpy as np

from demographer.tflm import SymbolTable

from demographer.transformer_indorg import extract_profile_features
from demographer.transformer_indorg import transform_features
from demographer.transformer_indorg import load_transformers


class HumanizrNames:

  MAX_LENGTH = 32
  PAD = "&pad;"
  UNK = "&unk;"

  def link_paths(self):
    raw = {
        "balanced_splits": "balanced/",
        "full_splits": "full/",
        "hum_full_splits": "hum_full/",
        "hum_balanced_splits": "hum_balanced/",
        "orgs": "all_orgs.txt",
        "inds": "all_inds.txt",
        "raw_data": "raw.json.gz"
    }

    for attr_name, path in raw.items():
      assert os.path.exists(os.path.join(self.work, path))
      setattr(self, attr_name, os.path.join(self.work, path))

  def __init__(self, setup='full', train_balance_ratio=1.):
    self._lengths = []
    base_dir = os.path.dirname(sys.modules[__package__].__file__)
    self.work = os.path.join(base_dir, 'models', 'indorg_neural', 'tmp')

    self.link_paths()

    if setup == 'balanced':
      splits_dir = self.balanced_splits
    elif setup == 'full':
      splits_dir = self.full_splits
    elif setup == 'humanizr_full':
      splits_dir = self.hum_full_splits
    elif setup == 'humanizr_balanced':
      splits_dir = self.hum_balanced_spLITS
    else:
      raise ValueError("Unknown setup: {}".format(setup))
    self.suffix = ".{}.{}".format(setup, train_balance_ratio)

    names = ("train", "dev", "test")
    self.setup_files = ['{}{}.tmp.json'.format(name, self.suffix) for name in names]
    self.json_files = ['{}{}.json'.format(name, self.suffix) for name in names]
    self.transformers = load_transformers()
    self.splits = {}

    self.label_map = {}
    with open(self.orgs) as inf:
      for line in inf:
        self.label_map[int(line.rstrip())] = "org"

    print("Dataset see {} orgs".format(len(self.label_map)))

    with open(self.inds) as inf:
      for line in inf:
        if int(line.rstrip()) in self.label_map:
          raise ValueError("Doubly labeled id {}".format(line.rstrip()))
        self.label_map[int(line.rstrip())] = "ind"

    num_train_orgs = 0
    for split in names:
      splitfn = os.path.join(splits_dir, "{}.txt".format(split))
      with open(splitfn) as inf:
        for line in inf:
          userid = int(line.rstrip())
          # Skip train individuals for now
          if split != 'train':
            self.splits[userid] = split
          elif self.label_map.get(userid) == "org":
            self.splits[userid] = split
            num_train_orgs += 1

    print("added {} organizations to train set".format(num_train_orgs))

    # Now add in train individuals
    with open(os.path.join(splits_dir, "train.txt")) as inf:
      count = 0
      for line in inf:
        userid = int(line.rstrip())
        # Now we add train individuals
        if self.label_map.get(userid) == "ind":
          self.splits[userid] = "train"
          count += 1
          if count > (num_train_orgs * train_balance_ratio):
            break

    print("added {} individuals to train set".format(count))
    self.names = names
    self.setup()

  def setup(self):

    if not os.path.exists(os.path.join(self.work, self.raw_data)):
      raise ValueError("need to download data")

    if not self._setup_files_ready():

      for setup_file in self.setup_files:
        setup_path = os.path.join(self.work, setup_file)
        if os.path.exists(setup_path):
          os.remove(setup_path)
      skipped = 0
      with gzip.open(os.path.join(self.work, self.raw_data), "rt") as inf:
        for line in inf:
          d = json.loads(line.rstrip())
          user = self.get_user(d)
          userid = user['id']
          split = self.splits.get(userid)
          label = self.label_map.get(userid)
          if split is None or label is None:
            skipped += 1
            continue

          features = {'name': user['name'], 'label': label}
          meta_features = extract_profile_features(user)
          meta_features = transform_features(self.transformers, meta_features)
          features.update(meta_features)

          outfn = os.path.join(
              self.work, self.setup_files[self.names.index(split)])
          with open(outfn, "a", encoding='utf8') as outf:
            outf.write("{}\n".format(json.dumps(features)))

        # print("skipped {} users".format(skipped))

    self._build_vocab()

    if not self.json_ready():
      self._write_json()

    self._rng = random.Random()
    self._rng.seed(42)

  def _build_vocab(self):

    base_dir = os.path.dirname(sys.modules[__package__].__file__)
    model_dir = os.path.join(base_dir, 'models', 'indorg_neural')
    vocab_fn = os.path.join(model_dir, "indorg_vocab.json")
    labels_fn = os.path.join(model_dir, "indorg_labels.json")

    if os.path.exists(vocab_fn) and os.path.exists(labels_fn):
      with open(vocab_fn, "r") as inf:
        obj = json.loads(inf.readline())
        self._vocab = SymbolTable.from_json(obj)
        self._pad = HumanizrNames.PAD
        self._max_name_length = HumanizrNames.MAX_LENGTH

      with open(labels_fn, "r") as inf:
        obj = json.loads(inf.readline())
        self._labels = SymbolTable.from_json(obj)

    else:  # need to build vocab and labels
      self._vocab = SymbolTable()
      self._labels = SymbolTable()

      # Create symbol table on training data
      infn = os.path.join(self.work, self.setup_files[0])
      with open(infn, encoding='utf8') as inf:
        for line in inf:
          try:
            d = json.loads(line.rstrip())
          except Exception as e:
            print(line, str(e))
            continue
          self._labels.add(d['label'])
          length = 0
          for token in d['name']:
            self._vocab.add(token)
            length += 1
          for _ in range(HumanizrNames.MAX_LENGTH - length):
            self._vocab.add(HumanizrNames.PAD)
          self._lengths.append(length)

      # Freeze symbol tables
      self._vocab.freeze(unk=HumanizrNames.UNK)
      self._labels.freeze()

      with open(vocab_fn, "w") as outf:
        obj = json.dumps(SymbolTable.to_json(self._vocab))
        outf.write(obj)
      with open(labels_fn, "w") as outf:
        obj = json.dumps(SymbolTable.to_json(self._labels))
        outf.write(obj)

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
      with open(infn) as inf, open(outfn, 'w') as outf:
        for line in inf:
          d = json.loads(line.rstrip())
          d['label'] = self._labels.idx(d['label'])
          tokens = self._encode_name(d.pop('name'))
          tokens = tokens[:HumanizrNames.MAX_LENGTH]
          length = len(tokens)
          d['length'] = length
          tokens += [self._vocab.idx(HumanizrNames.PAD)
                     for i in range(HumanizrNames.MAX_LENGTH - length)]
          d['tokens'] = tokens
          outf.write("{}\n".format(json.dumps(d)))

  def json_ready(self):
    return all([os.path.exists(os.path.join(self.work, split))
                for split in self.json_files])

  def _setup_files_ready(self):
    return all([os.path.exists(os.path.join(self.work, split))
                for split in self.setup_files])

  def yield_json(self, json_index):
    fn = os.path.join(self.work, self.json_files[json_index])
    with open(fn, 'r', encoding='utf8') as inf:
      for line in inf:
        yield json.loads(line.rstrip())

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
  d = HumanizrNames('full', 5.0)
  print("vocab_size: {}".format(len(d.vocab)))
  lengths = d.lengths
  if len(lengths) > 0:
    print("Lengths: mean is {}, median is {}, 90th is {} 95th is {}, max is {}".format(
        np.mean(lengths), np.median(lengths),
        np.percentile(lengths, 90), np.percentile(lengths, 95),
        np.max(lengths)))

  # with open("indorg_vocab.json", "w") as outf:
  #   outf.write(json.dumps(SymbolTable.to_json(d.vocab)))
  # with open("indorg_labels.json", "w") as outf:
  #   outf.write(json.dumps(SymbolTable.to_json(d.labels)))
