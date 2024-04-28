import time
from db.models.job_posts import delete_orphan_jobs, find_jobs_where_search, job_post
from db.queries import delete_where
from settings.element_selector_dictionary import Elements
from settings.pages import Pages
from utils.elements.find_element import find_element_wrapper_no_retry
from utils.elements.wait_for import highlight_click, wait_for
from utils.general.get_driver import get_driver
from utils.general.load_env import app_settings


expiry_text = "No longer accepting applications"

def is_current_job_expired(driverInstance) -> bool:
    try:
        title = find_element_wrapper_no_retry(driverInstance,Elements.JOB_PAGE_APPLY_ERROR).text
        expiry_text_found = expiry_text in title
        return expiry_text_found
    except:
        return False
    
def check_job_expiry(driverInstance ,job: job_post,delete_expired: bool = False) -> bool:
    url = f'{Pages.JOB_VIEW}/{job.linkedin_id}'
    driverInstance.get(url)  
    driverInstance.switch_to.window(driverInstance.current_window_handle)
    time.sleep(app_settings["page_wait_timeout"])
    wait_for(driverInstance,Elements.JOB_VIEW_MORE_BUTTON)
    highlight_click(driverInstance,Elements.JOB_VIEW_MORE_BUTTON)
    is_expired = is_current_job_expired(driverInstance)
    if is_expired and delete_expired:
        delete_where(job_post,"linkedin_id",job.linkedin_id)
    return is_expired

def remove_expired_jobs(driverInstance,job_list : list[job_post]):
    for job in job_list:
        print(f"Checking {job.linkedin_id} : {job.title} for expiration ...")
        try:
            if check_job_expiry(driverInstance,job,delete_expired=True):
                print(f"Deleted {job.linkedin_id} : {job.title}")
        except:
            print(f"Error while checking {job.linkedin_id} : {job.title}")
    return None

def removed_expired_from_search(search: str | None,driverInstance=None):
    if driverInstance is None:
        driverInstance = get_driver({"headless":True})
    job_list: list[job_post] = find_jobs_where_search(search)
    remove_expired_jobs(driverInstance,job_list)

def trim_all_jobs(driverInstance = None):
    if driverInstance is None:
        driverInstance = get_driver({"headless":True})
    removed_expired_from_search(None,driverInstance)
    driverInstance.quit()
    delete_orphan_jobs()


