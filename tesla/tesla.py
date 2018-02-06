#!/bin/python3

import argparse
import sys
import os.path as path
import os
import stat
import json

from page import Page, Evaluation
from common import nan
from htmldiff import HTMLDiff

pages = {}

def build_pages_list(directory):
    pages_path = path.join(directory, "pages.lst")
    with open(pages_path, 'r') as f:
        for page in f.readlines():
            page_name = page.split(" ")[0]
            pages[page_name] = Page(page_name)

def load_reports(directory):
    testers = os.listdir(directory)
    for tester in testers:  # For each tester
        if tester[0] != '.' and stat.S_ISDIR(os.stat(path.join(directory, tester)).st_mode):
            for result in os.listdir(path.join(directory, tester)):  # For each page that tester ran on
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
                    # VNU is a special case since it should always return 0, otherwise it isn't valid HTML
                    testers[tester]['live'] += 1
    for tester in testers.keys():
        testers[tester]['mutation_score'] = testers[tester]['live'] / float(mutants)


    stats = {"testers": testers, "mutant_pages": mutants}
    if output is not None:
        with open(output, 'w') as f:
            json.dump(stats, f)
    return stats

def check_equivalence(pages, report_object, output):
    equivalences = {}
    for page_name, page_data in report_object.items():
        equivalence = None
        if page_data['parent'] is not None:
            live = False
            for _, failures in page_data['failures'].items(): # For each failure found on the page
                if failures is not 0:
                    live = True
            if live:
                with open(path.join(pages, page_name)) as f:
                    mutant = f.readlines()
                with open(path.join(pages, page_data['parent'])) as f:
                    original = f.readlines()
                # Check that the HTML has been changed
                differ = HTMLDiff(original, mutant) 
                if differ.quick_ratio() < 1.0 or differ.ratio() < 1.0: 
                    # Non-equivalent page
                    if not path.exists(path.join(output, "results")):
                        os.mkdir(path.join(output, "results"))
                    with open(path.join(output, "results", page_name + ".diff"), 'w') as f:
                        f.write(differ.diff_table())
                    equivalence = False
                else:
                    # Equivalent
                    equivalence = True
            else:
                # Not live
                pass
        else:
            # Not an mutant
            pass
        equivalences[page_name] = equivalence
    if output is not None:
        with open(path.join(output, "equivalence.json"), 'w') as f:
            json.dump(equivalences, f)
    return equivalences
            

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
    equivalence = check_equivalence(argv.pages, report, argv.output)
