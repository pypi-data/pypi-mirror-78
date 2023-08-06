from __future__ import division

import os
import re
import sys

from demographer.demographer import Demographer
from demographer.utils import sgd_classifier_from_json
from demographer.utils import hasher_from_json
from demographer.utils import download_pretrained_models

from sklearn.feature_extraction import FeatureHasher
from sklearn.linear_model import SGDClassifier


class SimpleEthnicityDemographer(Demographer):
  asciiex = re.compile(r'[a-zA-Z]+')
  name_key = 'ethnicity_simple'

  def __init__(self, dictionary_filename=None, classifier_filename=None):
    # Load the dictionary
    self.classifier = None

    if not classifier_filename:
      dir = os.path.dirname(sys.modules[__package__].__file__)
      filename = os.path.join(dir, 'models', 'wb_simple', 'simple.json')
      if not os.path.exists(filename):
          assert download_pretrained_models(os.path.join(dir, 'models'), 'wb_simple')
    else:
      filename = classifier_filename

    # Both the hasher and classifier should have been saved to the same file
    with open(filename, 'r') as inf:
      hasher_json = inf.readline()
      self.hasher = hasher_from_json(FeatureHasher, hasher_json)
      classifier_json = inf.readline()
      self.classifier = sgd_classifier_from_json(SGDClassifier, classifier_json)

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
      result = {}

    return {self.name_key: result}

  def _name_probability(self, first_name_anycase):
    """Given something from the name field, predict gender based on
    social security data from the US.

    In this simple version, we use raw counts and compute probabilities
    based on the percentage of male vs. female children registered
    with those names.
    """
    firstname = first_name_anycase.lower()
    features = extract_name_features(firstname)
    vector = self.hasher.transform([features])
    prediction = self.classifier.predict(vector)[0]
    probs = self.classifier.predict_proba(vector)[0]
    probs = {self.classifier.classes_[i]: probs[i] for i in range(2)}

    result = {"value": prediction, "name": "ethnicity",
              "annotator": "Simple Ethnicity Classifier", "scores": probs}
    return result


# ----------------------------------------
# TODO move the training code to a separate train file

def extract_name_features(word):
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


if __name__ == "__main__":
  d = SimpleEthnicityDemographer()
  print(d.process_tweet({"name": "Zach Wood-Doughty"}))
