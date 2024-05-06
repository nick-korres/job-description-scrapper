from actions.save_job_search_descs import save_job_search_descs
from actions.login import login
from db.models.job_posts import job_post
from db.queries import count_all
from settings.pages import SearchLocations
from utils.general.get_driver import get_driver

driverInstance = get_driver( { "headless": False } )
# login if needed
login(driverInstance)
clear_cache=False
search_tags = [ "developer", "software", "engineer","backend" ]
location = SearchLocations.ATHENS
# multiple searches that overlap then you can filter on all of them together
count_before = count_all(job_post)
total_jobs_added = []
for search in search_tags:
    added_jobs = save_job_search_descs(driverInstance,search,clear_cache,Location=location)
    total_jobs_added += [job for job in added_jobs if job not in total_jobs_added]

count_after = count_all(job_post)
print(f"Total jobs added {len(total_jobs_added)}")
print(f"Total jobs added real {count_after - count_before}")



