import os
import gzip
import json
import sys

import numpy as np

from datetime import datetime
from collections import defaultdict

from demographer.transformer import Transformer


def get_user(d):
  if 'user' in d:
    return d['user']
  return d


def extract_features(user):
  features = {}
  if not user:
    return {}

  features['friends_count'] = user['friends_count']
  features['followers_count'] = user['followers_count']
  features['ratio'] = user['followers_count'] / float(max(1, user['friends_count']))
  features['listed_count'] = user['listed_count']
  features['statuses_count'] = user['statuses_count']

  features['verified'] = int(user['verified'])

  d1 = datetime.now()
  d2 = datetime.strptime(user['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
  diff = (d1.year - d2.year) * 12 + d1.month - d2.month

  tweets_per_month = user['statuses_count'] / float(diff)
  features['tweets_per_month'] = tweets_per_month
  features['months'] = diff

  return features


def get_stats(vec):
  return [
      min(vec),
      np.percentile(vec, 25),
      np.median(vec),
      np.mean(vec),
      np.std(vec),
      np.percentile(vec, 75),
      max(vec)
  ]


def test():
  infn = "/export/b20/zach/genseq/datasets/humanizrNames/raw.json.gz"
  features = defaultdict(list)
  with gzip.open(infn, 'rt') as inf:
    for line in inf:
      obj = json.loads(line.rstrip())
      user = get_user(obj)
      user_features = extract_features(user)
      for key in user_features:
        features[key].append(user_features[key])

  for key in features:
    # print({type(x): 1 for x in features[key]})
    print(key)
    data = np.array(features[key])
    print(get_stats(data))
    percentiles = [np.percentile(data, x) for x in np.arange(11) * 10]
    hist = np.histogram(data, bins=percentiles)
    print(hist)
    print(hist[0].shape)


def load_transformers(fn=None):
  if fn is None:
    dir = os.path.dirname(sys.modules[__package__].__file__)
    fn = os.path.join(dir, 'models', 'ethnicity_selfreport', 'transformer.json')

  with open(fn) as inf:
    d = json.loads(inf.readline())
    return {key: Transformer(data=None, num_bins=None, from_dict=val)
            for key, val in d.items()}


def transform_features(transformers, features):
  assert type(transformers) == dict
  assert type(features) == dict

  output = features.copy()

  for key in features:
    if key in transformers:
      if features[key] is not None:
        output[key] = transformers[key].transform(features[key])
      else:
        output[key] = -1

  return output


def build_transformers(infn, num_bins, outfn=None):
  ''' Build a Transformer object for each feature, then pickle '''

  if infn is None:
    infn = "/export/b20/zach/genseq/datasets/humanizrNames/raw.json.gz"
  features = defaultdict(list)
  with gzip.open(infn, 'rt') as inf:
    for line in inf:
      obj = json.loads(line.rstrip())
      user = get_user(obj)
      user_features = extract_features(user)
      for key in user_features:
        features[key].append(user_features[key])

  transformers = {}
  for key in features:
    t = Transformer(features[key], num_bins)
    # print(t.edges)
    transformers[key] = t

  if outfn is None:
    dir = os.path.dirname(sys.modules[__package__].__file__)
    outfn = os.path.join(dir, 'models', 'indorg_simple',
                         'indorg_transformer.json')

  with open(outfn, "w") as outf:
    outf.write(json.dumps(
        {key: val.to_dict() for key, val in transformers.items()}))
