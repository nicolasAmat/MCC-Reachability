#!/bin/bash

# Script to download the results of the Model Checking Contest 2022


wget --no-check-certificate --progress=dot:mega https://mcc.lip6.fr/archives/raw-result-analysis.csv.zip
unzip raw-result-analysis.csv.zip
rm -rv __MACOSX raw-result-analysis.csv.zip

echo "DONE"
