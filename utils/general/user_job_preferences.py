from selenium.webdriver.remote.webdriver import WebDriver
from nltk import FreqDist
from data_process.pattern import all_field_subtraction, get_word_distribution_all_fields_union, subtract_distributions
from db.models.job_posts import get_jobs_user_saw, job_post
from db.models.user import get_or_add_current_user, user
from settings.directories import Dirs
from utils.files.json_cache import save_json
from utils.general.load_env import app_settings


def save_distribution(dist: FreqDist, user_url:str = app_settings["user_url"],clear_cache:bool=False):
    preferences_file = f'{Dirs.OUT_SHOW_AND_CHOOSE}{user_url}_all_fields.json'
    merge = not clear_cache
    save_json(preferences_file,dist,merge=merge)

def save_current_user_preferences(driver:WebDriver):
    current_user: user = get_or_add_current_user(driver)
    job_posts_seen:list[job_post] = get_jobs_user_saw(current_user.id)
    job_posts_chosen : list[job_post] = get_jobs_user_saw(current_user.id,only_chose=True)
    distribution_union_all_fields = get_word_distribution_all_fields_union(job_posts_chosen,excluded_words=[])
    
    # job_not_chosen = [job for job in job_posts_seen if job not in job_posts_chosen]
    # distribution_union_all_fields_negative = get_word_distribution_all_fields_union(job_not_chosen,excluded_words=[])

    # negative_values_weight = 0.2
    # for field in distribution_union_all_fields_negative:
    #     for word in distribution_union_all_fields_negative[field]:
    #         distribution_union_all_fields_negative[field][word] = distribution_union_all_fields_negative[field][word]*negative_values_weight

    # overall_dist = all_field_subtraction(distribution_union_all_fields,distribution_union_all_fields_negative)
    save_distribution(distribution_union_all_fields,clear_cache=True)
