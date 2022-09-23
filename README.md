# Oracles and Report for the Reachability category of the Model Checking Contest 

This repository includes scripts to generate oracles for the 2022 edition of the
Model Checking Contest for the Reachability category.  
The `raw_runs/` subdirectory also includes scripts to compute a 2022 edition report.

## Usage

Below you will find a description of the scripts with their corresponding use.

### Install inputs

To download the models and formulas run:
```
$ ./install_inputs.sh
```

To download the summary of the 2022 edition of Model Checking Contest run:
```
$ ./get_summary.sh
```

### Oracles

After installing the inputs, you can compute the oracles from the MCC by running
(it will automatically generates the `oracle/` sub-directory):
```
$ ./compute_oracles.py
```

### Filter instances

You can also filter the formulas that are computed using some counterexamples (EF F
true or AG F false), or by proving an invariant (AG F true or EF F false) by running:
```
$ ./filter_inputs.sh [--cex | --inv] [--exclude-initial-states]
```
It will generates new ReachabilityCardinality and ReachabilityFireability files
suffixed with `_CEX.xml` or `_INV.xml`. 

The `--exclude` option permits to exclude some properties. For instance to
exclude properties for which the initial states is trivially a counterexample
you can compute the `initial_states.csv` file (see after) and use `--exclude
raw_runs/initial_states.csv`.

### MCC 2022 report

To obtain a report on the MCC 2022 and the methods used by SMPT to compute the
queries, go to the `raw_runs/` directory (`cd raw_runs/`).

To download the raw data from the MCC 2022 run:
```
$ ./install_runs.sh
```

To obtain the methods used by SMPT to compute the queries run (it will
automatically generates the `summary_methods.csv` file):
```
$ ./get_methods.py
```

To obtain the queries that are computed by only checking the initial state runs
(it will automatically generates the `summary_methods.csv` file):
```
$ ./get_initial_states.py
```

To obtain a report on the MCC 2022 for the Reachability category run:
```
$ ./resume.py
```

After some time of computation you will obtain some data from the MCC that
compare the different tools competing in the reachability category.