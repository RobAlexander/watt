#!/usr/bin/python3

from flask import Flask, render_template, url_for
import jenkins as jenkins_lib
import requests
from requests.auth import HTTPBasicAuth

import json


JENKINS_JOB_NAME = "WATT"
JENKINS_USERNAME = "admin"
JENKINS_PASSWORD = JENKINS_USERNAME
JENKINS_REQUESTS_AUTH = HTTPBasicAuth('admin', 'admin')

app = Flask(__name__)
jenkins = jenkins_lib.Jenkins('http://localhost:8081', username=JENKINS_USERNAME, password=JENKINS_PASSWORD)

def get_job_data(job, number):
    jenkins_data = jenkins.get_build_info(job, number)
    for action in jenkins_data['actions']:
        if action['_class'] == 'hudson.model.ParametersAction':
            parameters = {param['name']: param['value'] for param in action['parameters']}
    return {
        "number": number,
        "mutations": parameters['Mutations'].split(" "),
        "testers": requests.get(jenkins_data['url'] + "artifact/run/stats.json", auth=JENKINS_REQUESTS_AUTH).json()['testers'],
        "status": "BUILDING" if jenkins_data['building'] else jenkins_data['result']
    }

def get_job_summary(job, number):
    jenkins_data = jenkins.get_build_info(job, number)
    return requests.get(jenkins_data['url'] + "artifact/run/summary.json", auth=JENKINS_REQUESTS_AUTH).json()

def get_jobs_list(job_name):
    return [get_job_data(job_name, job['number']) for job in jenkins.get_job_info(job_name)['builds']]

@app.route('/')
def main():
    jobs = get_jobs_list(JENKINS_JOB_NAME)
    return render_template("main.html", jobs=jobs)

@app.route('/job')
def job_menu():
    jobs = get_jobs_list(JENKINS_JOB_NAME)
    return render_template("main.html", jobs=jobs, breadcrumb=[{"name": "Job", "url": url_for("job_menu")}])

@app.route('/job/new', methods=['GET', 'POST'])
def new():
    return "New Job"

@app.route('/job/<int:job>')
def job_info(job):
    job_data = get_job_data(JENKINS_JOB_NAME, job)
    job_data_summary = get_job_summary(JENKINS_JOB_NAME, job)
    return render_template("job.html", job=job_data, summary=job_data_summary, breadcrumb=[{"name": "Job", "url": url_for("job_menu")}, {"name": "Job %d" % job, "url": url_for("job_info", job=job)}])

@app.route('/job/<int:job>/summary')
def job_summary(job):
    return "Job %d Summary" % job

@app.route('/job/<int:job>/stats')
def job_stats(job):
    return "Job %d Stats" % job

@app.route('/job/<int:job>/page')
def job_page(job):
    return "Job %d Page Menu" % job

@app.route('/job/<int:job>/page/<page>')
def job_page_info(job, page):
    return "Job %d Page %s" % (job, page)

@app.route('/job/<int:job>/page/<page>/raw')
def job_page_raw(job, page):
    return "Job %d Page %s Raw" % (job, page)

@app.route('/job/<int:job>/tester')
def job_tester(job):
    return "Job %d Tester Menu" % job

@app.route('/job/<int:job>/tester/<tester>')
def job_tester_info(job, tester):
    return "Job %d Tester %s" % (job, tester)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
