#!/bin/bash

# Script to install the raw data of SMPT from the Model Checking Contest 2022


wget --no-check-certificate --progress=dot:mega https://homepages.laas.fr/namat/media/smpt_2022.zip
unzip smpt_2022.zip
rm -v smpt_2022.zip
mv smtp/ smpt/

echo "DONE"
