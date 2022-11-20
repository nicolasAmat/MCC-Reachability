#!/bin/bash

# Script to install the raw runs from the Model Checking Contest 2022

mkdir -p runs/
wget --no-check-certificate --progress=dot:mega https://mcc.lip6.fr/2022/archives/MCC-2022-raw-data.tar.gz -P runs/

cd runs

tar xf MCC-2022-raw-data.tar.gz
rm MCC-2022-raw-data.tar.gz
rm -r */BK_RESULTS/CSV
rm -r */BK_RESULTS/CONFIGURATIONS

cd ..

echo "DONE"
