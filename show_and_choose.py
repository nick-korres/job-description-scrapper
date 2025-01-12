from typing import Dict, List
from data_process.choose import Filter
from data_process.pattern import get_word_distribution_all_fields_union, get_word_distribution_union
from data_process.similarity import AllFieldsWeights, calculate_similarity_all_fields, calculate_similarity_all_fields_parallel
from db.models.job_posts import find_jobs_where_search, job_post
from db.models.search_strings import find_or_create_search, search_strings
from db.models.search_to_job import connect_jobs_to_search, delete_search_cache
from settings.directories import Dirs
from utils.files.json_cache import load_json, save_json
from utils.general.get_driver import get_driver
from utils.general.load_env import app_settings


from utils.general.user_job_preferences import save_current_user_preferences


def show_and_choose(filter_name:str,job_list: list[job_post] ,delete_cache:bool=False,save_selection_info:bool=False,hide_viewed_jobs: bool = True):

    # Show them one by one with selenium and choose the ones you want to keep
    driver = get_driver( { "headless": False } ) 
    selected_jobs_list : list[job_post]= Filter(driver=driver).choose(job_list,hide_viewed_jobs=hide_viewed_jobs)
    driver.quit()

    if save_selection_info:
        save_current_user_preferences(driver)

    # Save the ones you chose under new search string (filter_name)
    upsert_search(selected_jobs_list,filter_name,delete_cache=delete_cache)




def upsert_search(job_list: list[job_post],filter_name:str,delete_cache:bool=False):
    find_or_create_search(filter_name)
    all_jobs= []
    selected_jobs_ids = [job.linkedin_id for job in job_list]
    added_len = 0
    if delete_cache:
        delete_search_cache(filter_name)
        all_jobs = selected_jobs_ids
        added_len = len(all_jobs)
    else:
        connected_before = find_jobs_where_search(filter_name)
        old_jobs = [job.linkedin_id for job in connected_before]
        new_jobs = [id for id in selected_jobs_ids if id not in old_jobs ]
        added_len = len(new_jobs)
        all_jobs = old_jobs + new_jobs
        

    new_search = find_or_create_search(filter_name)
    connect_jobs_to_search(all_jobs,new_search.id)
    connected_after = find_jobs_where_search(filter_name)
    print(f"Connected {added_len} new jobs to {filter_name} (total {len(connected_after)})")    


if __name__ == "__main__":
    filter_name = "test_show_and_chose"
    search=None # None to search in all posts
    start_from= 54 # For when we have many results and we want to do the process in batches
    delete_cache = False # If True, it will delete the cache and start from scratch
    job_list = find_jobs_where_search(search)
    show_and_choose(filter_name,job_list,delete_cache,start_from)



def sort_jobs_by_similarity_parallel(job_list: list[job_post]):
    preferences_dist = load_json(f'{Dirs.OUT_SHOW_AND_CHOOSE}{app_settings["user_url"]}_all_fields.json')
    weights = Filter.weights

    id_to_dist = {job.linkedin_id: get_word_distribution_all_fields_union([job]) for job in job_list}
    id_to_similarity = calculate_similarity_all_fields_parallel(preferences_dist,id_to_dist,weights)
    job_similarity = [(job, id_to_similarity[job.linkedin_id]) for job in job_list]

    # Descending order
    job_similarity.sort(key=lambda x: x[1], reverse=True)
    return job_similarity