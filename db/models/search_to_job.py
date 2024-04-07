import uuid
from db.models.search_strings import find_existing_search, search_strings

from db.queries import delete_where, insert_one


class search_to_job:
    search_id:str
    linkedin_id:str
    def __init__(self,search_id:str, linkedin_id:str):
        self.search_id = search_id
        self.linkedin_id = linkedin_id


def connect_jobs_to_search(saved_jobs_list : list[str] , search_string_id:str):
    new_search_to_job_list = []
    for job in saved_jobs_list :
        new_search_to_job = search_to_job(search_id=search_string_id,linkedin_id=job) 
        insert_one(new_search_to_job)
        new_search_to_job_list.append(new_search_to_job)
    return new_search_to_job_list


def delete_search_cache(search:str):
    existing_search: search_strings | None =  find_existing_search(search)
    if existing_search is None:
        print(f'no entries found for {search}')
        return
    
    # search_to_job is many to many with on delete cascades on both sides
    delete_where(search_strings,"id",existing_search.id)
        