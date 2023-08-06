import gzip
import json
import os
import random

import numpy as np

from demographer.tflm import SymbolTable

from demographer.transformer_selfreport import extract_features
from demographer.transformer_selfreport import transform_features
from demographer.transformer_selfreport import load_transformers

VOCAB_PATH = "/export/c10/zach/demographics/models/datasets/noisy/vocab.json.gz"


class EvalDataset:
  MAX_LENGTH = 32
  UNIGRAM_VOCAB = 78066
  PAD = "&pad;"
  UNK = "&unk;"

  def __init__(self, input_file, work_dir, ):
    np.random.seed(42)

    name = ".".join(os.path.split(input_file)[-1].split('.')[:-1])
    self.data = input_file
    self.suffix = name
    self.work = work_dir
    self._lengths = []

    self.setup_file = '{}.tmp.json.gz'.format(name)
    self.json_files = ['{}.json.gz'.format(name)]
    self.transformers = load_transformers()

    self.setup()

  def setup(self):

    if not os.path.exists(self.data):
      raise ValueError("need to download train data to: {}".format(self.data))

    if not self._setup_files_ready():

      setup_path = os.path.join(self.work, self.setup_file)
      if os.path.exists(setup_path):
        os.remove(setup_path)
      skipped = 0

      if self.data.endswith('gz'):
        open_func = gzip.open
      else:
        open_func = open

      with open_func(self.data) as inf:
        with gzip.open(os.path.join(self.work, self.setup_file), "w") as outf:
          for line in inf:
            if open_func == gzip.open:
              line = line.decode()
            d = json.loads(line.rstrip())
            user = self.get_user(d)
            userid = user.get('id_str') or user.get("userid")

            features = {'userid': userid, 'name': user['name'], 'weight': 1.0}
            profile_features = extract_features(user)
            profile_features = transform_features(self.transformers, profile_features)
            features.update(profile_features)

            outf.write("{}\n".format(json.dumps(features)).encode('utf8'))

        print("skipped {} users".format(skipped))

    self._build_vocab()

    if not self.json_ready():
      self._write_json()

    self._rng = random.Random()
    self._rng.seed(42)

  def _build_vocab(self):
    if os.path.exists(VOCAB_PATH):
      with gzip.open(VOCAB_PATH) as inf:
        obj = json.loads(inf.readline().decode())
        self._vocab = SymbolTable.from_json(obj)
        obj = json.loads(inf.readline().decode())
        self._labels = SymbolTable.from_json(obj)

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
    outfn = os.path.join(self.work, self.json_files[0])
    with gzip.open(infn) as inf, gzip.open(outfn, 'w') as outf:
      for line in inf:
        d = json.loads(line.decode().rstrip())
        d['label'] = 0
        tokens = self._encode_name(d.pop('name'))
        tokens = tokens[:EvalDataset.MAX_LENGTH]
        length = len(tokens)
        d['length'] = length
        tokens += [self._vocab.idx(EvalDataset.PAD)
                   for i in range(EvalDataset.MAX_LENGTH - length)]
        d['tokens'] = tokens
        outf.write("{}\n".format(json.dumps(d)).encode('ascii'))

  def json_ready(self):
    return all([os.path.exists(os.path.join(self.work, split))
                for split in self.json_files])

  def _setup_files_ready(self):
    return os.path.exists(os.path.join(self.work, self.setup_file))

  def yield_json(self, json_index):
    fn = os.path.join(self.work, self.json_files[json_index])
    with gzip.open(fn, 'r') as inf:
      for line in inf:
        yield json.loads(line.decode().rstrip())

  # @property
  # def train(self):
  #   return self.yield_json(0)

  # @property
  # def labeled(self):
  #   return self.yield_json(0)

  # @property
  # def unlabeled(self):
  #   return []

  @property
  def dev(self):
    return self.yield_json(0)

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
  fake_dir = "/export/c10/zach/demographics/models/test_eval_data/"
  d = EvalDataset(os.path.join(fake_dir, 'faketweets.txt'), fake_dir)
  print("vocab_size: {}".format(len(d.vocab)))
  print("{} examples".format(len(list(d.dev))))
