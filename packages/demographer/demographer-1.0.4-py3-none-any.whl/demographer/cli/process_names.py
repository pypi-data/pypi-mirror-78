import argparse
import json
import logging

from demographer import process_name


def process(input_file, output_file, demographers=None):
  logging.info('Reading from %s' % input_file)
  logging.info('Writing to %s' % output_file)
  with open(input_file) as input, open(output_file, 'w') as writer:
    for line in input:
      if len(line.strip()) == 0:
        writer.write(line)
        continue

      name = {"name": line.strip()}
      result = process_name(line.strip(), demographers)
      name['demographics'] = result

      writer.write(json.dumps(name))
      writer.write('\n')


def main():
  logging.basicConfig(level=logging.INFO)

  parser = argparse.ArgumentParser(
      description='Process a tweets file to add demographic information.')
  parser.add_argument(
      '--classifier', required=True, type=str,
      help='The type of classifier to use. eg \
      "genderc gender indorg" in quotes')
  parser.add_argument(
      '--input', required=True, help='The path to the tweets file to process.')
  parser.add_argument(
      '--output', required=True,
      help='The tweets file with added demographic information.')

  args = parser.parse_args()
  demographers = []

  '''
  To add your own pickled classifier check the class
    of the respective demographer and set up initial commands
  Example: demographers.append(IndividualOrgDemographer(
    "data/indorg_classifier.p", "data/transformer.p"))

  '''
  for classifier in args.classifier.split():
    # TODO is this import setup helpful at all?
    if classifier == "genderc":
      from demographer.gender_c import GenderCDemographer
      demographers.append(GenderCDemographer())
    elif classifier == "gender":
      from demographer.gender import CensusGenderDemographer
      demographers.append(CensusGenderDemographer(use_classifier=True))
    elif classifier == "indorg":
      from demographer.indorg import IndividualOrgDemographer
      demographers.append(IndividualOrgDemographer())

  process(args.input, args.output, demographers)
  logging.info('Done')


if __name__ == '__main__':
  main()
