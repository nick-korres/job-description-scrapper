import asyncio
import time
from selenium.webdriver import Firefox,Chrome 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from db.models.job_posts import find_jobid_where_search, job_post
from db.models.search_strings import find_or_create_search, search_strings
from db.models.search_to_job import connect_jobs_to_search, delete_search_cache, search_to_job
from db.queries import delete_where, find_where
from settings.element_selector_dictionary import Elements
from utils.general.cleanup import cleanup
from utils.general.list_actions import intersection_lists
from utils.general.logging import logger
from utils.job_posting.get_all_job_ids import get_all_job_ids
from utils.job_posting.scrape_job_ids import concurrent_scrape_by_job_ids, scrape_by_job_ids
from utils.elements.wait_for import wait_for
from settings.pages import Pages
from utils.general.load_env import app_settings
from selenium.webdriver.remote.webdriver import WebDriver
from utils.url_params import append_url_params

search_jobs_url= Pages.SEARCH_JOBS
search_all_url = Pages.SEARCH_ALL

@cleanup()
def save_job_search_descs(driver:WebDriver,search_string:str,clear_cache:bool = False,Location=None):
    '''
    Search on Linkedin and save descriptions of job postings in /out/:search_string dir
    '''
    
    job_search_url = search(driver,search_string,Location=Location)
    print("Job Search URL : ",job_search_url)

    if (clear_cache):
        delete_search_cache(search_string)
        cached_jobs = []
    else:
        # cached_jobs = find_jobid_where_search(search_string)
        # Get all
        cached_jobs =[jp.linkedin_id for jp in find_where(job_post,"linkedin_id","NULL","IS NOT")]
        
        
    all_job_ids = get_all_job_ids(driver,job_search_url)

    # TODO invalidation should be checking all ids if they still exist not by this search
    # invalidate_cache(all_job_ids,search_string)

    saved_jobs: list[str] = scrape_by_job_ids(driver=driver,job_id_list=all_job_ids,cached_jobs=cached_jobs)
    search_string: search_strings = find_or_create_search(search_string)
    added_jobs = connect_jobs_to_search(saved_jobs,search_string.id)
    return added_jobs

def search(driver:WebDriver,search_string,Location=None):
    '''
    This function will save the job description of the recommended jobs
    '''
    search_url = search_jobs_url
    if Location is not None:
        search_url = append_url_params(search_url,{"location":Location})

    logger.print_pin(f"Searching for : {search_string} at {Location}")
    driver.get(search_url)
    search_bar =  wait_for(driver,Elements.JOB_SEARCH_BOX)
    search_bar.clear()
    search_bar.send_keys(search_string)
    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(app_settings["page_wait_timeout"])

    return driver.current_url

def invalidate_cache(all_job_ids : list[str],search : str):

    cached_jobs = find_jobid_where_search(search)

    cached_from_search = intersection_lists(all_job_ids,cached_jobs)

    logger.print_pin(f'Found {len(all_job_ids)} jobs , {len(cached_from_search)}/{len(all_job_ids)} are cached')

    invalidated_cache = [job_id for job_id in cached_jobs if job_id not in cached_from_search]
    print(f"cache with ids not in new search are invalidated ({len(invalidated_cache)})")
    if len(invalidated_cache) > 1:
        delete_where(
                db_class = search_to_job,
                attribute="linkedin_id",
                operator="IN",
                value=f'({",".join(invalidated_cache)})'
        )