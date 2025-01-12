from data_process.filter_search import Criteria, filter_search
from db.models.job_posts import get_jobs_user_saw, job_post
from show_and_choose import show_and_choose






filter_name="user_chosen"
user_id ="343fef39-d142-4ba2-b650-22dea55e5cf1"

job_list: list[job_post] = get_jobs_user_saw(user_id,only_chose=True)
show_and_choose(filter_name,job_list,delete_cache=False,save_selection_info=True,hide_viewed_jobs=False)