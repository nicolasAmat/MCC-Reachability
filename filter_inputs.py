#!/usr/bin/env python3

"""
Filter CEX or INV formulas.
"""

import argparse
import xml.etree.ElementTree as ET

import pandas


def main():
    """ Main function.
    """
    # Arguments parser
    parser = argparse.ArgumentParser(description='MCC oracles')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('--cex',
                       action='store_true',
                       help="Filter counterexamples")

    group.add_argument('--inv',
                       action='store_true',
                       help="Filter invariants")

    parser_results = parser.parse_args()

    path_inputs = "INPUTS-2022/"
    path_summary = "raw-result-analysis.csv"

    df = pandas.read_csv(path_summary, usecols=[
                         "### tool", "Input", "Examination", "estimated result"])
    df.columns = ['Tool', 'Input', 'Examination', 'Verdict']
    df.query("Tool == 'smpt' and (Examination == 'ReachabilityCardinality' or Examination == 'ReachabilityFireability')", inplace=True)

    kinds = []

    for input in set(df['Input']):
        for examination in ['ReachabilityCardinality', 'ReachabilityFireability']:
            verdicts = df.query('Input == "{}" and Examination == "{}"'.format(
                input, examination)).iloc[0]['Verdict'].replace(' ',  '')

            ET.register_namespace('', "http://mcc.lip6.fr/")
            tree = ET.parse(
                "{}/{}/{}.xml".format(path_inputs, input, examination))

            root = tree.getroot()
            for property_xml, verdict in zip(list(root), verdicts):
                _, _, kind = property_xml[2][0].tag.rpartition('}')

                if verdict == "?":
                    if parser_results.cex or parser_results.inv:
                        root.remove(property_xml)

                elif (kind == "exists-path" and verdict == "T") or (kind == "all-paths" and verdict == "F"):
                    if parser_results.inv:
                        root.remove(property_xml)

                else:
                    if parser_results.cex:
                        root.remove(property_xml)

            if parser_results.cex:
                tree.write('{}/{}/{}_CEX.xml'.format(path_inputs, input,
                           examination), encoding="utf-8", xml_declaration=True)

            if parser_results.inv:
                tree.write('{}/{}/{}_INV.xml'.format(path_inputs, input,
                           examination), encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
    print("DONE")
    exit(0)
