import os
import sys
import json
import gzip
import numpy as np

import torch
from pytorch_transformers import *
from transformers import DistilBertModel, DistilBertTokenizer
from sklearn.linear_model import LogisticRegression

from demographer.demographer import Demographer
from demographer.utils import download_pretrained_models
from demographer.utils import read_tweet_text_from_timeline
from demographer.utils import NumpySerializer
from demographer.utils import sgd_classifier_from_json
from demographer.label_mapping import race_bert_back_mapping

class EthSelfReportBERTDemographer(Demographer):
  name_key = 'eth_selfreport_bert'
  def __init__(self, model_dir=None, bert_model='distilbert-base-uncased', embed_dir=None, use_cuda=True, tweet_limit=200):
    """
    Initializes a class for a race/ethnicity classifier that use pre-trained DistilBERT

    Args:
        model_dir: where does the model live?
        bert_model: default using distilbert-base-uncased, could also be a path to fine-tuned bert model
        embed_dir: specify a directory to store embeddings, otherwise will not store the embeddings.
        use_cuda: whether use cuda
        tweet_limit: recommended 200 tweets
    """
    self.use_cuda = use_cuda
    self.bert_model_name = bert_model
    self.tweet_limit = tweet_limit

    self.embed_dir = embed_dir
    if embed_dir:
      if not os.path.exists(embed_dir):
        os.makedirs(embed_dir)

    if model_dir is None:
      base_dir = os.path.dirname(sys.modules[__package__].__file__)
      model_dir = os.path.join(base_dir, 'models')
      model_fn = os.path.join(model_dir, 'ethnicity_selfreport_bert', 'balanced_logistic.json')
      if not os.path.exists(model_fn):
        assert download_pretrained_models(model_dir, 'ethnicity_selfreport_bert')

      # load logistic regression model
      with open(model_fn, 'r') as inf:
        line = inf.readline()
        self.logis_model = sgd_classifier_from_json(cls=LogisticRegression, full_json=line)
    # initialize BERT model for generating embeddings for each user
    self.bert_model, self.tokenizer, self.device = self.init_bert_models()

  def init_bert_models(self):
    tokenizer = DistilBertTokenizer.from_pretrained(self.bert_model_name)
    model = DistilBertModel.from_pretrained(self.bert_model_name)

    if self.use_cuda and torch.cuda.is_available():
        print("using GPU")
        model.cuda()
        device = torch.device('cuda:0')
    else:
        print('using CPU')
        device = torch.device('cpu')
    return model, tokenizer, device

  def get_bert_embeddings(self, user_with_200_tweets):
    bert_embed_features = {}
    tmp_embed = []
    count = 0
    for tweet_text in user_with_200_tweets['texts']:
      count += 1
      if self.tweet_limit and count > self.tweet_limit:
        break
      sent = self.preprocess_text(tweet_text)
      input_ids = torch.tensor(self.tokenizer.encode(sent, add_special_tokens=True), device=self.device).unsqueeze(
        0)  # Batch size 1
      outputs = self.bert_model(input_ids)
      # NOTE: vector for last layer [cls] token. Since it's used for classification task
      tmp_embed.append(outputs[0][0][0].cpu().detach().numpy())
    bert_embed_features[user_with_200_tweets['user_id']] = self.average_embedding(tmp_embed)

    return bert_embed_features

  def process_multiple_tweets(self, user_with_200_tweets):
    _id = user_with_200_tweets['user_id']
    ## load/vectorize dataset
    if self.embed_dir and os.path.exists(os.path.join(self.embed_dir, '{}_embed.json.gz'.format(_id))):
      features = self.read_bert_embedding(os.path.join(self.embed_dir, '{}_embed.json.gz'.format(_id)))
    else:
      features = self.get_bert_embeddings(user_with_200_tweets)
      if self.embed_dir:
        self.write_bert_embeddings(_id=_id, embed=features)
    feats_data, feats_ids = self.vectorize(features)

    y_pred = self.logis_model.predict(feats_data)
    y_pred_probs = self.logis_model.predict_proba(feats_data)

    label_probs = {}
    for idx, num in enumerate(y_pred_probs[0]):
      label_probs[race_bert_back_mapping[idx+1]] = num

    ## output prediction result
    result = {"value":race_bert_back_mapping[y_pred[0]],
              "name": "eth_selfreport_bert",
              "setup": 'balanced',
              "annotator": "BERT Self-Report Ethnicity Classifier",
              "scores": label_probs}
    return {self.name_key: result}

  def write_bert_embeddings(self, _id, embed):
    with gzip.open(os.path.join(self.embed_dir, '{}_embed.json.gz'.format(_id)), 'w') as outf:
      outf.write("{}\n".format(json.dumps(embed, cls=NumpySerializer)).encode())

  @staticmethod
  def read_bert_embedding(embed_fn):
    with gzip.open(embed_fn, 'r') as inf:
      for line in inf:
        data = json.loads(line.strip().decode('utf8'))
    return data

  @staticmethod
  def average_embedding(embed_list):
    return np.mean(embed_list, axis=0)

  @staticmethod
  def vectorize(feature_dict):
    vecs = []
    user_ids = []
    for k, v in feature_dict.items():
      assert len(v) == 768, 'Inconsistent embedding size, it should be 768, but got {}'.format(len(v))
      vecs.append(v)
      user_ids.append(k)
    return vecs, user_ids

  @staticmethod
  def preprocess_text(text):
    return text.lower()


if __name__ == "__main__":
  users_with_200_tweets = []
  usernames = ['cd_hooks']
  for _user in usernames:
    users_with_200_tweets.append(read_tweet_text_from_timeline(user_id=_user, timeline_dir='data'))
  race_model = EthSelfReportBERTDemographer()
  for user_tweets in users_with_200_tweets:
    print(race_model.process_multiple_tweets(user_tweets))