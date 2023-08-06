import argparse
import logging

from demographer.cli.process_tweets import process, load_demographers


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)

  parser = argparse.ArgumentParser(
      description='Process a tweets file to add demographic information.')
  parser.add_argument(
      '--classifier', default='gender,organization', type=str,
      help='The comma-separated classifier(s) to use, e.g. "gender" or "gender,organization,ethnicity".')
  parser.add_argument(
      '--model', type=str, default='best',
      help="Type types of models to use in classifiers:\
      one of 'best', 'neural', 'simple', or 'all'.")
  parser.add_argument(
      '--input', required=True, help='The path to the tweets file to process.')
  parser.add_argument(
      '--output', required=True,
      help='The output file with inferred demographics.')
  parser.add_argument(
      '--full', action='store_true', help="Output full tweets, not just demographics.")

  args = parser.parse_args()

  assert args.model in ['best', 'neural', 'simple', 'all'], \
      "--model must be in ['best', 'neural', 'simple', 'all']"
  demographers = load_demographers(args.classifier, args.model)
  if not demographers:
    raise ValueError("No matching demographers could be loaded")

  process(args.input, args.output, demographers, full=args.full)
  logging.info('Done')
