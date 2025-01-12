from datetime import datetime,date
import os
from data_process.match_string import match_string_list_intersection, match_string_list_union, not_match_string_list
from db.models.job_posts import find_jobs_where_search, job_post
from utils.files.dirs import build_dir_name,create_dir
from utils.job_posting.get_job_url import get_job_url_list
from settings.directories import Dirs
from typing import TypedDict

# https://peps.python.org/pep-0589/
class CriteriaConfig(TypedDict):
    or_filter: list[str]
    and_filter:  list[str]
    not_filter:  list[str]
    use_regex: bool
    ignore_case: bool

class CriteriaConfigField(TypedDict):
    field_name: str
    criteria: CriteriaConfig

class Criteria():
    full: CriteriaConfig
    fields: list[CriteriaConfigField]

def filter_search(search :str | None ,criteria: Criteria,name=None):

    jobs_to_filter = find_jobs_where_search(search)
    if search is None: search="all_job_post"

    print(f"filtering on {len(jobs_to_filter)} job posts")
    
    if criteria.full is not None:
        jobs_to_filter = filter_by_field(criteria.full,"description",jobs_to_filter)

    for field in criteria.fields:
        jobs_to_filter = filter_by_field(field['criteria'],field['field_name'],jobs_to_filter)
    
    job_ids = [job.linkedin_id for job in jobs_to_filter ]

    output = f"------------ Match Criteria ------------\n\n"
    output = append_dict(output,vars(criteria))
    output += f'\nDate : {date.today().strftime("%d/%m/%Y")}'
    output += f"\n\n------------ Matches URLS ({len(job_ids)}) ------------\n\n"
    url_list = get_job_url_list(job_ids)
    output += "\n".join(url_list)
    write_filter_res(output,search,name)
    # The ids of the ones left
    return jobs_to_filter

def filter_by_field(criteria:CriteriaConfig,field:str,jobs_to_filter: list[job_post]):
    union_keywords = criteria.get("or",None)
    intersection_keywords = criteria.get("and",None)
    exclusion_keywords = criteria.get("not",None)

    if ( union_keywords is not None ):
        jobs_to_filter, _ = match_string_list_union(jobs_to_filter,union_keywords,extra_criteria=criteria,field_to_search=field)
        
    if ( intersection_keywords is not None ):
        jobs_to_filter = match_string_list_intersection(jobs_to_filter,intersection_keywords,extra_criteria=criteria,field_to_search=field)
        
    if ( exclusion_keywords is not None ):
        jobs_to_filter = not_match_string_list(jobs_to_filter,exclusion_keywords,extra_criteria=criteria,field_to_search=field)
    print(f"After applying {field} filter : {len(jobs_to_filter)}")    
    return jobs_to_filter

def filter_many_union(search,keywords,name=None):
    search_out_dir = build_dir_name(search)    

    matching_files, matches_count = match_string_list_union(search_out_dir,keywords)

    job_ids= get_job_id_from_path(matching_files)
    url_list = get_job_url_list(job_ids)

    output ="------------Matches Count------------\n\n"
    output = append_dict(output,matches_count)
    output += "\n\n------------Matches URLS------------\n\n"
    output += "\n".join(url_list)


    write_filter_res(output,search,name)
    

def filter_many_intersection(search,keywords,name=None):
    search_out_dir = build_dir_name(search)
    matching_files = match_string_list_intersection(search_out_dir,keywords)

    job_ids= get_job_id_from_path(matching_files)
    url_list = get_job_url_list(job_ids)
    output = f"------------Match Criteria------------\n\n  Contains all of : {keywords}\n  Total : {len(url_list)}"
    output += "\n\n------------Matches URLS------------\n\n"
    output += "\n".join(url_list)

    write_filter_res(output,search,name)

def filter_many_exclusion(search,keywords,name=None):
    search_out_dir = build_dir_name(search)
    matching_files = not_match_string_list(search_out_dir,keywords)

    job_ids= get_job_id_from_path(matching_files)
    url_list = get_job_url_list(job_ids)
    output = f"------------Match Criteria------------\n\n  Contains none of : {keywords}\n  Total : {len(url_list)}"
    output += "\n\n------------Matches URLS------------\n\n"
    output += "\n".join(url_list)

    write_filter_res(output,search,name)

def write_filter_res(output,search,name=None):
    filter_out_dir = create_dir(search,Dirs.OUT_FILTER)

    if( name  is None ):
        name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
    elif name == "":
        name = "empty_string"
    else:
        name = name.lower().replace(" ","_")

    filter_out_file= f"{filter_out_dir}{name}.txt"

    with open(filter_out_file, "w", encoding="utf-8") as file:
        file.write(output)

def append_dict(file_str,dict):
    file_str += "\n"
    for key,value in dict.items():
        file_str += f'{key} : {value} \n'
    return file_str
        

def get_job_id_from_path(path_list):
    return [os.path.splitext(os.path.basename(id))[0] for id in path_list]