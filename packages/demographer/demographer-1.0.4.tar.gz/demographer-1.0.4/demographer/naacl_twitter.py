import os
import json
import codecs
import random
import numpy as np

from demographer.tflm import SymbolTable


class NaaclTwitter():
  BASE_DIR = os.path.join("temp_data", "tf_preprocess")
  JSON_FILES = ("pretrain.json", "train.json", "dev.json", "test.json")
  SPLIT = '&split;'
  PAD = "&pad;"
  UNK = "<unk>"

  def __init__(self, task, dtype):
    '''
    task is one of (mw, wb, wlb) for man/woman, white/black, white/latino/black
    dtype is one of (n, n+s) for name-only, name plus screenname
    '''
    taskdir = os.path.join(NaaclTwitter.BASE_DIR, task)
    if not os.path.exists(taskdir):
      os.mkdir(taskdir)
    workdir = os.path.join(taskdir, dtype)
    if not os.path.exists(workdir):
      os.mkdir(workdir)

    fn = "{}_build.txt".format(task)
    self.buildfn = os.path.join(NaaclTwitter.BASE_DIR, fn)

    # fn =  "{}_pretrain.txt".format(task)
    # self.pretrainfn = os.path.join(NaaclTwitter.BASE_DIR, fn)

    self.dtype = dtype
    self.task = task
    self.splits = ['train', 'dev', 'test']
    self._lengths = []
    self.workdir = workdir

    self.setup()

  def setup(self):
    if not os.path.exists(self.buildfn):
      raise IOError("{} does not exist.".format(self.buildfn))

    for split in self.splits:
      splitfn = os.path.join(NaaclTwitter.BASE_DIR,
                             "{}.{}.txt".format(self.task, split))
      if not os.path.exists(splitfn):
        raise IOError("{} does not exist.".format(splitfn))

    self._build_vocab()
    self._set_max_length()

    if not self.json_ready():
      self._build_full_data()
      self._write_json()

    self._rng = random.Random()
    self._rng.seed(42)

  def _build_full_data(self):
    data = {}
    with open(self.buildfn, encoding='utf8') as inf:
      for line in inf:
        name, screen, _, label = line.rstrip('\n').split('\t')
        data[screen.lower()] = (name, screen, label.lower())
    self.full_data = data

  def _build_vocab(self):
    self._vocab = SymbolTable()
    self._screen_vocab = SymbolTable()
    self._labels = SymbolTable()

    # Create symbol table on training data
    with open(self.buildfn, encoding='utf8') as inf:
      for line in inf:
        # throw away description
        name, screen, _, label = line.rstrip('\n').split('\t')
        self._labels.add(label.lower())
        length = 0
        if self.dtype == 'n':
          for token in name:
            length += 1
            self._vocab.add(token)
        elif self.dtype == 'n+s':
          for token in name:
            length += 1
            self._vocab.add(token)
          self._vocab.add(NaaclTwitter.SPLIT)
          for token in screen:
            length += 1
            self._vocab.add(token)
          length += 1
        else:
          raise NotImplementedError("Unknown dtype {}".format(self.dtype))
        self._lengths.append(length)

    # NOTE we don't freeze vocab until after setting max length
    self._labels.freeze()

  def _set_max_length(self):
    print('lengths are mean: {}, median: {}, max: {}'.format(
        np.mean(self._lengths), np.median(self._lengths), np.max(self._lengths)))

    # max_dilation is relevant to CNN models
    max_length = np.max(self._lengths)
    max_dilation = max_length & (~ max_length + 1)
    # NOTE could instead round up to next power of 2:
    #   2 ** int(np.ceil(np.log2(max_length)))
    self.MAX_LENGTH = max(max_length, 2 ** (max_dilation + 1))
    print("max length set to {}".format(self.MAX_LENGTH))

    for length in self._lengths:
      for _ in range(self.MAX_LENGTH - length):
        self._vocab.add(NaaclTwitter.PAD)

    self._vocab.freeze(unk=NaaclTwitter.UNK)

  def _encode(self, name):
    return [self._vocab.idx(char) for char in name]

  def encode(self, name, screen=None):
    tokens = self._encode(name)
    if screen is not None:
      tokens.append(self._vocab.idx(NaaclTwitter.SPLIT))
      tokens += self._encode(screen)
    tokens += [self._vocab.idx(NaaclTwitter.PAD)
               for i in range(self.MAX_LENGTH - len(tokens))]
    return tokens[:self.MAX_LENGTH]

  def _write_json(self):
    assert self._vocab.frozen, "Vocab must be frozen before writing json"

    for split in self.splits:
      splitfn = os.path.join(NaaclTwitter.BASE_DIR,
                             "{}.{}.txt".format(self.task, split))

      outfn = os.path.join(self.workdir, "{}.json".format(split))
      with open(splitfn) as splitf, open(outfn, 'w') as outf:
        for line in splitf:
          label, screen = line.strip().split('\t')
          (name, screen, label) = self.full_data[screen.lower()]

          if self.dtype == 'n':
            screen = None
          tokens = self.encode(name, screen)
          assert len(tokens) == self.MAX_LENGTH
          label_idx = self._labels.idx(label)
          d = {'label': label_idx, 'tokens': tokens}
          if len(d['tokens']) > 0:
            outf.write("{}\n".format(json.dumps(d)))

  def _build_pretrain(self):
    assert self._vocab.frozen, "Vocab must be frozen before writing json"

    outfn = os.path.join(self.workdir, "pretrain.json")
    with open(self.pretrainfn) as inf, open(outfn, 'w') as outf:
      for line in inf:
        label, name = line.strip().split('\t')
        tokens = self._encode(name)
        tokens = tokens[:self.MAX_LENGTH]
        tokens += [self._vocab.idx(NaaclTwitter.PAD)
                   for i in range(self.MAX_LENGTH - len(tokens))]
        assert len(tokens) == self.MAX_LENGTH
        label_idx = self._labels.idx(label)
        d = {'label': label_idx, 'tokens': tokens}
        if len(d['tokens']) > 0:
          outf.write("{}\n".format(json.dumps(d)))

  def json_ready(self):
    return all([os.path.exists(os.path.join(self.workdir, split))
                for split in NaaclTwitter.JSON_FILES])

  @property
  def pretrain(self):
    with codecs.open(os.path.join(self.workdir, 'pretrain.json'),
                     'r', 'utf8') as inf:
      for line in inf:
        yield json.loads(line.rstrip())

  @property
  def train(self):
    with codecs.open(os.path.join(self.workdir, 'train.json'),
                     'r', 'utf8') as inf:
      for line in inf:
        yield json.loads(line.rstrip())

  @property
  def dev(self):
    with codecs.open(os.path.join(self.workdir, 'dev.json'),
                     'r', 'utf8') as inf:
      for line in inf:
        yield json.loads(line.rstrip())

  @property
  def test(self):
    with codecs.open(os.path.join(self.workdir, 'test.json'),
                     'r', 'utf8') as inf:
      for line in inf:
        yield json.loads(line.rstrip())

  @property
  def rng(self):
    return self._rng

  @property
  def labels(self):
    return self._labels

  @property
  def vocab(self):
    return self._vocab


if __name__ == "__main__":
  NaaclTwitter('mw', 'n')
