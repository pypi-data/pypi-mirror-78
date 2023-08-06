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
source $PYTHON_2_VENV/bin/activate
python -m demographer.cli.create_census_gender --census-data-path $DIR/temp_data/
python -m demographer.cli.train_gender_classifier
python -m demographer.cli.process_tweets --input $DIR/data/faketweets.txt --output $DIR/data/out2.txt
deactivate

echo 'Testing python3'
source $PYTHON_3_VENV/bin/activate
python -m demographer.cli.create_census_gender --census-data-path $DIR/temp_data/
python -m demographer.cli.train_gender_classifier
python -m demographer.cli.process_tweets --input $DIR/data/faketweets.txt --output $DIR/data/out3.txt
deactivate

echo 'Data gathered and compiled, cleaning up files.'
rm -R $DIR/temp_data
echo 'Complete.'
