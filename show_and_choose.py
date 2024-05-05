from data_process.choose import Filter
from data_process.pattern import get_word_distribution_union
from db.models.job_posts import find_jobs_where_search, job_post
from db.models.search_strings import find_or_create_search, search_strings
from db.models.search_to_job import connect_jobs_to_search, delete_search_cache
from settings.directories import Dirs
from utils.files.json_cache import save_json
from utils.general.load_env import app_settings
from nltk import FreqDist


def show_and_choose(filter_name:str,job_list: list[job_post] ,delete_cache:bool=False,start_from:int=0,save_selection_info:bool=False):
    job_list=job_list[start_from:]

    # Show them one by one with selenium and choose the ones you want to keep
    selected_jobs_list : list[job_post]= Filter().choose(job_list)

    if save_selection_info:
        distribution_union = get_word_distribution_union(selected_jobs_list,excluded_words=[])
        save_distribution(distribution_union)        

    # Save the ones you chose under new search string (filter_name)
    search_string: search_strings = find_or_create_search(filter_name)
    all_jobs= []
    selected_jobs_ids = [job.linkedin_id for job in selected_jobs_list]
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


def save_distribution(dist: FreqDist, user_url:str = app_settings["user_url"],clear_cache:bool=False):
    preferences_file = f'{Dirs.OUT_SHOW_AND_CHOOSE}{user_url}.json'
    merge = not clear_cache
    save_json(preferences_file,dist,merge=merge)


if __name__ == "__main__":
    filter_name = "test_show_and_chose"
    search=None # None to search in all posts
    start_from= 54 # For when we have many results and we want to do the process in batches
    delete_cache = False # If True, it will delete the cache and start from scratch
    job_list = find_jobs_where_search(search)
    show_and_choose(filter_name,job_list,delete_cache,start_from)    
