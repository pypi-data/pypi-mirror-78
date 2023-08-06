import os
import json
import sys

import numpy as np

from demographer.utils import tf
from demographer.demographer import Demographer
from demographer.tflm import SymbolTable
from demographer.naacl_twitter import NaaclTwitter


class NeuralEthnicityDemographer(Demographer):
  name_key = 'ethnicity'

  def __init__(self, model_dir=None, dtype='n'):
    """Initalizes a class for an Ethnicity neural classifier

    Constructor needs to load a classifier from tensorflow

    Args:
        model_dir: where does the model live?

    """
    # TODO wb vs wlb?
    self.dtype = dtype
    if not model_dir:
      base_dir = os.path.dirname(sys.modules[__package__].__file__)
      model_dir = os.path.join(base_dir, 'models', 'wb_neural')

    assert tf is not None
    self.graph = tf.Graph()
    with self.graph.as_default():
      saver = tf.train.import_meta_graph(os.path.join(model_dir, 'model-0.meta'),
                                         clear_devices=True)
      self.sess = tf.Session()
      saver.restore(self.sess, os.path.join(model_dir, 'model-0'))

      self.inputs = self.graph.get_tensor_by_name('inputs:0')
      self.logits = self.graph.get_tensor_by_name('logits:0')

    with open(os.path.join(model_dir, "vocab.json"), "r") as inf:
      obj = json.loads(inf.readline())
      self._vocab = SymbolTable.from_json(obj)
      self._pad = NaaclTwitter.PAD
      self._split = NaaclTwitter.SPLIT
      self._max_name_length = 32  # this was set dynamically by data length

    with open(os.path.join(model_dir, "labels.json"), "r") as inf:
      obj = json.loads(inf.readline())
      self._labels = SymbolTable.from_json(obj)

  def encode(self, name, screen=None):
    tokens = self._encode(name)
    if screen is not None:
      tokens.append(self._vocab.idx(self._split))
      tokens += self._encode(screen)
    tokens += [self._vocab.idx(self._pad)
               for i in range(self._max_name_length - len(tokens))]
    return tokens[:self._max_name_length]

  def _encode(self, name):
    return [self._vocab.idx(char) for char in name]

  def process_tweet(self, tweet):
    if 'user' in tweet:
        user_info = tweet.get('user')
    else:
        user_info = tweet

    name_string = user_info.get('name')
    if self.dtype == 'ns':
      screen_string = user_info.get('screen')
    else:
      screen_string = None

    # get logits from saved model
    inputs = self.encode(name_string, screen_string)
    inputs = np.expand_dims(inputs, 0)
    logits = self.sess.run(self.logits, {self.inputs: inputs})
    logits = np.squeeze(logits)

    # find probabilities over labels
    label_probs = {}
    logits_sum = np.sum(logits)
    for label_i in range(len(self._labels)):
      label = self._labels._i2v[str(label_i)]
      label_probs[label] = logits[label_i] / logits_sum
    prediction = self._labels._i2v[str(np.argmax(logits))]

    result = {"value": prediction,
              "name": "ethnicity",
              "annotator": "Neural Ethnicity Classifier",
              "scores": label_probs}
    return {self.name_key: result}


if __name__ == "__main__":
  d = NeuralEthnicityDemographer()
  print(d.process_tweet({"name": "Zach Wood-Doughty"}))
