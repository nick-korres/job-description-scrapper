import asyncio
import time
from db.models.job_posts import save_job_to_db
from settings.element_selector_dictionary import Elements
from utils.elements.wait_for import highlight_click, wait_for
from settings.pages import Pages
from utils.general.load_env import page_wait_timeout
import time
from selenium.webdriver.remote.webdriver import WebDriver

from utils.general.logging import logger

def scrape_by_job_ids(driver: WebDriver,job_id_list: list[str],base_url=Pages.JOB_VIEW,cached_jobs:list[str]=[]):

    total_jobs = len(job_id_list)
    start_time = None
    dt = None
    saved_jobs = []
    total_time_start = time.time()
    for index,job_id in enumerate(job_id_list):
        if job_id in cached_jobs:
            print(f'using cached version for {job_id}')
            saved_jobs.append(job_id)
            continue
        logger.clear_log()
        print(f"Scraping : {index+1}/{total_jobs}")
        if(start_time is not None):
            dt = time.time()- start_time
        start_time = time.time()
        print(f'job_id {job_id} { "" if dt is None else f" - time elapsed: {dt}"}')

        current_job_page = base_url + job_id
        driver.get(current_job_page)
        time.sleep(page_wait_timeout)
        wait_for(driver,Elements.JOB_VIEW_MORE_BUTTON)
        highlight_click(driver,Elements.JOB_VIEW_MORE_BUTTON)
        save_job_to_db(driver)
        saved_jobs.append(job_id)
        
    # The start_time after last iterations is current time
    print(f'Total time {start_time - total_time_start}')
    return saved_jobs

# def multitask_scrape_by_job_ids(driver,cached_jobs):
#     def partial_scrape_by_job_ids(job_id_list):
#         return scrape_by_job_ids(driver,cached_jobs,job_id_list)
#     return partial_scrape_by_job_ids


async def concurrent_scrape_by_job_ids(driver: WebDriver,job_id_list: list[str],cached_jobs:list[str]=[],max_concurrent=2):
    running_tasks = set()
    start_time = None
    dt = None
    saved_jobs = []
    total_jobs = len(job_id_list)
    loop = asyncio.get_event_loop()

    for index,job_id in enumerate(job_id_list):

        if job_id in cached_jobs:
            print(f'using cached version for {job_id}')
            saved_jobs.append(job_id)
            continue

        new_task = asyncio.create_task(scrape_job_id_single(driver,job_id,thread=index,cached_jobs=cached_jobs))
        running_tasks.add(new_task)

        if len(running_tasks) >= max_concurrent:
            print(f"running {len(running_tasks)} tasks \nWaiting...")
            # response = await asyncio.wait(running_tasks, return_when=asyncio.ALL_COMPLETED)            
            response  = loop.run_until_complete()
            jobs_inserted = [res._result for res in response[0]]
            print("Continuing")

        # current_task = running_tasks.pop()
        # jobs_inserted = [task for task in running_tasks]
        # job_inserted = await current_task
        # [saved_jobs.append(job_inserted) for job_inserted in jobs_inserted]
        # while len(running_tasks) >= max_concurrent:
        #     await asyncio.wait(running_tasks, return_when=asyncio.FIRST_COMPLETED)
        #     running_tasks = {task for task in running_tasks if not task.done()}

        # print(f"current index {index}")
        # task = asyncio.create_task(scrape_job_id_single(driver,job_id,thread=index,cached_jobs=cached_jobs))
        # running_tasks.add(task)

        # print(f"Scraping : {index+1}/{total_jobs}")
        # if(start_time is not None):
        #     dt = time.time()- start_time
        # start_time = time.time()
        # print(f'job_id {job_id} { "" if dt is None else f" - time elapsed: {dt}"}')       

    # resutls = await asyncio.gather(*running_tasks)
    return saved_jobs

async def scrape_job_id_single(driver: WebDriver,job_id: str,thread,cached_jobs:list[str]=[]):
    current_job_page = Pages.JOB_VIEW + job_id
    print(f"thread : {thread}")
    # open new tab
    driver.execute_script("window.open('');")
    # switch to last opened tab
    driver.switch_to.window(driver.window_handles[-1]) 
    driver.get(current_job_page)
    time.sleep(page_wait_timeout)
    wait_for(driver,Elements.JOB_VIEW_MORE_BUTTON)
    highlight_click(driver,Elements.JOB_VIEW_MORE_BUTTON)
    save_job_to_db(driver)
    # close tab that we are currently switched to 
    driver.close()
    # switch back to the original tab 
    driver.switch_to.window(driver.window_handles[0]) 
    return job_id