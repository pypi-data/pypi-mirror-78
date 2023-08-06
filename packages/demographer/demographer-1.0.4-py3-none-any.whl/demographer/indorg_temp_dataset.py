import os
import sys
import json
import random

# import numpy as np

from demographer.tflm import SymbolTable

from demographer.transformer_indorg import extract_features
from demographer.transformer_indorg import transform_features
from demographer.transformer_indorg import load_transformers
# from demographer.transformer_indorg import Transformer


class TempHumanizrNames:
  MAX_LENGTH = 32
  PAD = "&pad;"

  def __init__(self, input_fn, work_dir=None, model_dir=None):
    self.transformers = load_transformers()
    self.raw_tweets = input_fn
    self.work, input_fn = os.path.split(os.path.realpath(input_fn))

    # allow override if input_fn in read-only dir
    if work_dir is not None:
      self.work = work_dir

    if model_dir is not None:
      self.model_dir = model_dir
    else:
      dir = os.path.dirname(sys.modules[__package__].__file__)
      self.model_dir = os.path.join(dir, 'models', 'indorg_neural')

    self.preprocess1 = os.path.join(self.work, input_fn[:-4] + 'tmp1.json')
    self.preprocess2 = os.path.join(self.work, input_fn[:-4] + 'tmp2.json')
    self.setup()

  def setup(self):
    if not os.path.exists(self.raw_tweets):
      raise ValueError("need to download data: {}".format(self.raw_tweets))

    with open(self.raw_tweets, "r") as inf:
      with open(self.preprocess1, "w") as outf:
        for line in inf:
          d = json.loads(line.rstrip())
          tweet_id = int(d['id_str'])
          user = self.get_user(d)
          # userid = user['id']

          features = {'id': tweet_id, 'name': user['name']}
          meta_features = extract_features(user)
          meta_features = transform_features(self.transformers, meta_features)
          features.update(meta_features)

          outf.write("{}\n".format(json.dumps(features)))

    self._load_vocab()
    self._load_labels()

    self._write_json()

    self._rng = random.Random()
    self._rng.seed(42)

  def _load_vocab(self):
    with open(os.path.join(self.model_dir, "indorg_vocab.json"), "r") as inf:
      obj = json.loads(inf.readline())
      self._vocab = SymbolTable.from_json(obj)

  def _load_labels(self):
    with open(os.path.join(self.model_dir, "indorg_labels.json"), "r") as inf:
      obj = json.loads(inf.readline())
      self._labels = SymbolTable.from_json(obj)

  # def _build_vocab(self):
  #   self._vocab = SymbolTable()
  #   self._labels = SymbolTable()

  #   # Create symbol table on training data
  #   infn = os.path.join(self.work, self.setup_files[0])
  #   with open(infn, encoding='utf8') as inf:
  #     for line in inf:
  #       try:
  #         d = json.loads(line.rstrip())
  #       except Exception as e:
  #         print(line, str(e))
  #         continue
  #       length = 0
  #       for token in d['name']:
  #         self._vocab.add(token)
  #         length += 1
  #       for _ in range(TempHumanizrNames.MAX_LENGTH - length):
  #         self._vocab.add(TempHumanizrNames.PAD)
  #       self._lengths.append(length)

  #   # Freeze symbol tables
  #   self._vocab.freeze(unk=TempHumanizrNames.UNK)
  #   self._labels.freeze()

  def _encode_name(self, name):
    return [self._vocab.idx(char) for char in name]

  def get_user(self, d):
    if 'user' in d:
      return d['user']
    else:
      return d

  def _write_json(self):
    assert self._vocab.frozen, "Vocab must be frozen before writing json"

    infn = self.preprocess1
    outfn = self.preprocess2
    with open(infn) as inf, open(outfn, 'w') as outf:
      for line in inf:
        d = json.loads(line.rstrip())
        tokens = self._encode_name(d.pop('name'))
        tokens = tokens[:TempHumanizrNames.MAX_LENGTH]
        length = len(tokens)
        d['length'] = length
        tokens += [self._vocab.idx(TempHumanizrNames.PAD)
                   for i in range(TempHumanizrNames.MAX_LENGTH - length)]
        d['tokens'] = tokens
        outf.write("{}\n".format(json.dumps(d)))

  def yield_json(self):
    fn = self.preprocess2
    with open(fn, 'r', encoding='utf8') as inf:
      for line in inf:
        yield json.loads(line.rstrip())

  @property
  def test(self):
    return self.yield_json()

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
  d = TempHumanizrNames('small.json')
  for obj in d.test:
    print(obj)
