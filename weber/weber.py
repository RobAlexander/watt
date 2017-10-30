#!/usr/bin/python3

import json
import base64
import os

from flask import Flask, render_template, url_for, request, redirect
import jenkins as jenkins_lib
import requests
from requests.auth import HTTPBasicAuth


JENKINS_JOB_NAME = "WATT"
JENKINS_JOB_BUILD_KEY = "qwertyuiop"
JENKINS_USERNAME = "admin"
JENKINS_PASSWORD = JENKINS_USERNAME
JENKINS_REQUESTS_AUTH = HTTPBasicAuth('admin', 'admin')

MUTATIONS_DIRECTORY = "/vagrant/ampere/mutators"
TESTERS_DIRECTORY = "/vagrant/volt/testers"

app = Flask(__name__)
jenkins = jenkins_lib.Jenkins(
    'http://localhost:8081',
    username=JENKINS_USERNAME,
    password=JENKINS_PASSWORD
)

@app.template_filter('b64encode')
def b64encode(value):
    return base64.b64encode(value.encode('ascii')).decode('utf-8')

@app.template_filter('len')
def len_filter(value):
    return len(value)

@app.before_request
def before_request():
    app.jinja_env.cache = {}

def get_job_data(job, number):
    jenkins_data = jenkins.get_build_info(job, number)
    for action in jenkins_data['actions']:
        if action['_class'] == 'hudson.model.ParametersAction':
            parameters = {param['name']: param['value'] for param in action['parameters']}
    status = "BUILDING" if jenkins_data['building'] else jenkins_data['result']
    return {
        "number": number,
        "mutations": parameters['Mutations'].split(" "),
        "testers": get_job_stats(job, number)['testers'] if status == "SUCCESS" else {},
        "status": status
    }

def get_jenkins_artifact(job, number, artifact):
    jenkins_data = jenkins.get_build_info(job, number)
    return requests.get(
        jenkins_data['url'] + "artifact/run/" + artifact,
        auth=JENKINS_REQUESTS_AUTH
    )

def get_job_stats(job, number):
    return get_jenkins_artifact(job, number, "stats.json").json()

def get_job_summary(job, number):
    return get_jenkins_artifact(job, number, "summary.json").json()

def get_jobs_list(job_name):
    return [get_job_data(job_name, job['number']) \
        for job in jenkins.get_job_info(job_name)['builds']]

@app.route('/')
def main():
    jobs = get_jobs_list(JENKINS_JOB_NAME)
    return render_template("main.html", jobs=jobs)

@app.route('/job')
def job_menu():
    jobs = get_jobs_list(JENKINS_JOB_NAME)
    return render_template("main.html",
                           jobs=jobs, breadcrumb=[{"name": "Job", "url": url_for("job_menu")}])

@app.route('/job/new', methods=['GET', 'POST'])
def new():
    jenkins_info = jenkins.get_job_info(JENKINS_JOB_NAME)
    if request.method == "POST":
        pages = request.form['pages']
        mutations = " ".join(request.form.getlist('mutations'))
        testers = " ".join(request.form.getlist('testers'))
        jenkins.build_job(
                          JENKINS_JOB_NAME,
                          {'Pages':pages, 'Mutations':mutations, 'Testers':testers},
                          JENKINS_JOB_BUILD_KEY
                         )
        return redirect(url_for("new_wait", job=jenkins_info['nextBuildNumber']))
    else:
        params = {}
        for param in jenkins_info['property'][0]['parameterDefinitions']:
            params[param['name']] = param['defaultParameterValue']['value']
            if params[param['name']] == "":
                params[param['name']] = None
        all_mutations = [f.split(".")[0] for f in os.listdir(MUTATIONS_DIRECTORY) if os.path.isfile(os.path.join(MUTATIONS_DIRECTORY, f))]
        all_testers = [f.split(".")[0] for f in os.listdir(TESTERS_DIRECTORY) if os.path.isfile(os.path.join(TESTERS_DIRECTORY, f)) and f.split(".")[-1] == "sh"]
        return render_template("new.html",
                               pages=params['Pages'], mutations=params['Mutations'], testers=params['Testers'],
                               all_mutations=all_mutations, all_testers=all_testers,
                               breadcrumb=[
                                   {"name": "Job", "url": url_for("job_menu")},
                                   {"name": "New", "url": url_for("new")}
                               ]
                              )
                              
@app.route('/job/new/wait/<int:job>')
def new_wait(job):
    try:
        jenkins.get_build_info(JENKINS_JOB_NAME, job)
        return redirect(url_for("job_info", job=job))
    except:
        pass
    return render_template("wait.html", job=job,
                            breadcrumb=[
                                {"name": "Job", "url": url_for("job_menu")},
                                {"name": "Job %d" % job, "url": url_for("new_wait", job=job)}
                            ]
                           )


@app.route('/job/<int:job>')
def job_info(job):
    job_data = get_job_data(JENKINS_JOB_NAME, job)
    job_data_summary = get_job_summary(JENKINS_JOB_NAME, job) if job_data['status'] == "SUCCESS" else None
    console = jenkins.get_build_console_output(JENKINS_JOB_NAME, job)
    return render_template("job.html",
                           job=job_data, summary=job_data_summary, console=console,
                           breadcrumb=[
                               {"name": "Job", "url": url_for("job_menu")},
                               {"name": "Job %d" % job, "url": url_for("job_info", job=job)}
                           ]
                          )

@app.route('/job/<int:job>/summary')
def job_summary(job):
    return json.dumps(get_job_summary(JENKINS_JOB_NAME, job))

@app.route('/job/<int:job>/stats')
def job_stats(job):
    return json.dumps(get_job_stats(JENKINS_JOB_NAME, job))

@app.route('/job/<int:job>/page')
def job_page(job):
    job_data = get_job_data(JENKINS_JOB_NAME, job)
    job_data_summary = get_job_summary(JENKINS_JOB_NAME, job)
    return render_template("pages.html",
                           job=job_data, summary=job_data_summary,
                           breadcrumb=[
                               {"name": "Job", "url": url_for("job_menu")},
                               {"name": "Job %d" % job, "url": url_for("job_info", job=job)},
                               {"name": "Pages", "url": url_for("job_page", job=job)}
                           ]
                          )

@app.route('/job/<int:job>/page/<page>')
def job_page_info(job, page):
    job_data = get_job_data(JENKINS_JOB_NAME, job)
    job_data_summary = get_job_summary(JENKINS_JOB_NAME, job)
    return render_template("page.html",
                           job=job_data, page_name=page, page=job_data_summary[page],
                           breadcrumb=[
                               {"name": "Job", "url": url_for("job_menu")},
                               {"name": "Job %d" % job, "url": url_for("job_info", job=job)},
                               {"name": "Pages", "url": url_for("job_page", job=job)},
                               {"name": page, "url": url_for("job_page_info", job=job, page=page)}
                           ]
                          )

@app.route('/job/<int:job>/page/<page>/raw')
def job_page_raw(job, page):
    return get_jenkins_artifact(JENKINS_JOB_NAME, job, "pages/" + page).text

@app.route('/job/<int:job>/page/<page>/<tester>')
def job_page_tester(job, page, tester):
    job_data = get_job_data(JENKINS_JOB_NAME, job)
    report = get_jenkins_artifact(JENKINS_JOB_NAME, job, "results/" + tester + "/" + page + ".json").json()
    return render_template("page_tester.html",
                           job=job_data, page_name=page, tester=tester, report=report,
                           groups=["violations", "incomplete", "passes", "inapplicable"],
                           breadcrumb=[
                               {"name": "Job", "url": url_for("job_menu")},
                               {"name": "Job %d" % job, "url": url_for("job_info", job=job)},
                               {"name": "Pages", "url": url_for("job_page", job=job)},
                               {"name": page, "url": url_for("job_page_info", job=job, page=page)},
                               {"name": tester, "url": url_for("job_page_tester", job=job, page=page, tester=tester)}
                           ]
                          )


@app.route('/job/<int:job>/page/<page>/<tester>/json')
def job_page_tester_json(job, page, tester):
    return get_jenkins_artifact(JENKINS_JOB_NAME, job, "results/" + tester + "/" + page + ".json").text

@app.route('/job/<int:job>/tester')
def job_tester(job):
    job_data = get_job_data(JENKINS_JOB_NAME, job)
    return render_template("testers.html",
                           job=job_data,
                           breadcrumb=[
                               {"name": "Job", "url": url_for("job_menu")},
                               {"name": "Job %d" % job, "url": url_for("job_info", job=job)},
                               {"name": "Testers", "url": url_for("job_tester", job=job)}
                           ]
                          )

@app.route('/job/<int:job>/tester/<tester>')
def job_tester_info(job, tester):
    job_data = get_job_data(JENKINS_JOB_NAME, job)
    job_data_summary = get_job_summary(JENKINS_JOB_NAME, job)
    return render_template("tester.html",
                           job=job_data, tester_name=tester, summary=job_data_summary,
                           breadcrumb=[
                               {"name": "Job", "url": url_for("job_menu")},
                               {"name": "Job %d" % job, "url": url_for("job_info", job=job)},
                               {"name": "Testers", "url": url_for("job_tester", job=job)},
                               {"name": tester, "url": url_for("job_tester_info", job=job, tester=tester)}
                           ]
                          )

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=8080, debug=True)
