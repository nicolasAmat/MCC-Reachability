# Oracles and Report for the Reachability category of the Model Checking Contest 

This repository includes scripts to generate oracles for the 2022 edition of the
Model Checking Contest for the Reachability category. The `smpt/` subdirectory
also includes scripts to run a 2022 edition report.

## Usage

Below you will find a description of the scripts with their corresponding use.

### Install inputs

To download the models and formulas run:
```
$> ./install_inputs.sh
```

To download the summary of the 2022 edition of Model Checking Contest run:
```
$> ./get_summary.sh
```

### Oracles

After installing the inputs, you can compute the oracles from the MCC by running:
```
$> ./compute_oracles.py
```

### Filter instances

You can also filter the formulas that are found using some counterexamples (EF F
true or AG F false), or by proving an invariant (AG F true or EF F false) by running:
```
$> ./filter_inputs.sh [--cex | --inv]
```
It will generates new ReachabilityCardinality and ReachabilityFireability files
suffixed with `_CEX.xml` or `_INV.xml`. 

### MCC 2022 report

To get a report on the MCC 2022 and to also get the methods used by SMPT to
compute the queries, go to the `smpt/` directory (`cd smpt/`).

Next, run:
`./get_methods.py` followed by `./resume.py`.

After some time of computation you will obtain some data from the MCC that
compare the different tools competing in the reachability category.