from settings.pages import Pages

def get_job_url(job_id):
    return f'{Pages.JOB_VIEW}{job_id}'

def get_job_url_list(job_id_list):
    return [get_job_url(url) for url in job_id_list]