
#!/usr/bin/env bash

#python -m demographer.cli.create_ind_org_dict --input data/training_data/full_train.json --output data/dictionary/full_train_dict.p  --create_transformer True --transformer_filename data/full_transformer.p
#python -m demographer.cli.create_ind_org_dict --input data/training_data/full_dev.json --output data/dictionary/full_dev_dict.p
#python -m demographer.cli.train_ind_org_classifier --train_dict data/dictionary/full_train_dict.p --dev_dict data/dictionary/full_dev_dict.p --transformer_filename data/full_transformer.p --output data/full_classifier.p
#
#python -m demographer.cli.create_ind_org_dict --input data/training_data/balanced_train.json --output data/dictionary/balanced_train_dict.p  --create_transformer True --transformer_filename data/balanced_transformer.p
#python -m demographer.cli.create_ind_org_dict --input data/training_data/balanced_dev.json --output data/dictionary/balanced_dev_dict.p
#python -m demographer.cli.train_ind_org_classifier --train_dict data/dictionary/balanced_train_dict.p --dev_dict data/dictionary/balanced_dev_dict.p --transformer_filename data/balanced_transformer.p --output data/balanced_classifier.p

#python -m demographer.cli.create_ind_org_dict --input data/training_data/balanced_train.json --output data/dictionary/balanced_train_dict.p
#python -m demographer.cli.create_ind_org_dict --input data/training_data/balanced_dev.json --output data/dictionary/balanced_dev_dict.p
python -m demographer.cli.train_ind_org_classifier --train_dict data/dictionary/balanced_train_dict.p --dev_dict data/dictionary/balanced_dev_dict.p --transformer_filename data/full_transformer.p --output data/balanced_classifier_full_t.p

#python -m demographer.cli.create_ind_org_dict --input data/training_data/full_train.json --output data/dictionary/full_train_dict.p
#python -m demographer.cli.create_ind_org_dict --input data/training_data/full_dev.json --output data/dictionary/full_dev_dict.p
python -m demographer.cli.train_ind_org_classifier --train_dict data/dictionary/full_train_dict.p --dev_dict data/dictionary/full_dev_dict.p --transformer_filename data/balanced_transformer.p --output data/full_classifier_balanced_t.p