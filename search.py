from actions.save_job_search_descs import save_job_search_descs
from actions.login import login
from settings.pages import SearchLocations
from utils.general.init import driverInstance

# login if needed
login(driverInstance)
clear_cache=False
search_tags = [ "developer", "software", "engineer","backend" ]
location = SearchLocations.ATHENS
# multiple searches that overlap then you can filter on all of them together
total_jobs_added = []
for search in search_tags:
    added_jobs = save_job_search_descs(driverInstance,search,clear_cache,Location=location)
    total_jobs_added += added_jobs
print(f"Total jobs added {len(total_jobs_added)}")



