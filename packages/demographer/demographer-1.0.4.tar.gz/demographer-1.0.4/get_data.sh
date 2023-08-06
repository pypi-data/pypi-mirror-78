#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

mkdir $DIR/demographer/data/
mkdir $DIR/temp_data
pushd $DIR/temp_data
wget http://www.socialsecurity.gov/OACT/babynames/names.zip
unzip names.zip
rm names.zip
popd
