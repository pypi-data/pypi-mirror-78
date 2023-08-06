# Demographer
### Simple demographics inference from a single tweet

### Authors:
 [Zach Wood-Doughty](https://zachwd.com)  (<zach at cs.jhu.edu>),  
 [Paiheng Xu](https://paihengxu.github.io)  (<paiheng at jhu.edu>),  
 Xiao Liu (<xliu119 at jhu.edu>),  
 [Praateek Mahajan](https://prtk.in)  (<praateekm at gmail.com>),  
 [Rebecca Knowles](https://cs.jhu.edu/~rknowles)  (<rknowle2 at jhu.edu>),  
 Josh Carroll  (<josh at joshcarroll.xyz>),  
 [Mark Dredze](https://cs.jhu.edu/~mdredze)  (<mdredze at cs.jhu.edu>)  

##### Supports: Python 3
(Python 2.7+ is supported if you change module imports from `from demographer.XXX import YYY` to `from XXX import YYY`.

> **Demographer**: one who studies subjects including the geographical distribution of people, birth and death rates, socioeconomic status, and age and sex distributions in order to identify the influences on population growth, structure, and development. (Dictionary.com)

Demographer is a Python package that predicts demographic characteristics from information in a single tweet. It's designed for Twitter, where it takes the name of the user and returns information about their likely demographics.

### Why demographics?
Many downstream applications that consume Twitter data benefit from knowing information about a user. Analyzing opinions and trends based on demographics is a cornerstone analysis common in many areas of social science. While some social media platforms provide demographics for users, Twitter does not.

### Can I extend demographer?
Yes! We designed the package to be highly extensible. If you have new types of training data, or a different approach entirely, you should be able to add it to the package. You need to subclass `Demographer`.

### What demographic attributes are supported?
The current release makes predictions for user gender and race/ethnicity, and differentiates between individuals and organizations.
For each demographic characteristics above, we provide a simple model that requires only numpy and scikit-learn,
and a neural model which requires Tensorflow. If you can't or don't want to install tensorflow 1.13, the code will only run the simple models.

- Gender
    - `CensusGenderDemographer`: predicts binary (Man, Woman) gender from character n-grams of user names.
    - `NeuralGenderDemographer`: predicts binary (Man, Woman) gender from a character-level neural model of user names.
    
- Ethnicity
    - `SimpleEthnicityDemographer`: predicts user race (Black/African American, White) from character n-grams of user names.
    - `EthSelfReportNeuralDemographer`: predicts user race/ethnicity (Asian, Black/African-American, Hispanic/Latino, and White) from neural model of user name and profile.
    - `EthSelfReportBERTDemographer`: predicts user race/ethnicity (Asian, Black/African-American, Hispanic/Latino, and White) from average-pooled embeddings of user historical tweets.
    
- Individual vs. Organization:
    - `IndividualOrgDemographer`: classifiers users as individuals or organizations from user name and profile features. 
    - `NeuralOrganizationDemographer`: classifiers users as individuals or organizations with a neural model of user name and profile features.

### I want to learn more!
To find out more details on the training data and models, check out our papers:

 - Zach Wood-Doughty, Paiheng Xu, Xiao Liu, and Mark Dredze "Using Noisy Self-Reports to Predict Twitter User Demographics." arXiv:2005.00635, 2020. [[PDF](https://arxiv.org/pdf/2005.00635.pdf)] 
 - Zach Wood-Doughty, Praateek Mahajan, and Mark Dredze. "Johns Hopkins or johnny-hopkins: Classifying Individuals versus Organizations on Twitter." PEOPLES, 2018. [[PDF](https://www.aclweb.org/anthology/W18-1108/)] 
 - Zach Wood-Doughty,  Nicholas Andrews, Rebecca Marvin, and Mark Dredze. "Predicting Twitter User Demographics from Names Alone." PEOPLES, 2018. [[PDF](https://www.aclweb.org/anthology/W18-1114/)]  
 - Rebecca Knowles, Josh Carroll, and Mark Dredze. "Demographer: Extremely Simple Name Demographics." NLP+CSS, 2016. [[PDF](https://aclweb.org/anthology/W16-5614)]  

### Please cite our work
If you use Demographer in a paper, you should cite the relevant papers above.

## Installation
With pip:

```
pip install demographer
```
From source, you can use `setuptools`

```
python setup.py install
```

### Models
When you first use demographer, it will attempt to download the model files from `https://bitbucket.org/mdredze/demographer/downloads`.
However, access to the race/ethnicity models requires the Data Use Agreement found here: [PDF](http://www.cs.jhu.edu/~mdredze/demographics-training-data/).

### Data
The training data for the gender models can be found [here](https://www.cs.jhu.edu/~svitlana/data/data_emnlp2013.tar.gz).  
Our training data for the Ind/Org models can be found [here](https://bitbucket.org/mdredze/demographer/downloads/indorg_dataset.tar.gz).  
The rest of the data is from [McCorriston, James, David Jurgens, and Derek Ruths. "Organizations are users too: Characterizing and detecting the presence of organizations on Twitter." ICWSM, 2015.](http://networkdynamics.org/resources/software/humanizr/).  

Access to the race/ethnicity data requires the Data Use Agreement found here: [PDF](http://www.cs.jhu.edu/~mdredze/demographics-training-data/).  

## Examples

### Command Line Access
We also provide a script that processes a file containing tweets and adds demographic information to each one. The input file contains tweets, each encoded in json, one object per line. The output file contains the same tweets with a new field `demographics` which contains the list from above. The command line options are limited; it does not offer full control over model options (e.g. class-balancing).

To run available demographers on an input file, run:

> python -m demographer.cli --input INPUT_FILE --output OUTPUT_FILE

To see the full CLI options, run:

> python -m demographer.cli --help

### API Access

We provide a simple API for Demographer. Here is an example of how you annotate a single tweet. Note that this examples uses a sample tweet file distributed with the library (users installing via pip can download `faketweets.txt` from the `data` directory at the root of this repository).
  
```python
import json 
from demographer import process_tweet

with open('data/faketweets.txt') as inf:
  tweet = json.loads(inf.readline())
  result = process_tweet(tweet)
```

The first time you import demographer expect to wait a bit. It needs to load the data and model to initialize the underlying demographers.

`result` stores dictionary objects, each corresponding to the output from one demographer. Here is an example of `result`:

> {'indorg_neural': {'value': 'ind', 'scores': {'ind': 0.83569944, 'org': 0.16430053}, 'annotator': 'Neural Organization Classifier', 'name': 'indorg'}, 'eth_selfreport_neural': {'value': 'White', 'scores': {'Hispanic': -5.135958, 'Asian': -2.176922, 'Black': 3.9080877, 'White': 4.404793}, 'annotator': 'Neural Self-Report Ethnicity Classifier', 'name': 'eth_selfreport'}, 'gender_neural': {'value': 'man', 'scores': {'man': 0.99483526, 'woman': 0.0051647704}, 'annotator': 'Neural Gender Classifier', 'name': 'gender'}}

To use specific models described above, you could

```python
from demographer.ethnicity_selfreport_neural import EthSelfReportNeuralDemographer
from demographer.gender_neural import NeuralGenderDemographer
from demographer.indorg_neural import NeuralOrganizationDemographer
from demographer.ethnicity import SimpleEthnicityDemographer
from demographer.gender import CensusGenderDemographer
from demographer.indorg import IndividualOrgDemographer

demographer_list = [
        EthSelfReportNeuralDemographer(balanced=True),
        CensusGenderDemographer(use_classifier=True, use_name_dictionary=True),
        IndividualOrgDemographer(setup='balanced')
    ]
result = process_tweet(tweet, demographer_list)
```

For models that required multiple tweets, you would need to retrieve users' historical tweets (timeline),
and name it as `{user_id}_statuses.json.gz`. 
`user_id` could be username or user's id.
Then you could
```python
from demographer import process_multiple_tweet_texts
from demographer.utils import read_tweet_text_from_timeline

user_with_multiple_texts = read_tweet_text_from_timeline(user_id='fake_id', timeline_dir='directory for status files')

from demographer.ethnicity_selfreport_bert import EthSelfReportBERTDemographer
demographer_list = [
          EthSelfReportBERTDemographer(bert_model='distilbert-base-uncased', use_cuda=False, embed_dir='tmp_embed', tweet_limit=200)
]
result = process_multiple_tweet_texts(user_with_multiple_texts, demographer_list)
```

