import os
import re
import sys
import gzip
import json
import logging

import numpy as np

from datetime import datetime
from collections import defaultdict

from demographer.transformer import Transformer


def get_user(d):
  if 'user' in d:
    return d['user']
  return d


def extract_name_features(name_and_screenname):
  """Extract features from screenname and name.

  Make sure to delete the json files
    if you make changes to feature extraction method

  Args:
    name_and_screenname: Combined name and screenname split by a space
      Eg. Johns Hopkins U. johnshopkinsu


  Returns:
    features: A dictionary of features, extracted using both screenname and name
  """
  screenname = str(name_and_screenname.split(" ")[-1])
  name = " ".join(name_and_screenname.split(" ")[:-1])
  if screenname.strip() == "":
    screenname = name.strip().replace(" ", "")
  lower_screenname = screenname.lower()
  features = {}
  if not screenname:
    return {}

  # If screenname or name has a numeric character
  if re.search(r'[0-9]+', screenname) is not None:
    features['screen_alphanum'] = 1
  if re.search(r'[0-9]+', name) is not None:
    features['name_alphanum'] = 1

  # If screenname has a special (non-ASCII) character
  if re.search(r'[^\x00-\x7F]', lower_screenname) is not None:
    features['has_special_char'] = 1

  # Match capital letters in name and screenname
  # In "Some page USA", it matches USA
  matches = re.findall(r'[A-Z]+\b', name)
  match_capitals_name = set([i if len(i) < 5 else i[:4] for i in matches])
  for i in match_capitals_name:
    features["capitals_name_{}={}".format(len(i), i)] = 1

  matches = re.findall(r'[A-Z]+\b', name)
  match_capitals_name = set([i if len(i) < 5 else i[:4] for i in matches])
  for i in match_capitals_name:
    features["capitals_name_{}={}".format(len(i), i)] = 1

  # In "walmartUSA", it matches USA
  matches = re.findall(r'[A-Z]+\b', screenname)
  match_capitals_screename = set([i if len(i) < 5 else i[:4] for i in matches])
  for i in match_capitals_screename:
    features["capitals_screen_name_{}={}".format(len(i), i)] = 1

  # In TedTalk matches ted and talk
  matches = re.findall(r'[A-Z][a-z]+', screenname)
  match_capitalized_screenname = set(
      [i if len(i) < 5 else i[:4] for i in matches])

  for i in match_capitalized_screenname:
    features["capitalized_screen_name_{}={}".format(len(i), i.lower())] = 1

  # First and last n-grams from screename.
  features['last_letter=%s' % lower_screenname[-1]] = 1
  features['first_letter=%s' % lower_screenname[0]] = 1

  if len(screenname) > 1:
    features['first_2=%s' % lower_screenname[:2]] = 1
    features['last_2=%s' % lower_screenname[-2:]] = 1
  if len(screenname) > 2:
    features['first_3=%s' % lower_screenname[:3]] = 1
    features['last_3=%s' % lower_screenname[-3:]] = 1
  if len(screenname) > 3:
    features['first_4=%s' % lower_screenname[:4]] = 1
    features['last_4=%s' % lower_screenname[-4:]] = 1

  # Create feature for starting with a vowel/number/consonant
  if lower_screenname[0] in 'aeiou':
    features['starts_vowel'] = 1
  elif lower_screenname[0] in '0123456789':
    features['starts_number'] = 1
  else:
    features['starts_consonant'] = 1

  if lower_screenname[-1] in 'aeiou':
    features['ends_vowel'] = 1
  elif lower_screenname[-1] in '0123456789':
    features['ends_number'] = 1
  else:
    features['ends_consonant'] = 1

  # First and last n grams from name
  # Break the screen name into words and create individual features for all those features

  for i, word in enumerate(filter(lambda x: x, name.split(" "))):
    word = word.lower()
    features['w{0}_last_letter={1}'.format(i, word[-1])] = 1
    features['w{0}_first_letter={1}'.format(i, word[0])] = 1

    if re.search(r'[0-9]+', word) is not None:
      features['w{0}_has_num'.format(i)] = 1
    if len(word) > 1:
      features['w{0}_first_2={1}'.format(i, word[:2])] = 1
      features['w{0}_last_2={1}'.format(i, word[-2:])] = 1
    if len(word) > 2:
      features['w{0}_first_3={1}'.format(i, word[:3])] = 1
      features['w{0}_last_3={1}'.format(i, word[-3:])] = 1
    if len(word) > 3:
      features['w{0}_first_4={1}'.format(i, word[:4])] = 1
      features['w{0}_last_4={1}'.format(i, word[-4:])] = 1

    if not word[0].isalnum():
      features['w{0}_starts_char'.format(i)] = 1
    elif word[0] in 'aeiou':
      features['w{0}_starts_vowel'.format(i)] = 1
    elif word[0] in '0123456789':
      features['w{0}_starts_number'.format(i)] = 1
    else:
      features['w{0}_starts_consonant'.format(i)] = 1

    if not word[-1].isalnum():
      features['w{0}_ends_char'.format(i)] = 1
    elif word[-1] in 'aeiou':
      features['w{0}_ends_vowel'.format(i)] = 1
    elif word[-1] in '0123456789':
      features['w{0}_ends_number'.format(i)] = 1
    else:
      features['w{0}_ends_consonant'.format(i)] = 1

    features['w{0}={1}'.format(i, word)] = 1

  return features


def extract_profile_features(user):
  features = {}
  if not user:
    return {}

  features['friends_count'] = user.get('friends_count')
  features['followers_count'] = user.get('followers_count')
  if features['friends_count'] is None or features['followers_count'] is None:
    features['ratio'] = None
  else:
    features['ratio'] = user.get('followers_count') / float(max(1, user.get('friends_count')))
  features['listed_count'] = user.get('listed_count')
  features['statuses_count'] = user.get('statuses_count')

  descr_length = len(user.get('description', '') or '')
  features['descr_high'] = descr_length

  pronoun_count = 0
  collective_count = 0
  personal_pronouns = ['my', 'i', 'me', 'i\'m', 'i\'ll', 'mine']
  collective_pronouns = ['we', 'our', 'us', 'we\'ll', 'we\'ve', 'ours']

  try:
    words = re.split(r"\W+", user.get('description') or '')
  except Exception as e:
    logging.debug(e)
    words = []
  for word in words:
    if word.lower() in personal_pronouns:
      pronoun_count += 1
    if word.lower() in collective_pronouns:
      collective_count += 1

  features['collective_count'] = collective_count
  features['pronoun_count'] = pronoun_count

  repetitive_punc = r'(\!|\"|\#|\$|\%|\&|\'|\(|\)|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{|\|\|}\|\~){2,}'  # noqa
  try:
    rep_punc = len(re.findall(repetitive_punc, user.get('description') or ''))
  except Exception as e:
    logging.debug(e)
    rep_punc = 0
  features['rep_punc'] = rep_punc

  features['verified'] = int(user.get('verified', 0))

  try:
    d1 = datetime.now()
    d2 = datetime.strptime(user['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    diff = (d1.year - d2.year) * 12 + d1.month - d2.month

    tweets_per_month = user.get('statuses_count', 0) / float(diff)
    features['tweets_per_month'] = tweets_per_month
    features['months'] = diff
  except Exception as e:
    logging.debug(e)
    features['tweets_per_month'] = None
    features['months'] = None

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
  infn = "/export/c10/zach/data/humanizr/raw.json.gz"
  features = defaultdict(list)
  with gzip.open(infn, 'rt') as inf:
    for line in inf:
      obj = json.loads(line.rstrip())
      user = get_user(obj)
      user_features = extract_profile_features(user)
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


def load_transformers(model, fn=None):
  assert model in ["neural", "simple"]
  if fn is None:
    dir = os.path.dirname(sys.modules[__package__].__file__)
    fn = os.path.join(
        dir, 'models', 'indorg_{}'.format(model), 'indorg_transformer.json')

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
      output[key] = transformers[key].transform(features[key])

  return output


def build_transformers(infn, num_bins, outfn=None):
  ''' Build a Transformer object for each feature, then save to file '''

  # infn = "/export/b20/zach/genseq/datasets/humanizrNames/raw.json.gz"
  features = defaultdict(list)
  with gzip.open(infn, 'rt') as inf:
    for line in inf:
      obj = json.loads(line.rstrip())
      user = get_user(obj)
      user_features = extract_profile_features(user)
      for key in user_features:
        features[key].append(user_features[key])

  transformers = {}
  for key in features:
    t = Transformer(features[key], num_bins)
    transformers[key] = t

  if outfn is None:
    dir = os.path.dirname(sys.modules[__package__].__file__)
    outfn = os.path.join(dir, 'models', 'indorg_simple',
                         'indorg_transformer.json')

  with open(outfn, "w") as outf:
    outf.write(json.dumps(
        {key: val.to_dict() for key, val in transformers.items()}))
