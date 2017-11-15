#!/bin/python3

import argparse
import sys
import os.path as path
import os
import stat
import json


nan = float('nan')

class Page:
    def __init__(self, page_name):
        self._page_name = page_name
        self._evaluations = {}

    def __repr__(self):
        return self.page_name() + " with evaluations " + \
            ", ".join(str(evaluation) for _, evaluation in self.evaluations().items())

    def page_name(self):
        return self._page_name

    def original_name(self):
        return self._page_name.split(".")[0] + "." + self._page_name.split(".")[-1]

    def applied_mutations(self):
        parts = self._page_name.split(".")
        mutations = []
        for i in range(1, len(parts) - 1, 2):
            mutations.append(parts[i])
        return mutations

    def mutant_order(self):
        return len(self.applied_mutations())

    def evaluations(self):
        return self._evaluations

    def add_evaluation(self, evaluation):
        self._evaluations[evaluation.tool()] = evaluation

class Evaluation:
    def __init__(self, tool, failure=nan, inconclusive=nan, success=nan, skipped=nan, ran=nan):
        self._tool = tool
        self._failure = failure
        self._inconclusive = inconclusive
        self._success = success
        self._skipped = skipped
        self._ran = ran

    def __repr__(self):
        return self.tool() + " with pass rate of " + str(self.success()/self.ran())

    def tool(self):
        return self._tool

    def failure(self):
        if self._failure is nan:
            return self.ran() - self.skipped() - self.success() - self.inconclusive()
        return self._failure

    def inconclusive(self):
        if self._inconclusive is nan:
            return self.ran() - self.skipped() - self.success() - self.failure()
        return self._inconclusive

    def success(self):
        if self._success is nan:
            return self.ran() - self.skipped() - self.failure() - self.inconclusive()
        return self._success

    def skipped(self):
        if self._skipped is nan:
            return self.ran() - self.failure() - self.success() - self.inconclusive()
        return self._skipped

    def ran(self):
        if self._ran is nan:
            return self.skipped() + self.success() + self.inconclusive() + self.failure()
        return self._ran


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

def print_stats(report_object):
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
    print(json.dumps(stats))


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="Analyses results of mutation tests")
    argparser.add_argument('reports', help="Path to directory containing all reports")
    argparser.add_argument('output', help="Path to location to save summary report", default=None)
    argv = argparser.parse_args(sys.argv[1:] if ".py" in sys.argv[0] else sys.argv)

    build_pages_list(argv.reports)
    load_reports(argv.reports)
    report = build_report(argv.output)
    print_stats(report)
