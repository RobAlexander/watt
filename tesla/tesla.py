#!/bin/python3

import argparse
import sys
import os.path as path
import os
import stat
import json
import csv

from page import Page, Evaluation
from common import nan, make_resource
from htmldiff import HTMLDiff
from page_set import pages_table
import speed

pages = {}
pages_checksum = {}

def build_pages_list(directory):
    pages_path = path.join(directory, "pages.lst")
    with open(pages_path, 'r') as f:
        for page in f.readlines():
            page_parts = page.split(" ")
            page_name = page_parts[0]
            pages[page_name] = Page(page_name)
            pages_checksum[page_name] = page_parts[1] if len(page_parts) > 1 else None

def load_reports(directory, page_ignores=None, tester_ignores=None):
    if page_ignores is None:
        page_ignores = {}
    if tester_ignores is None:
        tester_ignores = {}
    testers = os.listdir(directory)
    for tester in testers:  # For each tester
        if tester[0] != '.' and stat.S_ISDIR(os.stat(path.join(directory, tester)).st_mode):
            for result in os.listdir(path.join(directory, tester)):  # For each page that tester ran on
                with open(path.join(directory, tester, result)) as f:
                    json_data = json.load(f)
                    page_name = ".".join(result.split(".")[:-1])
                    if page_name in pages.keys():
                        ignores = []
                        if tester in tester_ignores.keys():
                            ignores = tester_ignores[tester]
                        parent_page_name = page_name[0]
                        if parent_page_name in page_ignores.keys() and tester in page_ignores[parent_page_name].keys():
                            ignores.extend(page_ignores[parent_page_name][tester])
                        violation_count = 0
                        for violation in json_data['violations']:
                            if violation['description'] not in ignores:
                                violation_count += 1
                        pages[page_name].add_evaluation(Evaluation(
                            tester,
                            failure=violation_count,
                            success=len(json_data['passes']),
                            inconclusive=len(json_data['incomplete']),
                            skipped=len(json_data['inapplicable'])
                        ))

def load_ignores(pages_file, testers):
    # Pages Ignores
    with open(pages_file) as f:
        page_ignores = json.load(f)
    # Tester Ignores
    tester_ignores = {}
    tester_ignores_dir = os.path.join(os.path.dirname(__file__), "tester_ignores")
    for tester in testers:
        tester_ignores[tester] = []
        tester_ignore_path = os.path.join(tester_ignores_dir, tester + ".txt")
        if os.path.exists(tester_ignore_path):
            with open(tester_ignore_path) as f:
                tester_ignores[tester] = f.readlines()
    return page_ignores, tester_ignores


def build_results_csv(directory, output):
    testers = pages[list(pages.keys())[0]].evaluations().keys()
    with open(path.join(output, 'all.csv'), 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['.PageName'] + [tester + ".Error" for tester in testers] + [tester  + ".Warning" for tester in testers])
        for page_name, page in pages.items():
            writer.writerow([page_name] + [page.evaluations()[tester].failure() for tester in testers] + [page.evaluations()[tester].inconclusive() for tester in testers])
    for tester in testers:
        tester_errors = {}
        tester_warning = {}
        for page_name, page in pages.items():
            with open(path.join(directory, tester, page_name + ".json")) as f:
                json_data = json.load(f)
                for failure in json_data['violations']:
                    if failure['description'] not in tester_errors.keys():
                        tester_errors[failure['description']] = {page_name: 1}
                    elif page_name not in tester_errors[failure['description']].keys():
                        tester_errors[failure['description']][page_name] = 1
                    else:
                        tester_errors[failure['description']][page_name] += 1
                for warning in json_data['incomplete']:
                    if warning['description'] not in tester_warning.keys():
                        tester_warning[warning['description']] = {page_name: 1}
                    elif page_name not in tester_warning[warning['description']].keys():
                        tester_warning[warning['description']][page_name] = 1
                    else:
                        tester_warning[warning['description']][page_name] += 1
        error_list = tester_errors.keys()
        warning_list = tester_warning.keys()
        with open(path.join(output, tester + ".csv"), 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['.PageName'] + [error + "(Error)" for error in error_list] + [warning + "(Warning)" for warning in warning_list])
            for page_name, page in pages.items():
                writer.writerow([page_name] + [(tester_errors[error][page_name] if page_name in tester_errors[error].keys() else 0) for error in error_list] + [(tester_warning[warning][page_name] if page_name in tester_warning[warning].keys() else 0) for warning in warning_list])

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

def build_stats(report_object, equivalents, dupes, output):
    testers = {}
    mutants = 0

    for page_name, page in report_object.items():
        if page_name not in dupes and not equivalents[page_name]:  # Don't do anything with duplicates or equivalents
            if page['parent'] is not None:
                mutants += 1
                for tester, failure in page['failures'].items():
                    if tester not in testers.keys():
                        testers[tester] = {"live": 0, "dead": 0, "mutation_score": nan, "operators": {}}
                    for mutation in page["mutations"]:
                        if mutation not in testers[tester]["operators"].keys():
                            testers[tester]["operators"][mutation] = {"live": 0, "dead": 0, "mutation_score": nan}
                    # VNU is a special case since it should always return 0, otherwise it isn't valid HTML
                    if ((failure is 0 or report_object[page['parent']]['failures'][tester] < failure) and tester != 'vnu') or (tester == "vnu" and failure is not 0):
                        testers[tester]['live'] += 1
                        for mutation in page["mutations"]:
                            testers[tester]["operators"][mutation]["live"] += 1
                    else:
                        testers[tester]['dead'] += 1
                        for mutation in page["mutations"]:
                            testers[tester]["operators"][mutation]["dead"] += 1
    for tester in testers.keys():
        testers[tester]['mutation_score'] = testers[tester]['dead'] / float(mutants)
        for mutation in testers[tester]["operators"].keys():
            testers[tester]["operators"][mutation]["mutation_score"] = testers[tester]["operators"][mutation]["dead"] / (testers[tester]["operators"][mutation]["dead"] + testers[tester]["operators"][mutation]["live"])


    stats = {"testers": testers, "mutant_pages": mutants}
    if output is not None:
        with open(output, 'w') as f:
            json.dump(stats, f)
    return stats

def stats_mutation_table(stats, table_tex_file="tester_score.tex"):
    make_resource("tester_score.tex.jinja2", table_tex_file,
                  testers=sorted(stats["testers"].keys()), stats=stats["testers"]
                 )

def stats_operator_table(stats, table_tex_file="operator_score.tex"):
    scores = {}
    averages = {}
    for tester, tester_stats in stats["testers"].items():
        for operator, operator_stats in tester_stats["operators"].items():
            if operator not in scores.keys():
                scores[operator] = {}
            scores[operator][tester] = operator_stats["mutation_score"]
    for operator, operator_scores in scores.items():
        total = 0
        for tester, score in operator_scores.items():
            total += score
        averages[operator] = total / len(operator_scores)
    make_resource("operator_score.tex.jinja2", table_tex_file,
                  operators=sorted(scores.keys()), testers=sorted(stats["testers"].keys()),
                  scores=scores, averages=averages
                 )

def page_mutations_table(report_object, table_tex_file="page_operators.tex"):
    pages = {}
    page_names = []
    for _, page in report_object.items():
        initial_page = page["parent"]
        if initial_page not in pages.keys():
            pages[initial_page] = {}
            page_names.append(initial_page)
        for operator in page["mutations"]:
            if operator not in pages[initial_page].keys():
                pages[initial_page][operator] = 0
            pages[initial_page][operator] += 1
    make_resource("page_operators.tex.jinja2", table_tex_file,
                  page_names=page_names, pages=pages
                 )

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

def check_duplicates(output):
    result = {}
    treat_as_dupes = []
    for page_name, checksum in pages_checksum.items():
        for other_page_name, other_checksum in pages_checksum.items():
            # Make sure it's not the same page and we haven't checked the other one yet
            if page_name != other_page_name and other_page_name not in result.keys():
                # Are the checksums the same
                if checksum == other_checksum:
                    if page_name not in result.keys():
                        result[page_name] = []
                    result[page_name].append(other_page_name)
                    treat_as_dupes.append(other_page_name)
    if output is not None:
        with open(output, 'w') as f:
            json.dump(result, f)
    return result, treat_as_dupes

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description="Analyses results of mutation tests")
    argparser.add_argument('pages', help="Path to directory containing all pages")
    argparser.add_argument('reports', help="Path to directory containing all reports")
    argparser.add_argument('output', help="Path to directory to save output", default=None)
    argv = argparser.parse_args(sys.argv[1:] if ".py" in sys.argv[0] else sys.argv)

    build_pages_list(argv.reports)
    load_reports(argv.reports)
    report = build_report(path.join(argv.output, "summary.json"))
    build_results_csv(argv.reports, argv.output)

    equivalence = check_equivalence(argv.pages, report, argv.output)
    duplicates, treat_as_dupes = check_duplicates(path.join(argv.output, "duplicates.json"))

    stats = build_stats(report, equivalence, treat_as_dupes, path.join(argv.output, "stats.json"))
    pages_table(path.join(argv.output, "pages.json"), path.join(argv.output, "pages.tex"))
    stats_mutation_table(stats, path.join(argv.output, "tester_score.tex"))
    stats_operator_table(stats, path.join(argv.output, "operator_score.tex"))
    page_mutations_table(report, path.join(argv.output, "page_operators.tex"))

    page_speeds, tester_speeds = speed.average(speed.load_speeds(argv.reports, sorted(stats['testers'].keys())))
    speed.make_page_speed_table(page_speeds, path.join(argv.output, "page_speed"))
    speed.make_tester_speed_table(tester_speeds, path.join(argv.output, "tester_speed"))

    page_ignores, tester_ignores = load_ignores(os.path.join(argv.output, "pages-ignores.json"), sorted(stats['testers'].keys()))
    # Page ignores
    load_reports(argv.reports, page_ignores=page_ignores)
    page_ignore_report = build_report(path.join(argv.output, "pageignore_summary.json"))
    page_ignore_stats = build_stats(page_ignore_report, equivalence, treat_as_dupes, path.join(argv.output, "pageignore_stats.json"))
    stats_mutation_table(page_ignore_stats, path.join(argv.output, "pageignore_tester_score.tex"))
    # Tool ignores
    load_reports(argv.reports, tester_ignores=tester_ignores)
    tester_ignore_report = build_report(path.join(argv.output, "testerignore_summary.json"))
    tester_ignore_stats = build_stats(tester_ignore_report, equivalence, treat_as_dupes, path.join(argv.output, "testerignore_stats.json"))
    stats_mutation_table(tester_ignore_stats, path.join(argv.output, "testerignore_tester_score.tex"))
    # Both ignores
    load_reports(argv.reports, page_ignores=page_ignores, tester_ignores=tester_ignores)
    ignore_report = build_report(path.join(argv.output, "ignore_summary.json"))
    ignore_stats = build_stats(ignore_report, equivalence, treat_as_dupes, path.join(argv.output, "ignore_stats.json"))
    stats_mutation_table(ignore_stats, path.join(argv.output, "ignore_tester_score.tex"))
