import json
import gzip
import inspect
import os
import logging

import numpy as np

# Try to import tensorflow requirements, otherwise fail gracefully and expect
#   the command-line checks to avoid an attribute error
try:
  import tensorflow as tf
  import absl.flags
except ImportError:
  tf = None

PRETRAINED_MODEL_ARCHIVE_MAP = {
  'ethnicity_selfreport': None,
  'ethnicity_selfreport_bert': None,
  'wb_simple': None,
  'indorg_neural': 'https://bitbucket.org/mdredze/demographer/downloads/indorg_neural.tar.gz',
  'mw_neural': 'https://bitbucket.org/mdredze/demographer/downloads/mw_neural.tar.gz',
  'mw_simple': 'https://bitbucket.org/mdredze/demographer/downloads/mw_simple.tar.gz',
  'indorg_simple': 'https://bitbucket.org/mdredze/demographer/downloads/indorg_simple.tar.gz',
}

logger = logging.getLogger(__name__)


class NumpySerializer(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, np.integer):
      return int(obj)
    elif isinstance(obj, np.floating):
      return float(obj)
    elif isinstance(obj, np.ndarray):
      return obj.tolist()
    elif tf is not None and isinstance(obj, absl.flags._flag.Flag):
      return obj.value
    else:
      # return super(NumpySerializer, self).default(obj)
      return super().default(obj)


def sgd_classifier_to_json(classifier):
  args_dict = {}
  needed_args = inspect.signature(type(classifier).__init__).parameters.keys()
  for key in needed_args:
    if hasattr(classifier, key):
      args_dict[key] = getattr(classifier, key)
  params_dict = {}
  for key in ['classes_', 'coef_', 'intercept_', 't_']:
    if hasattr(classifier, key):
      params_dict[key] = getattr(classifier, key)

  full_dict = {'args': args_dict, 'params': params_dict}
  return json.dumps(full_dict, cls=NumpySerializer)


def sgd_classifier_from_json(cls, full_json):
  full_dict = json.loads(full_json)
  needed_args = inspect.signature(cls.__init__).parameters.keys()
  args = {key: val for key, val in full_dict['args'].items()
          if key in needed_args}
  new_classifier = cls(**args)
  for key in full_dict['params']:
    setattr(new_classifier, key, np.array(full_dict['params'][key]))

  return new_classifier


def hasher_from_json(cls, full_json):
  full_dict = json.loads(full_json)
  needed_args = inspect.signature(cls.__init__).parameters.keys()
  args = {key: val for key, val in full_dict.items()
          if key in needed_args}
  return cls(**args)


def download_pretrained_models(tmp_model_path, model_name):
  assert model_name in PRETRAINED_MODEL_ARCHIVE_MAP
  url = PRETRAINED_MODEL_ARCHIVE_MAP[model_name]
  logger.warn('Pretrained model does not exist.')
  if not url:
    err_msg = 'You need to fill out data use agreement to download {}. Please visit http://www.cs.jhu.edu/~mdredze/demographics-training-data/ and contact the authors.'.format(model_name)  # NOQA
    logger.error(err_msg)
    raise IOError(err_msg)

  logger.info('Downloading models for {} from {}'.format(model_name, url))
  if not os.path.isdir(tmp_model_path):
    os.mkdir(tmp_model_path)

  model_tgz = os.path.join(tmp_model_path, '{}.tar.gz'.format(model_name))
  os.system('wget -O {fn} {url}'.format(fn=model_tgz, url=url))

  if os.path.exists(model_tgz):
    print('Extracting downloaded model to {}'.format(tmp_model_path))
    os.system('tar -xzvf {fn} -C {target_dir}'.format(fn=model_tgz, target_dir=tmp_model_path))
    return True
  else:
    logger.info('Download failed. Please retry')
    return False


def softmax(logits):
  max_ = np.max(logits)
  tmp = np.exp(logits - max_)
  return tmp / np.sum(tmp)


def read_tweet_text_from_timeline(user_id, timeline_dir, tweet_limit=200, no_rt=True, lower_text=True):
  with gzip.open(os.path.join(timeline_dir, "{}_statuses.json.gz".format(user_id)), 'r') as inf:
    count = 0
    texts = []
    for line in inf:
      tweet = json.loads(line.decode())
      if 'text' in tweet:
        text = tweet['text']
      elif 'full_text' in tweet:
        text = tweet['full_text']
      else:
        continue
      if lower_text:
        text = text.lower()
      if no_rt and (text.startswith('rt') or tweet.get('retweeted_status') is not None):
        continue
      count += 1
      if count and count > tweet_limit:
        continue
      texts.append(text)
  return {'user_id': user_id, 'texts': texts}
