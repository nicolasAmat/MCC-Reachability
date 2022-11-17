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


    parser.add_argument('--cex',
                       action='store_true',
                       help="Filter counterexamples")

    parser.add_argument('--inv',
                       action='store_true',
                       help="Filter invariants")

    parser.add_argument('--include',
                        dest='path_include',
                        type=str,
                        help="Path to included properties (.csv format)")

    parser.add_argument('--exclude',
                        dest='path_exclude',
                        type=str,
                        help="Path to excluded properties (.csv format)")

    parser_results = parser.parse_args()

    path_inputs = "INPUTS-2022/"
    path_summary = "raw-result-analysis.csv"

    df = pandas.read_csv(path_summary, usecols=[
                         "### tool", "Input", "Examination", "estimated result"])
    df.columns = ['Tool', 'Input', 'Examination', 'Verdict']
    df.query("Tool == 'smpt' and (Examination == 'ReachabilityCardinality' or Examination == 'ReachabilityFireability')", inplace=True)

    if parser_results.path_include:
        df_include = pandas.read_csv(parser_results.path_include)
        df_include.columns = ['Input', 'Formula']
    else:    
        df_include = None

    if parser_results.path_exclude:
        df_exclude = pandas.read_csv(parser_results.path_exclude)
        df_exclude.columns = ['Input', 'Formula']
    else:    
        df_exclude = None

    for input in set(df['Input']):
        for examination in ['ReachabilityCardinality', 'ReachabilityFireability']:
            verdicts = df.query('Input == "{}" and Examination == "{}"'.format(
                input, examination)).iloc[0]['Verdict'].replace(' ',  '')

            ET.register_namespace('', "http://mcc.lip6.fr/")
            tree = ET.parse(
                "{}/{}/{}.xml".format(path_inputs, input, examination))

            root = tree.getroot()
            for property_xml, verdict in zip(list(root), verdicts):
                formula = property_xml[0].text
                _, _, kind = property_xml[2][0].tag.rpartition('}')

                if parser_results.path_include and not (df_include['Formula'] == formula).any():
                    root.remove(property_xml)
                elif parser_results.path_exclude and (df_exclude['Formula'] == formula).any():
                    root.remove(property_xml)
                elif verdict == "?" and (parser_results.cex or parser_results.inv):
                    root.remove(property_xml)
                elif parser_results.inv and ((kind == "exists-path" and verdict == "T") or (kind == "all-paths" and verdict == "F")):
                    root.remove(property_xml)
                elif parser_results.cex and ((kind == "exists-path" and verdict == "F") or (kind == "all-paths" and verdict == "T")):
                    root.remove(property_xml)

            if parser_results.cex:
                tree.write('{}/{}/{}_CEX.xml'.format(path_inputs, input,
                           examination), encoding="utf-8", xml_declaration=True)

            elif parser_results.inv:
                tree.write('{}/{}/{}_INV.xml'.format(path_inputs, input,
                           examination), encoding="utf-8", xml_declaration=True)

            elif parser_results.path_include:
                tree.write('{}/{}/{}_INCLUDED.xml'.format(path_inputs, input,
                           examination), encoding="utf-8", xml_declaration=True)

            elif parser_results.path_excluded:
                tree.write('{}/{}/{}_EXCLUDED.xml'.format(path_inputs, input,
                           examination), encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
    print("DONE")
    exit(0)
