#!/usr/bin/env python3

"""
Script to compute oracles from the summary files of the Model Checking Contest,
and filter CEX or INV formulas.
"""

import argparse
from importlib.resources import path
import pandas
import xml.etree.ElementTree as ET

def main():
    """ Main function.
    """
    # Arguments parser
    parser = argparse.ArgumentParser(description='MCC oracles')

    parser.add_argument('path_summary',
                        metavar='summary',
                        type=str,
                        help='path to summary .csv file')

    parser.add_argument('path_inputs',
                        metavar='inputs',
                        type=str,
                        help='path to INPUTS-2022 directory')

    parser.add_argument('path_oracles',
                        metavar='oracles',
                        type=str,
                        help='path to oracles directory')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('--cex',
                       action='store_true',
                       help="Filter counterexamples")

    group.add_argument('--inv',
                       action='store_true',
                       help="Filter invariants")

    parser_results = parser.parse_args()

    abrev = {'ReachabilityCardinality': 'RC', 'ReachabilityFireability': 'RF'}
    answer = {'T': 'TRUE', 'F': 'FALSE', '?': 'UNKNOWN'}

    unknown, cex, inv = 0, 0, 0

    df = pandas.read_csv(parser_results.path_summary, usecols=["### tool", "Input", "Examination", "estimated result"])
    df.columns = ['Tool', 'Input', 'Examination', 'Verdict']
    df.query("Tool == 'smpt' and (Examination == 'ReachabilityCardinality' or Examination == 'ReachabilityFireability')", inplace=True)
    
    for input in df['Input']:
        for examination in ['ReachabilityCardinality', 'ReachabilityFireability']:
            with open(parser_results.path_oracles + '/{}-{}.out'.format(input, abrev[examination]), 'w') as fp:
                fp.write("{} {}\n".format(input, examination))
                verdicts = df.query('Input == "{}" and Examination == "{}"'.format(input, examination)).iloc[0]['Verdict'].replace(' ',  '')

                ET.register_namespace('', "http://mcc.lip6.fr/")
                tree = ET.parse("{}/{}/{}.xml".format(parser_results.path_inputs, input, examination))
                
                root = tree.getroot()
                for index, (property_xml, verdict) in enumerate(zip(root, verdicts)):
                    _, _, kind = property_xml[2][0].tag.rpartition('}')
                    
                    if verdict == "?":
                        unknown += 1
                        if parser_results.cex or parser_results.inv:
                            root.remove(property_xml)
                    elif (kind == "exists-path" and verdict == "T") or (kind == "all-paths" and verdict == "F"):
                        cex += 1
                        if parser_results.inv:
                            root.remove(property_xml)
                    else:
                        inv += 1
                        if parser_results.inv:
                            root.remove(property_xml)
                
                    fp.write("FORMULA {}-{}-{:02d} {} TECHNIQUES ORACLE2022\n".format(input, examination, index, answer[verdict]))

                if parser_results.cex:
                    tree.write('{}/{}/{}_CEX.xml'.format(parser_results.path_inputs, input, examination), encoding="utf-8", xml_declaration=True)
                if parser_results.inv:
                    tree.write('{}/{}/{}_INV.xml'.format(parser_results.path_inputs, input, examination), encoding="utf-8", xml_declaration=True)


    print("STATS\n-----")
    print("Unknown:", unknown)
    print("Cex:", cex)
    print("Inv:", inv)
    print("Total:", unknown + cex + inv)

if __name__ == "__main__":
    main()
    print("DONE")
    exit(0)