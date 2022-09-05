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
        "../raw-result-analysis.csv", usecols=["### tool", "Input", "Examination", "results"])
    df_results.columns = ['Tool', 'Input', 'Examination', 'Verdict']

    df_methods = pandas.read_csv("summary_methods.csv")
    df_methods.columns = ['Input', 'Formula', 'Method']

    df_kinds = pandas.read_csv("../kinds.csv")
    df_kinds.columns = ['Input', 'Formula', 'Kind']

    queries = []
    answers = {tool: [] for tool in tools}

    exclude = {
        "ReachabilityCardinality": ["CSRepetitions-PT-03",
                                    "CSRepetitions-COL-03",
                                    "CSRepetitions-PT-04",
                                    "CSRepetitions-COL-04",
                                    "SafeBus-PT-20",
                                    "SafeBus-COL-20",
                                    "UtilityControlRoom-PT-Z2T4N02",
                                    "UtilityControlRoom-COL-Z2T4N02",
                                    "UtilityControlRoom-PT-Z2T4N08",
                                    "UtilityControlRoom-COL-Z2T4N08",
                                    "UtilityControlRoom-PT-Z2T4N10",
                                    "UtilityControlRoom-COL-Z2T4N10",
                                    "UtilityControlRoom-PT-Z4T3N06",
                                    "UtilityControlRoom-COL-Z4T3N06",
                                    "UtilityControlRoom-PT-Z4T4N06",
                                    "UtilityControlRoom-COL-Z4T4N06"],
        "ReachabilityFireability": ["PermAdmissibility-PT-01",
                                    "PermAdmissibility-COL-01",
                                    "PermAdmissibility-PT-02",
                                    "PermAdmissibility-COL-02",
                                    "UtilityControlRoom-PT-Z2T3N10",
                                    "UtilityControlRoom-COL-Z2T3N10",
                                    "UtilityControlRoom-PT-Z2T4N04",
                                    "UtilityControlRoom-COL-Z2T4N04",
                                    "UtilityControlRoom-PT-Z2T4N06",
                                    "UtilityControlRoom-COL-Z2T4N06"]
    }

    print("Retrieve data...")
    with alive_bar(len(set(df_results['Input']))) as bar:

        for input in set(df_results['Input']):

            for examination in ['ReachabilityCardinality', 'ReachabilityFireability']:

                if input in exclude[examination]:
                    continue

                queries += ["{}-{}-{:02d}".format(input, examination, index)
                            for index in range(16)]

                for tool in tools:
                    verdicts = df_results.query('Tool == "{}" and Input == "{}" and Examination == "{}"'.format(
                        tool, input, examination)).iloc[0]['Verdict']

                    if verdicts in ["DNF", "DNC", "CC"]:
                        answers[tool] += [False for _ in range(16)]
                    else:
                        answers[tool] += [verdict in ["T", "F"]
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

    print("All smpt methods")

    formulas = [formula for formula, verdict in zip(
        queries, answers["smpt"]) if verdict]
    methods = [df_methods.query('Formula == "{}"'.format(
        formula)).iloc[0]['Method'] for formula in formulas]
    counts = pandas.Series(methods).value_counts()
    print(counts)

    print(">>>")

    print("Only smpt methods")

    only_smpt = [a & (not any(i)) for a, i in zip(answers["smpt"], zip(
        *[answers[other_tool] for other_tool in tools if other_tool != "smpt"]))]
    formulas = [formula for formula, only in zip(queries, only_smpt) if only]
    methods = [df_methods.query('Formula == "{}"'.format(
        formula)).iloc[0]['Method'] for formula in formulas]
    counts = pandas.Series(methods).value_counts()
    print(counts)

    print(">>>")


if __name__ == "__main__":
    main()
    print("DONE")
    exit(0)
