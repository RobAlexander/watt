import json
import os

from common import make_resource

def load_speeds(results_dir, testers):
    speeds = {}
    for tester in testers:
        with open(os.path.join(results_dir, tester + ".json")) as f:
            speeds[tester] = json.load(f)
    return speeds

def average(speeds):
    page_speeds = {}
    tester_speeds = {}
    # Collect
    for tester, pages in speeds.items():
        tester_speeds[tester] = 0
        for page_name, page_speed in pages.items():
            tester_speeds[tester] += page_speed
            if page_name not in page_speeds.keys():
                page_speeds[page_name] = page_speed
            else:
                page_speeds[page_name] += page_speed
    # Average
    for page, speed in page_speeds.items():
        page_speeds[page] = speed / len(tester_speeds.keys())
    for tester, speed in tester_speeds.items():
        tester_speeds[tester] = speed / len(page_speeds.keys())
    return page_speeds, tester_speeds

def make_tester_speed_table(tester_speeds, output):
    make_resource("tester_speed.tex.jinja2", output + ".tex", testers=sorted(tester_speeds.keys()), speeds=tester_speeds)
    with open(output + ".json", 'w') as f:
        json.dump(tester_speeds, f)

def make_page_speed_table(page_speeds, output):
    with open(output + ".json", 'w') as f:
        json.dump(page_speeds, f)
