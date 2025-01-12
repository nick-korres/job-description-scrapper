import time
from typing import List, TypedDict
from actions.login import login
from data_process.pattern import get_word_distribution_all_fields_union
from data_process.similarity import AllFieldsWeights, calculate_similarity_all_fields
from db.models.job_posts import job_post, set_to_expired
from db.models.user import get_or_add_current_user, user
from db.models.user_saw_job_post import connect_user_to_job_post, get_user_saw_job_posts
from settings.element_selector_dictionary import Elements
from settings.pages import Pages
from utils.elements.wait_for import highlight_click, wait_for
from utils.files.json_cache import load_json
from utils.general.get_driver import get_driver
from utils.general.load_env import app_settings
import keyboard
from settings.directories import Dirs
from utils.job_posting.remove_expired import is_current_job_expired



class Filter:
    accepted_jobs: list[job_post] = []
    current_job = None
    continue_ = False
    driver_was_provided = False
    current_is_accepted_ = None
    exit_ = False
    driver = None
    weights: AllFieldsWeights = {
        "title" : 0.2,
        "description" : 0.2,
        "name" : 0, ## Company name
        "sector" : 0.2,
        "location" : 0,
        "remote" : 0.1,
        "skills_required" : 0.3
    }
    # "-#-" is the delimiter for skills
    excluded_words = ["-#-"]
    def __init__(self,driver=None):
        if driver is None:
            self.driver = get_driver( { "headless": False } )   
        else:
            self.driver = driver
            self.driver_was_provided = True
    
    def __del__(self):
        if self.driver is not None:
            self.driver.quit()
        keyboard.remove_all_hotkeys()

    def add_job(self):
        if self.current_job is not None:
            job_id_list = [job.linkedin_id for job in self.accepted_jobs]
            if self.current_job.linkedin_id not in job_id_list:
                self.accepted_jobs.append(self.current_job)
                print(f'Added {self.current_job.title}')
                self.current_is_accepted_ = True
                self.continue_ = True
    
    def reject_job(self):
        self.current_is_accepted_ = False
        self.continue_ = True

    def close(self):
        self.continue_ = True
        self.exit_ = True

    def choose(self,job_list : list[job_post],hide_viewed_jobs:bool = True , sorted:bool = True):
        # List to store URLs selected by the user
    
        # Initialize Selenium webdriver , specifically not headless

        login(self.driver)
        current_user: user = get_or_add_current_user(self.driver)

        if hide_viewed_jobs:
            jobs_seen = get_user_saw_job_posts(current_user.id,show_expired=False)
            job_seen_ids = [job.job_post_id for job in jobs_seen]
            job_list = [job for job in job_list if job.linkedin_id not in job_seen_ids]

        keyboard.add_hotkey('alt+c', self.close,suppress=True)
        keyboard.add_hotkey('alt+right', self.add_job,suppress=True)
        keyboard.add_hotkey('alt+left', self.reject_job,suppress=True)
        print("Press 'alt+right' to add job , 'alt+left' to reject job , 'alt+c' to close")
        
        total_jobs = len(job_list)
        index = 1
        expired =[]
        preferences_dist = load_json(f'{Dirs.OUT_SHOW_AND_CHOOSE}{app_settings["user_url"]}_all_fields.json')

        
        sorted_jobs = sort_jobs_by_similarity(job_list)
        for sorted_job in sorted_jobs:
            job = sorted_job["job"]

            self.continue_ = False
            url = f'{Pages.JOB_VIEW}/{job.linkedin_id}'
            # Load the URL in the browser
            self.driver.get(url)  
            self.driver.switch_to.window(self.driver.current_window_handle)
            print(f"Showing {job.linkedin_id} : {job.title} ({index}/{total_jobs})")
            time.sleep(app_settings["page_wait_timeout"])

            try:
                wait_for(self.driver,Elements.JOB_VIEW_MORE_BUTTON)
                highlight_click(self.driver,Elements.JOB_VIEW_MORE_BUTTON)
            except:
                print("More button not found")

            if is_current_job_expired(self.driver):
                print(f"{job.linkedin_id} : {job.title} is Expired , deleting it ...")
                expired.append(job.linkedin_id)
                continue
            keyboard.press("esc")  
            keyboard.press("esc")
            self.current_job = job
            
            
            if preferences_dist != {}:
                current_job_dist = get_word_distribution_all_fields_union([self.current_job])
                if sorted_job["similarity"] is None:
                    similarity = calculate_similarity_all_fields(preferences_dist,current_job_dist,self.weights)
                else:
                    similarity = sorted_job["similarity"]
                print(f"Similarity : {similarity}")

            
            while not self.continue_:
                time.sleep(1)


            if self.exit_:
                print("Exiting ...")
                break
            index += 1
            user_saw_post(current_user,self.current_is_accepted_,job.linkedin_id)
            
        if len(expired)>0:
            set_to_expired(expired)
        
        if not self.driver_was_provided:
            self.driver.quit()
        return self.accepted_jobs



def user_saw_post(current_user: user,current_is_accepted:bool,job_id : str):
    if current_is_accepted is None:
        return
    connect_user_to_job_post(current_user.id,job_post_id=job_id,chose_it=current_is_accepted)
    return

class JobSimilarity(TypedDict):
    id: str
    similarity: float
    job: job_post

def sort_jobs_by_similarity(job_list: list[job_post]):
    preferences_dist = load_json(f'{Dirs.OUT_SHOW_AND_CHOOSE}{app_settings["user_url"]}_all_fields.json')
    weights = Filter.weights
    # id to similarity list of dicts


    job_similarities : List[JobSimilarity] = []
    for job in job_list:
        current_job_dist = get_word_distribution_all_fields_union([job])
        similarity = calculate_similarity_all_fields(preferences_dist,current_job_dist,weights)
        job_similarities.append(JobSimilarity(id=job.linkedin_id, similarity=similarity, job=job))
        

    # Descending order by similarity
    sorted_job_similarities = sorted(job_similarities, key=lambda x: x['similarity'], reverse=True)
    
    return sorted_job_similarities