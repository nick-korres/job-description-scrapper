from data_process.choose import Filter
from db.models.job_posts import find_jobs_where_search, job_post
from db.models.search_strings import find_or_create_search, search_strings
from db.models.search_to_job import connect_jobs_to_search, delete_search_cache

filter_name = "test_show_and_chose"
search=None # None to search in all posts
start_from=0 # For when we have many results and we want to do the process in batches


# Get all jobs or the ones that match the search
job_list = find_jobs_where_search(search)
job_list=job_list[start_from:]
# Show them one by one with selenium and choose the ones you want to keep
selected_jobs_list : list[job_post]= Filter().choose(job_list)




# Save the ones you chose under new search string (filter_name)
search_string: search_strings = find_or_create_search(filter_name)
connected_before = find_jobs_where_search(filter_name)
delete_search_cache(filter_name)

selected_jobs_ids = [job.linkedin_id for job in selected_jobs_list]
old_jobs = [job.linkedin_id for job in connected_before]
new_jobs = [id for id in selected_jobs_ids if id not in old_jobs ]

connect_jobs_to_search(selected_jobs_ids,search_string.id)
connected_after = find_jobs_where_search(filter_name)
print(f"Connected {len(new_jobs)} new jobs to {filter_name} (total {len(connected_after)})")