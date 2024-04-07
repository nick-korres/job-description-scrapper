from data_process.choose import Filter
from data_process.filter_search import filter_search
from data_process.pattern import find_top_words
from db.models.job_posts import find_jobs_where_search, job_post
from db.models.search_strings import find_or_create_search, search_strings
from db.models.search_to_job import connect_jobs_to_search, delete_search_cache
from settings.pages import Pages
# search="Back End Developer"


# name="c++ or javascript"
# keywords=["C++","javascript"]
# filter_many_union(search,keywords,name)

# name="c++ and javascript"
# keywords=["C++","javascript"]
# filter_many_intersection(search,keywords,name)

# name="not senior"
# keywords=["5.*years"]
# filter_many_exclusion(search,keywords,name)

# stack different criteria 

# ----- Potential ideas ------
# maybe multiple or instances so that we can do ["Athens","Attiki"] and ["hybrid","remote"]
# "and" : { "or" :["Athens","Attiki"],"or" : ["hybrid","remote"]}
# maybe chain "or" "and" and "not"  ? have "or" under the "and" for start
# regex can cover that for now

# Example , each (?=) is one more "and" expression
# (?=match this expression)(?=match this too)(?=oh, and this)
# | is "or" so a python data engineer or a c++ embedded is:
# (?=.*python)(?=.*data engineer)|(?=.*c\+\+)(?=.*embedded)

criteria = {
    # "or" : ["Athens|Attiki","hybrid|remote"],
    # "and":["( |,)iot( |,)|internet of things"],
    # "and":["c\+\+|python","research|r&d|algorithm"],
    # "and" : ["back(-|\s)?end","node","remote|hybrid"],
    "and" :[".*"],
    "not" : [
        # "5.*years",
        # "7.*years",
        # "10.*years",
        # "Senior",
        # "devops",
        # " EY,",
        # " Accenture ",
        # "front(-|\s)?end",
        # "React",
        # "UI/UX"
],
    "ignore_case" : True,
    "use_regex" : True
}

# search="developer"
search=None # None to search in all posts
filter_name="test_filter"
job_list: list[job_post] = filter_search(search,criteria,filter_name)
selected_jobs_ids: list[str] = [job.linkedin_id for job in job_list]

search_string: search_strings = find_or_create_search(filter_name)
connected_before: list[job_post]  = find_jobs_where_search(filter_name)
delete_search_cache(search_string)
old_jobs = [job.linkedin_id for job in connected_before]
new_jobs = [id for id in selected_jobs_ids if id not in old_jobs ]
connect_jobs_to_search(selected_jobs_ids,search_string.id)
connected_after: list[job_post]  = find_jobs_where_search(filter_name)
print(f"Connected {len(new_jobs)} new jobs to {filter_name} (total {len(connected_after)})")
