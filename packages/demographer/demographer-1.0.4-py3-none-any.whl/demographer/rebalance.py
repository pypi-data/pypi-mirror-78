import time
from functools import reduce

import numpy as np

from sklearn.datasets import fetch_openml
from sklearn.linear_model import LogisticRegression

DANIEL_DATA_PROBS = {0: .808, 1: .095, 2: .061, 3: .036}
BALANCED_PROBS = {i: 0.25 for i in range(4)}
# class probs: {W: 80.8, B: 9.5, H: 6.1, A: 3.6}


def mnist():
  data_home = '/export/c10/zach/data/mnist/'
  # Load data from https://www.openml.org/d/554
  start = time.time()
  X, y = fetch_openml('mnist_784', version=1, return_X_y=True, data_home=data_home)
  # data_path = "/export/c10/zach/data/mnist/openml/openml.org/data/v1/download/52667.gz"
  # with gzip.open(data_path) as inf:
  #   data, meta = arff.loadarff(inf)

  y = y.astype(np.int32)
  print("loading took {}s".format(time.time() - start))

  return X, y


def preprocess(X, y):
  np.random.seed(42)
  permutation = np.random.permutation(X.shape[0])
  X = X[permutation]
  y = y[permutation]

  x_odd = X[y % 2 == 1]
  y_odd = y[y % 2 == 1]
  x_even = X[y % 2 == 0]
  y_even = y[y % 2 == 0]
  y_odd = np.zeros_like(y_odd)
  y_even = np.ones_like(y_even)

  n_odd = x_odd.shape[0]
  n_even = x_even.shape[0]
  uneven_percent = .8
  odd_cutoff = int(n_odd * uneven_percent)
  even_cutoff = int(n_even * (1 - uneven_percent))

  x_train = np.concatenate((x_odd[:odd_cutoff], x_even[:even_cutoff]))
  y_train = np.concatenate((y_odd[:odd_cutoff], y_even[:even_cutoff]))

  x_test = np.concatenate((x_odd[odd_cutoff:], x_even[even_cutoff:]))
  y_test = np.concatenate((y_odd[odd_cutoff:], y_even[even_cutoff:]))

  return (x_train, y_train, x_test, y_test)


def analyze(x_train, y_train, x_test, y_test):

  n_classes = 1 + np.max(y_train)

  clf = LogisticRegression(C=10,
                           multi_class='multinomial',
                           penalty='l1', solver='saga', tol=0.1)
  # clf = MLPClassifier()
  clf.fit(x_train, y_train)

  # train: 0.9341 test: 0.8963
  print("train: {:.4f} test: {:.4f}".format(clf.score(x_train, y_train),
                                            clf.score(x_test, y_test)))
  # print(np.mean(np.equal(np.argmax(clf.predict_proba(x_test), axis=1), y_test)))

  train_logits = clf.predict_proba(x_train)
  test_class_probs = {k: np.mean(y_test == k) for k in range(n_classes)}
  class_thresholds = rebalance_classifier(train_logits, y_train, test_class_probs)
  print(class_thresholds)

  test_logits = clf.predict_proba(x_test)
  test_predictions = stacked_threshold_classifier(test_logits, class_thresholds)
  test_accuracy = np.mean(np.equal(y_test, test_predictions))
  print("test accuracy: {:.4f}".format(test_accuracy))
  print("cls \t train_prop \t test_prop \t train_acc \t test_acc \t rebal_acc")
  for i in range(n_classes):
    train_prop = np.mean(y_train == i)
    test_prop = np.mean(y_test == i)
    train_acc = clf.score(x_train[y_train == i], y_train[y_train == i])
    test_acc = clf.score(x_test[y_test == i], y_test[y_test == i])
    rebal_acc = np.mean(np.equal(y_test[y_test == i],
                                 test_predictions[y_test == i]))
    print("\t".join([str(i), "{:.1f}%".format(100 * train_prop),
                     "{:.1f}%".format(100 * test_prop),
                     "{:.1f}".format(100 * train_acc),
                     "{:.1f}".format(100 * test_acc),
                     "{:.1f}".format(100 * rebal_acc)]))

    # print("class {} gets {:.4f} train acc and {:.4} test acc".format(i,
    # print("class {} gets {:.4} rebalanced test acc".format(i, acc))


def threshold_argmax(logits, k, threshold):
  upweight = np.zeros_like(logits)
  upweight[:, k] = threshold
  return np.argmax(logits + upweight, axis=1)


def stacked_threshold_classifier(logits, class_thresholds):
  predictions = -1 * np.ones(logits.shape[0])
  for k, threshold in class_thresholds:
    new_classifications = threshold_argmax(logits, k, threshold)
    for i in range(new_classifications.shape[0]):
      if predictions[i] == -1 and new_classifications[i] == k:
        predictions[i] = k
  return predictions


def rebalance_classifier(logits, labels, class_probs=None):
  n_classes = 1 + int(np.max(labels))
  # print("We see {} classes".format(n_classes))
  class_stats = []
  if class_probs is None:
    for k in range(n_classes):
      where_true = labels == k
      # what dtype is where_true supposed to be?
      prob = np.mean(where_true)
      recall = np.mean(np.equal(labels[where_true],
                       np.argmax(logits[where_true], axis=1)))
      class_stats.append((k, recall, prob))
  else:
    for k in range(n_classes):
      where_true = labels == k
      prob = class_probs[k]
      recall = np.mean(np.equal(labels[where_true],
                       np.argmax(logits[where_true], axis=1)))
      class_stats.append((k, recall, prob))

  class_thresholds = []
  total_prob = 0
  seen = []
  class_stats = sorted(class_stats, key=lambda tup: tup[2], reverse=True)
  for tup in class_stats[:-1]:
    k, recall, prob = tup
    seen.append(k)
    total_prob += prob
    where_true = labels == k
    where_false = reduce(np.logical_and, [labels != k for k in seen])

    scores = []
    # this does range(-1, 1, 0.05)
    thresholds = [-1 + i / 100 for i in range(0, 200, 5)]
    for threshold in thresholds:
      new_classifications = threshold_argmax(logits, k, threshold)
      class_recall = np.mean(np.equal(labels[where_true], new_classifications[where_true]))
      if np.sum(where_false) > 0:
        other_recall = np.mean(np.equal(labels[where_false], new_classifications[where_false]))
      else:
        other_recall = 0
      score = prob * class_recall + (1 - total_prob) * other_recall
      scores.append(score)

    threshold_i = np.argmax(scores)
    class_thresholds.append((k, thresholds[threshold_i]))
  class_thresholds.append((class_stats[-1][0], np.inf))

  # accuracy = np.mean(np.equal(labels,
  #                    stacked_threshold_classifier(logits, class_thresholds)))

  return class_thresholds


# if __name__ == "__main__":
  # mnist()
