#!/bin/bash

# Script to install the models and formulas from the Model Checking Contest 2022


wget --no-check-certificate --progress=dot:mega https://mcc.lip6.fr/2022/archives/INPUTS-2022.tar.gz
tar -xvf INPUTS-2022.tar.gz
rm -v INPUTS-2022.tar.gz

cd INPUTS-2022
rm -v .DS_Store
ls *.tgz | xargs -n1 tar -xzvf
rm -v *.tgz
cd ..

echo "DONE"
