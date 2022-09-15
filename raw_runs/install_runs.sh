#!/bin/bash

# Script to install the raw runs from the Model Checking Contest 2022

mkdir -p runs/
wget --no-check-certificate --progress=dot:mega https://mcc.lip6.fr/archives/MCC-2022-raw-data.tar.gz -P runs/
tar xvf runs/MCC-2022-raw-data.tar.gz
rm -v runs/MCC-2022-raw-data.tar.gz

echo "DONE"
