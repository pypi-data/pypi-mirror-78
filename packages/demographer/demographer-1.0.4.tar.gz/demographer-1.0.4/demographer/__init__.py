__version__ = '1.0.0'

import warnings
warnings.filterwarnings("ignore", message=".*numpy.ufunc size changed.*")

try:
  with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=FutureWarning,
                            message=".*future version of numpy.*")
    from demographer.utils import tf  # noqa
except ImportError:
  print("If you are still using python2, you will need to change all 'from demographer.XXX import YYY' statements to 'from XXX import YYY'")  # noqa
  print("Try: `find demographer -name '*.py' -exec sed -i 's/demographer\.//g' {} +`")  # noqa
  raise ImportError

from demographer.cli.process_tweets import process_tweet
from demographer.cli.process_tweets import process_multiple_tweet_texts
