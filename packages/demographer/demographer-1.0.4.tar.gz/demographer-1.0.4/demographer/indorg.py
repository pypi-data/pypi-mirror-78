import os
import sys

from demographer.demographer import Demographer
from demographer.transformer_indorg import load_transformers
from demographer.transformer_indorg import transform_features
from demographer.transformer_indorg import extract_profile_features
from demographer.transformer_indorg import extract_name_features
from demographer.utils import sgd_classifier_from_json
from demographer.utils import hasher_from_json
from demographer.utils import download_pretrained_models

from sklearn.feature_extraction import FeatureHasher
from sklearn.linear_model import SGDClassifier


class IndividualOrgDemographer(Demographer):

  def __init__(self, classifier_filename=None, transformer_filename=None,
               setup='balanced'):
    """Initalizes a class for an Individual vs Organization classifier

    Constructor needs to load a classifier (sklearn module), a hasher (sklearn module)
    and a transformer.

    A transformer is used to normalize our continuous features such as
    followers count, statuses count to a -1,1 range

    The transformer should have been created using train set, and now is used on test set

    Args:
      classifier_filename: Path to the classifier filename. (default is in data dir)
      transformer_filename: Path to the transformer. (default is in data dir)

    """
    self.name_key = 'indorg_{}'.format(setup)
    self.classifier = None
    self.transformers = None
    self.hasher = None
    self.setup = setup
    if not classifier_filename:
      dir = os.path.dirname(sys.modules[__package__].__file__)
      if setup == 'full':
        filename = os.path.join(dir, 'models/indorg_simple/indorg_full_classifier.json')
      elif setup == 'balanced':
        filename = os.path.join(dir, 'models/indorg_simple/indorg_balanced_classifier.json')
      else:
        raise ValueError("Unknown setup `{}'".format(setup))
      if not os.path.exists(filename):
          assert download_pretrained_models(os.path.join(dir, 'models'), 'indorg_simple')
    else:
      filename = classifier_filename

    with open(filename, 'r') as inf:
      hasher_json = inf.readline()
      self.hasher = hasher_from_json(FeatureHasher, hasher_json)
      classifier_json = inf.readline()
      self.classifier = sgd_classifier_from_json(SGDClassifier, classifier_json)

    self.transformers = load_transformers("simple", fn=transformer_filename)

  def process_tweet(self, tweet):
    """Get the user object from tweet and pass it to _process_user

    Args:
      tweet: Has to be either tweet containing user info, or just user info

    Returns:
      result: Which is the prediction based on the classifier
    """
    if 'user' in tweet:
      user_info = tweet.get('user')
    else:
      user_info = tweet

    return self._process_user(user_info)

  def process_name(self, name_string):
    """Extracts features of users and makes a prediction using the classifier
    Args:
      user_info: The user object from which features are extracted

    Returns:

    """
    # Add extra space, so that screenname is empty
    extract_features_from = name_string + " " + " "
    features_dict = extract_name_features(extract_features_from)
    vector = self.hasher.transform([features_dict])
    prediction = self.classifier.predict(vector)[0]
    score = self.classifier.decision_function(vector)[0]
    result = {"value": prediction, "name": self.name_key,
              "annotator": "Individual vs Organization",
              "setup": self.setup,
              "scores": {prediction: score}}
    return {self.name_key: result}

  def _process_user(self, user_info):
    """Extracts features of users and makes a prediction using the classifier
    Args:
      user_info: The user object from which features are extracted
    """
    extract_features_from = user_info['name'] + " " + user_info['screen_name']
    features_dict = extract_name_features(extract_features_from)
    profile_features = extract_profile_features(user_info)
    profile_features = transform_features(self.transformers, profile_features)
    features_dict.update(profile_features)
    vector = self.hasher.transform([features_dict])
    prediction = self.classifier.predict(vector)[0]
    score = self.classifier.decision_function(vector)[0]
    result = {"value": prediction, "name": self.name_key,
              "annotator": "Individual vs Organization",
              "setup": self.setup,
              "scores": {prediction: score}}
    return {self.name_key: result}

# def extract_profile_features(user):
#   features = {}
#   if not user:
#     return {}
#
#   features['friends_count'] = user['friends_count']
#   features['followers_count'] = user['followers_count']
#   features['ratio'] = user['followers_count'] / float(max(1, user['friends_count']))
#   features['listed_count'] = user['listed_count']
#   features['statuses_count'] = user['statuses_count']
#
#   try:
#     descr_length = len(user['description'] or [])
#   except Exception as e:
#     print(e)
#     descr_length = 0
#   features['descr_high'] = descr_length
#
#   pronoun_count = 0
#   collective_count = 0
#   personal_pronouns = ['my', 'i', 'me', 'i\'m', 'i\'ll', 'mine']
#   collective_pronouns = ['we', 'our', 'us', 'we\'ll', 'we\'ve', 'ours']
#
#   try:
#     words = re.split(r"\W+", user['description'] or '')
#   except Exception as e:
#     print(e)
#     words = []
#   for word in words:
#     if word.lower() in personal_pronouns:
#       pronoun_count += 1
#     if word.lower() in collective_pronouns:
#       collective_count += 1
#
#   features['collective_count'] = collective_count
#   features['pronoun_count'] = pronoun_count
#
#   repetitive_punc = r'(\!|\"|\#|\$|\%|\&|\'|\(|\)|\*|\+|\,|\-|\.|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\|\]|\^|\_|\`|\{|\|\|}\|\~){2,}'  # noqa
#   try:
#     rep_punc = len(re.findall(repetitive_punc, user['description'] or ''))
#   except Exception as e:
#     print(e)
#     rep_punc = 0
#   features['rep_punc'] = rep_punc
#
#   features['verified'] = int(user['verified'])
#
#   d1 = datetime.now()
#   d2 = datetime.strptime(user['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
#   diff = (d1.year - d2.year) * 12 + d1.month - d2.month
#
#   tweets_per_month = user['statuses_count']/float(diff)
#   features['tweets_per_month'] = tweets_per_month
#   features['months'] = diff
#
#   return features

# def transform_features(transformers, features):
#   """Transform features of users as per transformer.
#
#   Args:
#     features: Features of our example in test set
#
#   Returns:
#     output: Transformed features
#   """
#   assert type(transformers) == dict
#   assert type(features) == dict
#
#   output = features.copy()
#
#   for key in features:
#     if key in transformers:
#       try:
#         # TODO this is a slightly hacky solution. AFAIK `listed_count' is the only missing key
#         output[key] = transformers[key].transform(features.get(key, 0))
#       except TypeError:
#         output[key] = transformers[key].min
#         pass
#
#   return output


if __name__ == "__main__":
  # TODO: if run `python -m demographer.indorg`, structure dependency caused runtime warning
  tweets = [
      {"name": "Zach Wood-Doughty", "screen_name": "zachwooddoughty",
       "location": None, "url": None, "description": "PhD student at @JHUCLSP",
       "protected": False, "verified": False, "followers_count": 76,
       "friends_count": 89, "listed_count": 6, "favourites_count": 367,
       "statuses_count": 3013,
       "created_at": "Thu Dec 24 17:07:51 +0000 2015", },  # noqa
      {"name": "ESPN", "screen_name": "ESPN", "location": "Sports",
       "url": "espn.com", "protected": False, "verified": True,
       "description": "Best place to follow all your favorite news websites",
       "followers_count": 10000000, "friends_count": 42, "listed_count": 1235,
       "favourites_count": 123, "statuses_count": 20013,
       "created_at": "Thu Dec 24 17:07:51 +0000 2012", }]  # noqa

  for setup in ['full', 'balanced']:
    d = IndividualOrgDemographer(setup=setup)
    for tweet in tweets:
      print(setup, tweet['name'], d.process_tweet(tweet))
