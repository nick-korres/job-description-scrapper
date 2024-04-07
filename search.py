from actions.save_job_search_descs import save_job_search_descs
from actions.login import login
from utils.general.init import driverInstance

# login if needed
login(driverInstance)
clear_cache=True
search_tags = [ "developer", "software", "engineer" ]


# multiple searches that overlap then you can filter on all of them together
for search in search_tags:
    save_job_search_descs(driverInstance,search,clear_cache)



