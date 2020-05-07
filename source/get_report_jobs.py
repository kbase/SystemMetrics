import requests
import json
import os
from job_info import get_job_info


def get_report_jobs():
    # Get jobs
    job_url = "https://appdev.kbase.us/services/condor-rest-api/v1/jobs/kbase@proda-dock01?"
    running_jobs_constraint = "constraint=jobstatus==2"
    queued_jobs_constraint = "constraint=jobstatus==5"
    response_running = requests.get(job_url + running_jobs_constraint,
                                    headers={'Authorization': os.environ['KB_AUTH_TOKEN']})
    response_queued = requests.get(job_url + queued_jobs_constraint,
                                   headers={'Authorization': os.environ['KB_AUTH_TOKEN']})
    json_data_running = json.loads(response_running.text)
    json_data_queued = json.loads(response_queued.text)
    total_jobs = json_data_running + json_data_queued
    job_info_by_queue = get_job_info(total_jobs)
    job_info_by_queue['total_queued'] = len(json_data_queued)
    job_info_by_queue['total_running'] = len(json_data_running)

    return job_info_by_queue