#!/usr/bin/env python3

""" Generates summary_methods.csv containing the methods used by SMPT during the Model Checking Contest 2022.
"""

import glob
import os
import pandas


def main():
    """ Main function.
    """
    methods = {"WALK": 0, "STATE_EQUATION": 0, "BMC": 0, "K-INDUCTION": 0,
               "PDR-REACH-SATURATED": 0, "PDR-COV": 0, "SAT-SMT": 0}
    summary = []

    for examination in ['ReachabilityCardinality', 'ReachabilityFireability']:
        for path in glob.iglob('runs/**/BK_RESULTS/OUTPUTS/smpt_*_{}_*.stdout'.format(examination), recursive=True):

            with open(path, 'r') as fp:

                for line in fp.read().splitlines():
                    if "FORMULA " not in line:
                        continue

                    split_line = line.split(' ')
                    method = split_line[-1]
                    formula = split_line[1]

                    if method in ["USE_NUPN", "TOPOLIGICAL"]:
                        method = "STATE_EQUATION"

                    methods[method] += 1

                    summary.append([os.path.basename(path).split('_')[1], formula, method])

    df = pandas.DataFrame(summary, columns=["INPUT", "FORMULA", "METHOD"])
    df.to_csv("summary_methods.csv", index=False)

    for method, count in methods.items():
        print(method, "-", count)


if __name__ == "__main__":
    main()
    print("DONE")
    exit(0)
