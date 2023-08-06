from __future__ import division

import os
import json
import re
import sys
import random
import logging
import csv
from collections import defaultdict

from demographer.demographer import Demographer
from demographer.utils import sgd_classifier_from_json
from demographer.utils import hasher_from_json
from demographer.utils import sgd_classifier_to_json
from demographer.utils import NumpySerializer
from demographer.utils import download_pretrained_models

from sklearn.feature_extraction import FeatureHasher
from sklearn.linear_model import SGDClassifier


class CensusGenderDemographer(Demographer):
  asciiex = re.compile(r'[a-zA-Z]+')
  name_key = 'gender'

  def __init__(self, dictionary_filename=None, classifier_filename=None,
               use_classifier=False, use_name_dictionary=True):
    # Load the dictionary
    self.name_dictionary = None
    self.classifier = None

    assert use_name_dictionary or use_classifier

    if use_name_dictionary:
      self.name_dictionary = load_name_dictionary(dictionary_filename)

    # Load the classifier.
    if use_classifier:
      if not classifier_filename:
        dir = os.path.dirname(sys.modules[__package__].__file__)
        filename = os.path.join(dir, 'models', 'mw_simple', 'simple.json')
        if not os.path.exists(filename):
          assert download_pretrained_models(os.path.join(dir, 'models'), 'mw_simple')
      else:
        filename = classifier_filename

      # Both the hasher and classifier should have been saved to the same file
      with open(filename, 'r') as inf:
        hasher_json = inf.readline()
        self.hasher = hasher_from_json(FeatureHasher, hasher_json)
        # self.hasher = FeatureHasher(**hasher_json)
        classifier_json = inf.readline()
        self.classifier = sgd_classifier_from_json(SGDClassifier, classifier_json)
      # # Both the hasher and classifier should have been saved to the same file
      # with open(filename, 'rb') as inf:
      #   if version3:
      #     self.hasher = pickle.load(inf, encoding='bytes')
      #     self.classifier = pickle.load(inf, encoding='bytes')
      #   else:
      #     self.hasher = pickle.load(inf)
      #     self.classifier = pickle.load(inf)

  def process_tweet(self, tweet):
    if 'user' in tweet:
      user_info = tweet.get('user')
    else:
      user_info = tweet
    name_string = user_info.get('name')

    return self.process_name(name_string)

  def process_name(self, name_string):
    """Get something like a name from a string using a simple regex.
    """
    matcher = self.asciiex.search(name_string.split(' ')[0])
    if matcher:
      firstname = matcher.group(0)
      result = self._name_probability(firstname)
    else:
      result = {"value": "unk", "name": "gender"}

    return {self.name_key: result}

  def _name_probability(self, first_name_anycase):
    """Given something from the name field, predict gender based on
    social security data from the US.

    In this simple version, we use raw counts and compute probabilities
    based on the percentage of male vs. female children registered
    with those names.
    """
    firstname = first_name_anycase.lower()

    if self.name_dictionary and firstname in self.name_dictionary:
      w_ct = self.name_dictionary[firstname]['F']
      m_ct = self.name_dictionary[firstname]['M']
      tot = (w_ct + m_ct) * 1.0
      prob_w = w_ct / tot
      prob_m = m_ct / tot
      if prob_w > prob_m:
        result = {
            "value": "woman", "name": "gender",
            "annotator": "Gender Namelist",
            "scores": {"woman": prob_w, "man": prob_m}}
      else:
        result = {
            "value": "man", "name": "gender", "annotator": "Gender Namelist",
            "scores": {"woman": prob_w, "man": prob_m}}

    elif self.classifier:
      features = extract_gender_features(firstname)
      vector = self.hasher.transform([features])
      prediction = self.classifier.predict(vector)[0]
      score = self.classifier.decision_function(vector)[0]
      if prediction == "M":
        prob_m, prob_w = score, 1 - score
        prediction = 'man'
      else:
        prob_w, prob_m = score, 1 - score
        prediction = 'woman'

      result = {"value": prediction, "name": "gender",
                "annotator": "Simple Gender Classifier",
                "scores": {"woman": prob_w, "man": prob_m}}

    else:
      result = {"value": "unk", "name": "gender"}

    # Sort the list from most probable to least probable.
    # result = sorted(result, key=lambda x: x.get("prob"))
    # result.reverse()

    return result


# TODO move the training code to a separate train file
# ----------------------------------------
def load_name_dictionary(dictionary_filename):
  if not dictionary_filename:
    dir = os.path.dirname(sys.modules[__package__].__file__)
    # filename = os.path.join(dir, 'data/census_gender_dct.p')
    filename = os.path.join(dir, 'models', 'mw_simple', 'census_gender_dct.json')
    if not os.path.exists(filename):
      assert download_pretrained_models(os.path.join(dir, 'models'), 'mw_simple')
  else:
    filename = dictionary_filename

  with open(filename) as inf:
    name_dictionary = json.loads(inf.readline())

  return name_dictionary


def extract_gender_features(word):
  """ Produce features for classification.
  If you choose to add new features, be sure to delete the saved
  classifier (or the new features will not be used).
  """
  word = word.lower()
  features = {}

  # First and last n-grams.
  features['last_letter=%s' % word[-1]] = 1
  features['first_letter=%s' % word[0]] = 1

  if len(word) > 1:
    features['first_2=%s' % word[:2]] = 1
    features['last_2=%s' % word[-2:]] = 1
  if len(word) > 2:
    features['first_3=%s' % word[:3]] = 1
    features['last_3=%s' % word[-3:]] = 1
  if len(word) > 3:
    features['first_4=%s' % word[:4]] = 1
    features['last_4=%s' % word[-4:]] = 1

  if word[0] in 'aeiou':
    features['starts_vowel'] = 1
  else:
    features['starts_consonant'] = 1

  if word[-1] in 'aeiou':
    features['ends_vowel'] = 1
  else:
    features['ends_consonant'] = 1

  # Whole name
  features['name=%s' % word] = 1

  return features


def create_census_gender_dict(data_path, dictionary_filename):
  """Read in data, produce json dictionary file.

  name_dict[NAME][YEAR][GENDER] = # NAME with GENDER in YEAR

  Example: name_dict[susan][1880][W] = #woman susans in 1880

  Note: also includes count over all years -- example:
  name_dict[susan]['all'][W] = total # woman susans from 1880-2014
  """

  years = range(1916, 2000)
  name_dict = defaultdict(defaultdict)
  gender_mapping = {'F': 'W', 'M': 'M'}
  logging.info('Reading from: %s' % data_path)
  for year in years:
    try:
      file = open(data_path + 'yob%s.txt' % year)
      CSV_file = csv.reader(file)
    except FileNotFoundError:
      err_msg = "Error: Data failed to load, please check that " + \
          "name data is in data directory.\n"
      logging.critical(err_msg)
      sys.exit(err_msg)

    for line in CSV_file:
      name, gender, count = line
      name = name.lower()
      gender = gender_mapping[gender]
      count = int(count)
      if year not in name_dict[name]:
        name_dict[name][year] = {'W': 0, 'M': 0}
      name_dict[name][year][gender] = count

    file.close()

  for name in name_dict:
    w_ct, m_ct = 0, 0
    for year in name_dict[name]:
      w_ct += name_dict[name][year]['W']
      m_ct += name_dict[name][year]['M']

    name_dict[name]['all'] = {'W': w_ct, 'M': m_ct}

  logging.info('Saving to %s' % dictionary_filename)
  with open(dictionary_filename, 'w') as outf:
    # pickle.dump(name_dict, writer)
    outf.write(json.dumps(name_dict))


def train_gender_classifier(classifier_filename, dictionary_filename=None):
  '''
  Train a classifier based on the given data.
  If you choose to change the classifier (or features), be sure to delete
  the saved classifier, or you will not see changes to your model.
  '''
  # from sklearn.grid_search import GridSearchCV

  logging.info('Loading name dictionary')
  name_dictionary = load_name_dictionary(dictionary_filename)

  unique_features = set()

  train_set = []
  for name in name_dictionary:
    vals = name_dictionary[name]['all']
    label = 'M'

    # Label name by gender more frequently associated with it.
    if vals['W'] >= vals['M']:
      label = 'W'

    features_dict = extract_gender_features(name)

    unique_features.update(features_dict.keys())

    train_set.append((features_dict, label))

  # Convert to sklearn instances
  hasher = FeatureHasher(n_features=len(unique_features) * 2)

  random.seed(0)
  random.shuffle(train_set)

  train_features = [features_dict for features_dict, label in train_set]
  train_labels = [label for features_dict, label in train_set]

  train_vectors = hasher.transform(train_features)

  logging.info('Training')
  classifier = SGDClassifier(loss='hinge', penalty='l2')
  classifier.fit(train_vectors, train_labels)

  '''
  parameters = {'alpha': [0.000001, 10]}
  gs = GridSearchCV(classifier, parameters)
  gs.fit(train_vectors, train_labels)
  classifier = gs.best_estimator_
  logging.info('Selected alpha=%s' % str(gs.best_params_['alpha']))
  '''

  from sklearn.metrics import accuracy_score
  logging.info('Train accuracy: {:.4f}'.format(
      accuracy_score(train_labels, classifier.predict(train_vectors))))

  logging.info('Saving classifier to %s' % classifier_filename)
  with open(classifier_filename, 'wb') as writer:
    hasher_dict = hasher.__dict__
    del hasher_dict['dtype']
    writer.write("{}\n".format(json.dumps(hasher_dict, cls=NumpySerializer)))
    writer.write("{}\n".format(sgd_classifier_to_json(classifier)))
    # pickle.dump(hasher, writer)
    # pickle.dump(classifier, writer)


if __name__ == "__main__":
  d = CensusGenderDemographer(use_classifier=True, use_name_dictionary=False)
  print(d.process_tweet({"name": "Zach Wood-Doughty"}))
