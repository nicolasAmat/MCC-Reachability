#!/usr/bin/env python3

""" Resume of the Model Checking Contest 2022.
"""

from itertools import chain, combinations

import pandas
from alive_progress import alive_bar


def powerset(tools):
    return chain.from_iterable(combinations(tools, r) for r in range(len(tools)+1))


def main():
    """ Main function.
    """
    tools = ["smpt", "Tapaal", "ITS-Tools", "GreatSPN"]

    df_results = pandas.read_csv(
        "../raw-result-analysis.csv", usecols=["### tool", "Input", "Examination", "flags:bonus:scores:mask"])
    df_results.columns = ['Tool', 'Input', 'Examination', 'Verdict']

    df_kinds = pandas.read_csv("../kinds.csv")
    df_kinds.columns = ['Input', 'Formula', 'Kind']

    queries = []
    answers = {tool: [] for tool in tools}


    print("Retrieve data...")
    with alive_bar(len(set(df_results['Input']))) as bar:

        for input in set(df_results['Input']):

            for examination in ['ReachabilityCardinality', 'ReachabilityFireability']:

                queries += ["{}-{}-{:02d}".format(input, examination, index)
                            for index in range(16)]

                for tool in tools:
                    verdicts = df_results.query('Tool == "{}" and Input == "{}" and Examination == "{}"'.format(
                        tool, input, examination)).iloc[0]['Verdict'].split(":")[-1]

                    if len(verdicts) == 1:
                        answers[tool] += [False for _ in range(16)]
                    else:
                        if len(verdicts) != 16:
                            raise ValueError
                        answers[tool] += [verdict == "T"
                                          for verdict in verdicts]
            bar()

    print("Compute summary...")

    print(">>>")

    tools = ["smpt", "Tapaal", "ITS-Tools"]

    for combo in powerset(["smpt", "Tapaal", "ITS-Tools"]):
        if combo:
            combo_answers = [all(i) for i in zip(
                *[answers[tool] for tool in combo])]
            formulas = [formula for formula, only in zip(
                queries, combo_answers) if only]
            kinds = [df_kinds.query('Formula == "{}"'.format(
                formula)).iloc[0]['Kind'] for formula in formulas]
            print('> All', ' & '.join(combo) + ':', sum(combo_answers))
            kinds = pandas.Series(kinds).value_counts()
            print(kinds)

    print(">>>")

    for combo in powerset(["smpt", "Tapaal", "ITS-Tools"]):
        if combo and len(combo) < len(tools):
            combo_answers = [all(i) for i in zip(
                *[answers[tool] for tool in combo])]
            other_answers = [any(i) for i in zip(
                *[answers[tool] for tool in tools if tool not in combo])]
            combo_answers = [i and (not j)
                             for i, j in zip(combo_answers, other_answers)]

            formulas = [formula for formula, only in zip(
                queries, combo_answers) if only]
            kinds = [df_kinds.query('Formula == "{}"'.format(
                formula)).iloc[0]['Kind'] for formula in formulas]
            print('> Only', ' & '.join(combo) + ':', sum(combo_answers))
            kinds = pandas.Series(kinds).value_counts()
            print(kinds)

    print(">>>")


if __name__ == "__main__":
    main()
    print("DONE")
    exit(0)
