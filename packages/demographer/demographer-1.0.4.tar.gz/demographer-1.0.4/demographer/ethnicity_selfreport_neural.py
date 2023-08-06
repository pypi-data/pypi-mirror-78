# import pdb; pdb.set_trace()

import os
import sys
import json

import numpy as np

from demographer.utils import tf
from demographer.tflm import SymbolTable

from demographer.transformer_indorg import transform_features
from demographer.transformer_selfreport import load_transformers
from demographer.transformer_selfreport import extract_features
from demographer.combo_dataset import ComboDataset

from demographer.demographer import Demographer
from demographer.utils import download_pretrained_models, softmax


class EthSelfReportNeuralDemographer(Demographer):
  name_key = 'eth_selfreport_neural'

  def __init__(self, balanced=True, rebalance=False, model_dir=None):
    """Initalizes a class for a race/ethnicity neural classifier

    Constructor needs to load a classifier from tensorflow

    Args:
        model_dir: where does the model live?

    """
    if balanced:
      self.model_prefix = 'balanced'
    else:
      self.model_prefix = 'imbalanced_rebalance' if rebalance else 'imbalanced'

    if model_dir is None:
      base_dir = os.path.dirname(sys.modules[__package__].__file__)
      model_dir = os.path.join(base_dir, 'models', 'ethnicity_selfreport')
      if not os.path.exists(model_dir):
        assert download_pretrained_models(os.path.join(base_dir, 'models'), 'ethnicity_selfreport')

    self.graph = tf.Graph()
    with self.graph.as_default():
      saver = tf.train.import_meta_graph(
          os.path.join(model_dir, '{}.meta'.format(self.model_prefix)),
          clear_devices=True)
      self.sess = tf.Session()
      saver.restore(self.sess, os.path.join(model_dir, self.model_prefix))

      self.tokens = self.graph.get_tensor_by_name('tokens:0')
      self.meta = self.graph.get_tensor_by_name('meta:0')
      self.logits = self.graph.get_tensor_by_name('logits:0')

    with open(os.path.join(model_dir, "eth_vocab.json"), "r") as inf:
      obj = json.loads(inf.readline())
      self._vocab = SymbolTable.from_json(obj)
      self._pad = ComboDataset.PAD
      self._max_name_length = ComboDataset.MAX_LENGTH

    with open(os.path.join(model_dir, "eth_labels.json"), "r") as inf:
      obj = json.loads(inf.readline())
      self._labels = SymbolTable.from_json(obj)

    self._transformers = load_transformers()

  def encode_name(self, name):

    tokens = [self._vocab.idx(char) for char in name]
    tokens = tokens[:ComboDataset.MAX_LENGTH]
    length = len(tokens)
    tokens += [self._vocab.idx(ComboDataset.PAD)
               for i in range(ComboDataset.MAX_LENGTH - length)]
    return tokens

  def process_tweet(self, tweet):
    if 'user' in tweet:
        user_info = tweet.get('user')
    else:
        user_info = tweet

    name_string = user_info.get('name')
    tokens = self.encode_name(name_string)
    tokens = np.expand_dims(tokens, 0)

    meta_dict = extract_features(user_info)
    meta_dict = transform_features(self._transformers, meta_dict)
    meta_features = []
    for key in [
        "friends_count", "followers_count", "ratio", "listed_count",
        "statuses_count", "verified", "tweets_per_month", "months"
    ]:
      meta_features.append(float(meta_dict.get(key, 0.) or 0.))
    meta_features = np.array(meta_features)
    meta_features = np.expand_dims(meta_features, 0)

    logits = self.sess.run(
        self.logits, feed_dict={self.tokens: tokens, self.meta: meta_features})
    logits = softmax(np.squeeze(logits))

    # find probabilities over labels
    label_probs = {}
    for label_i in range(len(self._labels)):
      label = self._labels._i2v[str(label_i)]
      label_probs[label] = logits[label_i]
    prediction = self._labels._i2v[str(np.argmax(logits))]

    result = {"value": prediction,
              "name": "eth_selfreport",
              "setup": self.model_prefix,
              "annotator": "Neural Self-Report Ethnicity Classifier",
              "scores": label_probs}
    return {self.name_key: result}


if __name__ == "__main__":
  tweets = [
      {"name": "Zach Wood-Doughty", "screen_name": "zachwooddoughty", "location": None, "url": None, "description": "PhD student at @JHUCLSP", "protected": False, "verified": False, "followers_count": 76, "friends_count": 89, "listed_count": 6, "favourites_count": 367, "statuses_count": 3013, "created_at": "Thu Dec 24 17:07:51 +0000 2015", },  # noqa
      {"name": "ESPN", "screen_name": "ESPN", "location": "Sports", "url": "espn.com", "description": "Best place to follow all your favorite news websites", "protected": False, "verified": True, "followers_count": 10000000, "friends_count": 42, "listed_count": 1235, "favourites_count": 123, "statuses_count": 20013, "created_at": "Thu Dec 24 17:07:51 +0000 2012", }  # noqa
  ]
  balanced = EthSelfReportNeuralDemographer(balanced=True)
  for tweet in tweets:
    print(balanced.process_tweet(tweet))
