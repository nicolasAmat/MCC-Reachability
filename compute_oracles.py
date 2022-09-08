#!/usr/bin/env python3

"""
Script to compute oracles from the summary files of the Model Checking Contest.
Also generates kinds.csv, containing whether the verdict is obtained by using a counterexample (EF F true or AG F false) or by proving an invariant (AG F true or EF F false).
"""

import xml.etree.ElementTree as ET

import pandas


def main():
    """ Main function.
    """
    path_inputs = "INPUTS-2022/"
    path_oracles = "oracles/"
    path_summary = "raw-result-analysis.csv"
    path_kinds = "kinds.csv"

    abreviation = {'ReachabilityCardinality': 'RC',
                   'ReachabilityFireability': 'RF'}
    verdict_mapping = {'T': 'TRUE', 'F': 'FALSE', '?': 'UNKNOWN'}

    unknown, cex, inv = 0, 0, 0

    df = pandas.read_csv(path_summary, usecols=[
                         "### tool", "Input", "Examination", "estimated result"])
    df.columns = ['Tool', 'Input', 'Examination', 'Verdict']
    df.query("Tool == 'smpt' and (Examination == 'ReachabilityCardinality' or Examination == 'ReachabilityFireability')", inplace=True)

    kinds = []

    for input in set(df['Input']):
        for examination in ['ReachabilityCardinality', 'ReachabilityFireability']:
            with open(path_oracles + '/{}-{}.out'.format(input, abreviation[examination]), 'w') as fp:
                fp.write("{} {}\n".format(input, examination))
                verdicts = df.query('Input == "{}" and Examination == "{}"'.format(
                    input, examination)).iloc[0]['Verdict'].replace(' ',  '')

                ET.register_namespace('', "http://mcc.lip6.fr/")
                tree = ET.parse(
                    "{}/{}/{}.xml".format(path_inputs, input, examination))

                root = tree.getroot()
                for index, (property_xml, verdict) in enumerate(zip(root, verdicts)):
                    _, _, kind = property_xml[2][0].tag.rpartition('}')

                    if verdict == "?":
                        kind = "Unknown"
                        unknown += 1

                    elif (kind == "exists-path" and verdict == "T") or (kind == "all-paths" and verdict == "F"):
                        kind = "Cex"
                        cex += 1

                    else:
                        kind = "Inv"
                        inv += 1

                    formula = "{}-{}-{:02d}".format(input, examination, index)
                    fp.write("FORMULA {} {} TECHNIQUES ORACLE2022\n".format(
                        formula, verdict_mapping[verdict]))
                    kinds.append([input, formula, kind])

    df_kinds = pandas.DataFrame(kinds, columns=["INPUT", "FORMULA", "KIND"])
    df_kinds.to_csv(path_kinds, index=False)

    print("STATS\n-----")
    print("Unknown:", unknown)
    print("Cex:", cex)
    print("Inv:", inv)
    print("Total:", unknown + cex + inv)


if __name__ == "__main__":
    main()
    print("DONE")
    exit(0)
