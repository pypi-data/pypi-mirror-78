#!/bin/bash

if [[ $# < 2 ]] ; then
    echo 'Usage: bash test_python23.sh <python2 virtualenv dir> <python3 virtualenv dir>'
    exit 0
fi

PYTHON_2_VENV=$1
PYTHON_3_VENV=$2

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

rm -rf $DIR/demographer/data
mkdir $DIR/demographer/data/
mkdir $DIR/temp_data
pushd $DIR/temp_data
wget http://www.socialsecurity.gov/OACT/babynames/names.zip
unzip names.zip
rm names.zip
popd
echo 'Testing python2'
echo $1
source activate $PYTHON_2_VENV
which python
python -m demographer.cli.create_census_gender --census-data-path $DIR/temp_data/ --output $DIR/demographer/data/census_gender_dct.p
python -m demographer.cli.train_gender_classifier --output $DIR/demographer/data/gender_classifier.p
python -m demographer.cli.process_tweets --input $DIR/data/faketweets.txt --output $DIR/data/out2.txtifier.p
source deactivate

echo 'Testing python3'
echo $2
source activate $PYTHON_3_VENV
which python
python -m demographer.cli.create_census_gender --census-data-path $DIR/temp_data/ --output $DIR/demographer/data/census_gender_dct.p
python -m demographer.cli.train_gender_classifier --output $DIR/demographer/data/gender_classifier.p
python -m demographer.cli.process_tweets --input $DIR/data/faketweets.txt --output $DIR/data/out3.txt
source deactivate

echo 'Data gathered and compiled, cleaning up files.'
rm -R $DIR/temp_data
echo 'Complete.'
