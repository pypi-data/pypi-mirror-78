import logging
import json
import gzip

from demographer.utils import tf
from demographer.utils import NumpySerializer


def get_default_demographers():
  if tf is not None:
    from demographer.gender_neural import NeuralGenderDemographer
    from demographer.indorg_neural import NeuralOrganizationDemographer

    return [NeuralGenderDemographer(),
            NeuralOrganizationDemographer(setup="full")]
  else:
    from demographer.gender import CensusGenderDemographer
    from demographer.indorg import IndividualOrgDemographer

    return [
        CensusGenderDemographer(use_classifier=True, use_name_dictionary=True),
        IndividualOrgDemographer(setup="full")]


def get_default_demographer_for_multiple_tweets():
  from demographer.ethnicity_selfreport_bert import EthSelfReportBERTDemographer
  return [EthSelfReportBERTDemographer()]


def process_tweet(tweet, demographers=None):
  """
  Process a single tweet (json format) and return a dictionary whose keys
  are demographic attributes and whose entries are lists of predictions.
  """

  if not demographers:
    demographers = get_default_demographers()

  result = {}
  for demographer in demographers:
    result.update(demographer.process_tweet(tweet))

  return result


def process_multiple_tweet_texts(user_with_tweets, demographers=None):
  """
  Process multiple tweet texts and return a dictionary whose keys
  are demographic attributes and whose entries are lists of predictions.
  """

  result = {}
  if not demographers:
    demographers = get_default_demographer_for_multiple_tweets()

  for demographer in demographers:
    assert demographer.name_key in ['eth_selfreport_bert']
    result.update(demographer.process_multiple_tweets(user_with_tweets))

  return result


def process_name(name, demographers=None):
  """
  Process a single tweet (json format) and return a dictionary whose keys
  are demographic attributes and whose entries are lists of predictions.
  """

  if not demographers:
    demographers = get_default_demographers()

  result = {}

  for demographer in demographers:
    result.update(demographer.process_name(name))

  return result


def process(input_file, output_file, demographers=None, full=False):
  '''
  To run this directly, call:
    process(tweets.json, labeled_tweets.json, load_demographers())
  '''
  is_gzip = input_file.endswith('gz')

  logging.info('Reading from %s' % input_file)
  logging.info('Writing to %s' % output_file)

  open_fn = open
  if is_gzip:
    open_fn = gzip.open

  with open_fn(input_file) as input, open_fn(output_file, 'w') as writer:
    for line in input:
      if is_gzip:
        line = line.decode()
      if len(line.strip()) == 0:
        writer.write(line)
        continue

      tweet = json.loads(line)
      result = process_tweet(tweet, demographers)
      if full:
        output = tweet
      else:
        output = {}
        if "user" in tweet:
          output["tweetid"] = tweet["id_str"]
        user = tweet.get("user", tweet)
        output["userid"] = user["id_str"]
        output["screen_name"] = user["screen_name"]

      output['demographics'] = result

      outline = "{}\n".format(json.dumps(output, cls=NumpySerializer))
      if is_gzip:
        outline = outline.encode('utf8')
      writer.write(outline)


def check(a, b):
  return len(a.intersection(b)) > 0


def load_demographers(classifiers, model):
  '''
  classifiers: comma-separated classifiers to use
    e.g. "gender" or "gender,ethnicity,organization"

  model: one of "neural", "best", "simple"
    neural requires tensorflow, best will use tensorflow if it is installed

  To add your own pickled classifier check the class
    of the respective demographer and set up initial commands
   Example: demographers.append(IndividualOrgDemographer(
    "data/indorg_classifier.p", "data/transformer.p"))

  '''

  demographers = []

  get_simple = model in ['simple', 'all'] or (model == 'best' and tf is None)
  get_neural = model == 'neural' or (model in ['best', 'all'] and tf is not None)
  classifiers = set(classifiers.split(','))

  all_classifiers = {"all", "genderc", "gender", "ethnicity", "organization"}
  if len(classifiers - all_classifiers) > 0:
    raise ValueError("Unknown classifiers: {}".format(
        ", ".join(map(str, classifiers - all_classifiers))))

  if check(classifiers, {"all", "genderc"}):
    from demographer.gender_c import GenderCDemographer
    demographers.append(GenderCDemographer())

  if check(classifiers, {"all", "gender"}):
    if get_neural:
      if tf is None:
        raise ImportError("Please install tensorflow==1.13.1!")
      from demographer.gender_neural import NeuralGenderDemographer
      demographers.append(NeuralGenderDemographer(dtype='n'))
    if get_simple:
      from demographer.gender import CensusGenderDemographer
      demographers.append(CensusGenderDemographer(use_classifier=True))

  if check(classifiers, {"all", "ethnicity"}):
    if get_neural:
      if tf is None:
        raise ImportError("Please install tensorflow==1.13.1!")
      from demographer.ethnicity_selfreport_neural import EthSelfReportNeuralDemographer
      balance = [True]
      rebalance = [True]
      demographers.append(EthSelfReportNeuralDemographer(
          balanced=balance, rebalance=rebalance))

    if get_simple:
      from demographer.ethnicity import SimpleEthnicityDemographer
      demographers.append(SimpleEthnicityDemographer())

  if check(classifiers, {"all", "organization"}):
    setups = ["full"]
    if model == 'all':
      setups = ["full", "balanced"]
    for setup in setups:
      if get_neural:
        if tf is None:
          raise ImportError("Please install tensorflow==1.13.1!")
        from demographer.indorg_neural import NeuralOrganizationDemographer
        demographers.append(NeuralOrganizationDemographer(setup=setup))
      if get_simple:
        from demographer.indorg import IndividualOrgDemographer
        demographers.append(IndividualOrgDemographer(setup=setup))

  return demographers
