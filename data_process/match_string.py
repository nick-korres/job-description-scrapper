import os
import re
from db.models.job_posts import job_post

default_criteria={
     "ignore_case" : True,
     "use_regex" : False
}

def match_string_list_union(jobs_to_filter:list[job_post], search_strings:list[str],extra_criteria=default_criteria,field_to_search="description"):
    # Initialize a dictionary to store the counts of matches for each search string
    matches_count = {search_str: 0 for search_str in search_strings}
    
    # Initialize a list to store matching jobs
    matching_jobs :list[job_post] = list()

    compiled_patterns = compile_patterns(search_strings,extra_criteria)

    for job in jobs_to_filter:            
        for search_key in search_strings:
            field = getattr(job,field_to_search)
            any_string_matched = any(pattern.search(field) for pattern in compiled_patterns)
            if any_string_matched:
                # Increment the count for this search string
                matches_count[search_key] += 1
                # Add the job to the matching jobs list
                matching_jobs.append(job)
                # break  # Exit the loop once a match is found

    return matching_jobs, matches_count


def match_string_list_intersection(jobs_to_filter:list[job_post], search_strings:list[str],extra_criteria=default_criteria,field_to_search="description"):
    matching_jobs :list[job_post] = list()
    compiled_patterns = compile_patterns(search_strings,extra_criteria)
    for job in jobs_to_filter:
        field = getattr(job,field_to_search)         
        all_strings_matched = all(pattern.search(field) for pattern in compiled_patterns)
        # if all_strings_found:
        if all_strings_matched:
        # Add the job to the matching jobs list
            matching_jobs.append(job)
                    
    return matching_jobs

def not_match_string_list(jobs_to_filter:list[job_post], excluded_strings:list[str],extra_criteria=default_criteria,field_to_search="description"):
    matching_jobs :list[job_post] = list()
    compiled_patterns = compile_patterns(excluded_strings,extra_criteria)
    for job in jobs_to_filter:
        field = getattr(job,field_to_search)                 
        any_string_found = any(pattern.search(field) for pattern in compiled_patterns)
        # If none match
        if not any_string_found:
        # Add the job to the matching jobs list
            matching_jobs.append(job)
                    
    return matching_jobs

# def get_file_list(directory,file_list=None):

#     if (file_list is None):
#         files = get_files_in_dir(directory)
#     else:
#         files = file_list

#     return_files = []
#     for file in files:
#         if directory not in file:
#             return_files.append(os.path.join(directory, file))
#         else:
#             return_files.append(file) 

#     return  return_files
    
def compile_patterns(strings,extra_criteria):
    flags=0
    ignore_case = extra_criteria.get("ignore_case",True)
    use_regex = extra_criteria.get("use_regex",True)
    
    if ( ignore_case ):
        flags = flags|re.IGNORECASE

    if ( not use_regex ):
        strings = [re.escape(s) for s in strings]

    patterns =  [re.compile(pattern,flags) for pattern in strings]

    return patterns