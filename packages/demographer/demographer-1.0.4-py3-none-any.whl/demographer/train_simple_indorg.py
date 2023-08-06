import os
import json
import random
import logging
from collections import defaultdict


from sklearn.feature_extraction import FeatureHasher
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score

from demographer.transformer_indorg import Transformer
from demographer.transformer_indorg import load_transformers
from demographer.transformer_indorg import transform_features
from demographer.transformer_indorg import extract_profile_features
from demographer.transformer_indorg import extract_name_features

from demographer.utils import sgd_classifier_to_json
from demographer.utils import NumpySerializer


def create_twitter_data_dict(data_file, dictionary_filename,
                             create_transformer=False, transformer_filename=None,
                             training=True, num_bins=10):
  """Creates a data dictionary from input file.

  You should create a transformer using your train set (not your validation set).
  This transformer is then used by `create_vectors_from_dict`

  Can be run by the client by
    $ python -m demographer.cli.create_ind_org_dict \
        --input data/train.json --output data/train_dict.p \
        --create_transformer True --transformer_filename tdata/transformer.p
    $ python -m demographer.cli.create_ind_org_dict \
        --input data/dev.json --output data/dev_dict.p


  Args:
    data_file: Path to input file, which has one json tweet per line
    dictionary_filename:  Where to save the dictionary json
    create_transformer: Need to create a transformer? True or False
    transformer_filename: If want to create a transformer where to save it?
    num_bins: Defaults to 10 (value required for the transformer)

  Returns:
    dictionary_filename : Where the dictionary was saved
  """
  name_dict = defaultdict(defaultdict)
  if create_transformer:
    features = defaultdict(list)

  logging.info('Reading from: %s' % data_file)
  with open(data_file, 'r') as input:
    for line in input:
      data = json.loads(line.strip())
      if 'user' in data:
        data = data.get('user')

      label, name, screen_name = data['accounttype_'], data['name'], data['screen_name']
      name_dict[screen_name][label] = name_dict[screen_name].get(label, 0) + 1
      name_dict[screen_name]['label'] = label

      name_dict[screen_name] = name_dict.get(screen_name, {})
      name_dict[screen_name]['name'] = name
      name_dict[screen_name]['followers_count'] = data['followers_count']
      name_dict[screen_name]['friends_count'] = data['friends_count']
      name_dict[screen_name]['listed_count'] = data['listed_count']
      name_dict[screen_name]['statuses_count'] = data['statuses_count']
      name_dict[screen_name]['verified'] = data['verified']
      name_dict[screen_name]['description'] = data['description']
      name_dict[screen_name]['created_at'] = data['created_at']

      if create_transformer:
        user_features = extract_profile_features(data)
        for key in user_features:
          features[key].append(user_features[key])

  if create_transformer:
    logging.info('Saving transformer to %s' % transformer_filename)

    transformers = {}
    for key in features:
      t = Transformer(features[key], num_bins)
      transformers[key] = t
    with open(transformer_filename, "w") as outf:
      outf.write({key: t.to_json() for key, t in transformers.items()})

  logging.info('Saving dictionary to %s' % dictionary_filename)

  with open(dictionary_filename, 'w') as outf:
    outf.write(json.dumps(name_dict))

  return dictionary_filename


def create_vectors_from_dict(data_dict, transformer_filename=None):
  """Create proper vectors form our data dictionary.
  This extracts features, normalizes them (using transformer).
  And creates an intermediate format which will be used by the classifier.

  Args:
    data_dict: The dictionary of input
    transformer_filename: Path to transformer

  Returns:
    unique_features: set of features (including name features and meta)
    train_set: List of tuples (feature, label), where each list item is
      an individual example

  """
  unique_features = set()
  train_set = []
  transformers = load_transformers(transformer_filename)

  name_iterable = data_dict.keys()

  for name in name_iterable:
    vals = data_dict[name]
    extract_features_from = data_dict[name]['name'] + " " + name
    features_dict = extract_name_features(extract_features_from)
    profile_features = extract_profile_features(data_dict[name])
    profile_features = transform_features(transformers, profile_features)

    unique_features.update(features_dict.keys())
    unique_features.update(profile_features.keys())
    features_dict.update(profile_features)
    label = vals['label']
    train_set.append((features_dict, label))

  return unique_features, train_set


def train_indorg_classifier(classifier_filename, train_dictionary_filename=None,
                            dev_dictionary_filename=None,
                            transformer_filename=None):
  """
  Train a classifier using training data,
  selects the best model which achieves the highest accuracy on dev data.
  Use the transformer create from training data to transform
  features of both training and dev set.

  Args:
    classifier_filename: Path where you want to save your classifier
    train_dictionary_filename: Path to your train dictionary
        (created using create_twitter_data_dict)
    dev_dictionary_filename: Path to your dev dictionary
        (created using create_twitter_data_dict)
    transformer_filename: Path to your transformer.

  Returns:
    None
  """

  # Load the training data which has been transformed into a json file
  logging.info('Loading name dictionary')

  with open(train_dictionary_filename, 'rb') as train_input:
    train_dictionary = json.loads(train_input)

  with open(dev_dictionary_filename, 'rb') as dev_input:
    dev_dictionary = json.loads(dev_input)

  unique_features, train_set = create_vectors_from_dict(
      train_dictionary, transformer_filename)
  _, dev_set = create_vectors_from_dict(dev_dictionary, transformer_filename)

  hasher = FeatureHasher(n_features=len(unique_features) * 2)
  random.shuffle(train_set)
  train_features = [features_dict for features_dict, label in train_set]
  train_labels = [label for features_dict, label in train_set]
  train_vectors = hasher.transform(train_features)

  dev_features = [features_dict for features_dict, label in dev_set]
  dev_labels = [label for features_dict, label in dev_set]
  dev_vectors = hasher.transform(dev_features)
  classifier = None
  best_accuracy = -1

  # Alter this as per your grid search over hyperparameters
  # TODO get rid of hinge loss; no predict_proba

  for loss in ['hinge', 'log', 'modified_huber', 'squared_hinge', 'perceptron']:
    for i in range(5, 50, 1):
      alpha = float(i) * 1e-5
      candidate_classifier = SGDClassifier(
          loss=loss, penalty='l2', alpha=alpha, max_iter=1000, tol=1e-3)
      candidate_classifier.fit(train_vectors, train_labels)
      predictions = candidate_classifier.predict(dev_vectors)
      candidate_accuracy = accuracy_score(predictions, dev_labels)
      if candidate_accuracy > best_accuracy:
        best_accuracy = candidate_accuracy
        classifier = candidate_classifier
        # best_alpha = alpha
        # best_loss = loss

  logging.info("On grid search, best dev accuracy was {:.4f}".format(
      best_accuracy))

  classifier.fit(train_vectors, train_labels)
  logging.info('Train accuracy: %.4f' % accuracy_score(
      train_labels, classifier.predict(train_vectors)))
  predictions = classifier.predict(dev_vectors)
  candidate_accuracy = accuracy_score(predictions, dev_labels)
  logging.info('Dev accuracy: %.4f' % candidate_accuracy)

  logging.info('Saving classifier to %s' % classifier_filename)
  with open(classifier_filename, 'wb') as writer:
    hasher_dict = hasher.__dict__
    del hasher_dict['dtype']
    writer.write("{}\n".format(json.dumps(hasher_dict, cls=NumpySerializer)))
    writer.write("{}\n".format(sgd_classifier_to_json(classifier)))
    # pickle.dump(hasher, writer)
    # pickle.dump(classifier, writer)


def train_and_test(work_dir, training_data_files, valid_data_files, test_data_files,
                   test_on_dev=False):

  train_fn = os.path.join(work_dir, "train.json")
  train_dict = create_twitter_data_dict(training_data_files, train_fn)
  valid_fn = os.path.join(work_dir, "valid.json")
  valid_dict = create_twitter_data_dict(valid_data_files, valid_fn)
  if test_on_dev:
    test_dict = valid_dict
    test_data_files = valid_data_files
  elif test_data_files is not None:
    test_fn = os.path.join(work_dir, "test.json")
    test_dict = create_twitter_data_dict(test_data_files, test_fn)
  else:
    test_dict = None
  train_indorg_classifier(train_dict, valid_dict, test_dict, test_data_files)


def main():
  work_dir = "."
  test_on_dev = False
  train_and_test(
      work_dir,
      [],  # train users
      [],  # dev users
      [],  # test users
      test_on_dev=test_on_dev)


if __name__ == '__main__':
  main()
