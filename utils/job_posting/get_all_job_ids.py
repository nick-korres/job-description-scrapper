
import os
import time
from utils.general.list_actions import union_lists
from utils.general.logging import logger
from utils.job_posting.get_job_id_list_from_file import get_job_id_list_from_file, get_job_id_list_from_string
from utils.files.save_page_text_to_temp import save_page_html_to_temp
from utils.url_params import append_url_params
import requests
from selenium.webdriver.remote.webdriver import WebDriver

def get_all_job_ids(driver:WebDriver,start_job_url:str):    
    job_id_list: list[str] = list()
    job_url = start_job_url
    pagination = 0
    have_more_jobs = True
    param_to_add = { "start" : pagination }
    # headers = {
    # 'User-Agent':  driver.execute_script("return navigator.userAgent;") 
    # }
    start_time = time.time()
    index = 0
    # job_url ='https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.search.JobSearchCardsCollection-188&count=25&q=jobSearch&query=(origin:JOB_SEARCH_PAGE_SEARCH_BUTTON,keywords:developer,locationUnion:(geoId:104677530),spellCorrectionEnabled:true)&start=0'
    while have_more_jobs == True:
        # clear log every 5 iterations
        if index % 5 == 0:
            logger.clear_log()
        
        # saving file waits so no need to wait extra for 429 prevention
        temp_file_path = save_page_html_to_temp(driver,job_url)
        current_page_job_id_list = get_job_id_list_from_file(temp_file_path)
        

        # TODO alternative to temp files
        # response = requests.get(url=job_url,params={"start":pagination},headers=headers)
        # data = response.text

        # driver.get(job_url)
        # data = driver.page_source
        # current_page_job_id_list = get_job_id_list_from_string(data)



        current_page_job_id_count =len(current_page_job_id_list)
        pagination += len(current_page_job_id_list)
        # os.remove(temp_file_path)

        # Remove duplicates 
        new_job_id_list = union_lists(job_id_list,current_page_job_id_list)
        new_job_count = len(new_job_id_list) - len(job_id_list)
        job_id_list=[str(job_id) for job_id in new_job_id_list]

        param_to_add = { "start" : pagination }
        # if it exists , it updates it
        job_url = append_url_params(start_job_url,param_to_add)

        print("new_job_count",new_job_count)
        index += 1

        
        if current_page_job_id_count == 0:
            have_more_jobs = False
    print(f"Total time gathering ids {time.time()-start_time}")
    return set(job_id_list)
