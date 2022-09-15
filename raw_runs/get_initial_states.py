#!/usr/bin/env python3

""" Get queries that are solved using the initial state by ITS-Tools.
    Output: initial_states.csv
"""

import csv
import glob
import os


def main():
    """ Main function.
    """
    with open('initial_states.csv', 'w') as fp_csv:
        writer = csv.writer(fp_csv)
        writer.writerow("INPUT,FORMULA")

        for examination in ['ReachabilityCardinality', 'ReachabilityFireability']:
            for path in glob.iglob('runs/**/BK_RESULTS/OUTPUTS/itstools_*_{}_*.stdout'.format(examination), recursive=True):
                
                filename = os.path.basename(path)
                instance = filename.split('_')[1]

                with open(path) as fp:
                    lines = fp.readlines()

                    for line in lines:
                        if 'INITIAL_STATE' in line:
                            writer.writerow([instance, line.split(' ')[1]])


if __name__=='__main__':
    main()
    print("DONE")
