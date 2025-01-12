from asyncio import sleep
import time
from utils.general.logging import logger
from actions.save_job_search_descs import save_job_search_descs
from actions.login import login
from db.models.job_posts import job_post
from db.queries import count_all
from settings.pages import SearchLocations
from utils.general.get_driver import get_driver



def scrape_tags(driverInstance, search_tags, location, clear_cache=False,depth=1):
    '''
    Scrape job posts for a list of tags

        Parameters:
            driverInstance (WebDriver): The selenium driver instance
            search_tags (list): A list of tags to search for
            location (str): The location to search in
            clear_cache (bool): Whether to clear the cache
            depth (int): How many loops to run, -1 to go until all jobs are found
        Returns:
            None
    '''
    if depth < -1: return

    while True:
        # multiple searches that overlap then you can filter on all of them together
        count_before = count_all(job_post)
        total_jobs_added = []
        total_tags = len(search_tags)
        for search in search_tags:
            logger.print_pin(f"Tag {search} {search_tags.index(search)+1}/{total_tags}",append=False)
            added_jobs = save_job_search_descs(driverInstance,search,clear_cache,Location=location)
            total_jobs_added += [job for job in added_jobs if job not in total_jobs_added]

        count_after = count_all(job_post)
        
        print(f"Total jobs added {len(total_jobs_added)}")
        print(f"Total jobs added real {count_after - count_before}")
    
        if ((depth == -1) and (count_after == count_before)) or (depth == 0):
            break
        depth -= 1
        