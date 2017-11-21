#!/bin/python3

import argparse
import sys
import os.path as path
import os
import stat
import json

from page import Page, Evaluation
from common import nan

pages = {}

def build_pages_list(directory):
    pages_path = path.join(directory, "pages.lst")
    with open(pages_path, 'r') as f:
        for page in f.readlines():
            page_name = page.split(" ")[0]
            pages[page_name] = Page(page_name)

def load_reports(directory):
    testers = os.listdir(directory)
    for tester in testers:
        if tester[0] != '.' and stat.S_ISDIR(os.stat(path.join(directory, tester)).st_mode):
            for result in os.listdir(path.join(directory, tester)):
                with open(path.join(directory, tester, result)) as f:
                    json_data = json.load(f)
                    page_name = ".".join(result.split(".")[:-1])
                    if page_name in pages.keys():
                        pages[page_name].add_evaluation(Evaluation(
                            tester,
                            failure=len(json_data['violations']),
                            success=len(json_data['passes']),
                            inconclusive=len(json_data['incomplete']),
                            skipped=len(json_data['inapplicable'])
                        ))

def build_report(output):
    pages_output = {}
    for page_name, page_data in pages.items():
        failures = {}
        for tool, evaluation in page_data.evaluations().items():
            failures[tool] = evaluation.failure()
        pages_output[page_name] = {
            "failures": failures,
            "mutations": page_data.applied_mutations(),
            "parent": page_data.original_name() if page_data.original_name() != page_name else None,
            "valid": page_data.evaluations()['vnu'].failure() == 0 if 'vnu' in page_data.evaluations().keys() else None
        }
    if output is not None:
        with open(output, 'w') as f:
            json.dump(pages_output, f)
    return pages_output

def build_stats(report_object, output):
    testers = {}
    mutants = 0

    for _, page in report_object.items():
        if page['parent'] is not None:
            mutants += 1
            for tester, failure in page['failures'].items():
                if tester not in testers.keys():
                    testers[tester] = {"live": 0, "mutation_score": nan}
                if (failure is 0 and report_object[page['parent']]['failures'][tester] is 0 and tester != 'vnu') or (tester == "vnu" and failure is not 0):
                    testers[tester]['live'] += 1
    for tester in testers.keys():
        testers[tester]['mutation_score'] = testers[tester]['live'] / float(mutants)


    stats = {"testers": testers, "mutant_pages": mutants}
    if output is not None:
        with open(output, 'w') as f:
            json.dump(stats, f)
    return stats


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="Analyses results of mutation tests")
    argparser.add_argument('pages', help="Path to directory containing all pages")
    argparser.add_argument('reports', help="Path to directory containing all reports")
    argparser.add_argument('output', help="Path to directory to save output", default=None)
    argv = argparser.parse_args(sys.argv[1:] if ".py" in sys.argv[0] else sys.argv)

    build_pages_list(argv.reports)
    load_reports(argv.reports)
    report = build_report(path.join(argv.output, "summary.json"))
    stats = build_stats(report, path.join(argv.output, "stats.json"))
