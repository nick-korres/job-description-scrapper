import time
from actions.login import login
from data_process.pattern import get_word_distribution_union
from data_process.similarity import calculate_similarity
from db.models.job_posts import job_post
from db.models.user import get_current_user, user
from db.models.user_saw_job_post import connect_user_to_job_post, get_user_saw_job_posts
from db.queries import delete_where
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
    accepted_jobs:list[job_post] = []
    current_job = None
    continue_ = False
    current_is_accepted_ = None
    exit_ = False

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

    def choose(self,job_list : list[job_post],hide_viewed_jobs:bool = True):
        # List to store URLs selected by the user
    
        # Initialize Selenium webdriver , specifically not headless
        driverInstance = get_driver( { "headless": False } )
        current_user: user = get_current_user(driverInstance)

        if hide_viewed_jobs:
            jobs_seen = get_user_saw_job_posts(current_user.id)
            job_list = [job for job in job_list if job.linkedin_id not in jobs_seen]

        keyboard.add_hotkey('alt+c', self.close,suppress=True)
        keyboard.add_hotkey('alt+right', self.add_job,suppress=True)
        keyboard.add_hotkey('alt+left', self.reject_job,suppress=True)
        
        total_jobs = len(job_list)
        index = 1
        for job in job_list:
            self.continue_ = False
            url = f'{Pages.JOB_VIEW}/{job.linkedin_id}'
            # Load the URL in the browser
            login(driverInstance)
            driverInstance.get(url)  
            driverInstance.switch_to.window(driverInstance.current_window_handle)
            
            time.sleep(app_settings["page_wait_timeout"])
            wait_for(driverInstance,Elements.JOB_VIEW_MORE_BUTTON)
            highlight_click(driverInstance,Elements.JOB_VIEW_MORE_BUTTON)

            if is_current_job_expired(driverInstance):
                print(f"{job.linkedin_id} : {job.title} is Expired , deleting it ...")
                delete_where(job_post,"linkedin_id",job.linkedin_id)
                continue
            keyboard.press("esc")  
            keyboard.press("esc")
            self.current_job = job
            
            preferences_dist = load_json(f'{Dirs.OUT_SHOW_AND_CHOOSE}{app_settings["user_url"]}.json')
            if preferences_dist != {}:
                current_job_dist = get_word_distribution_union([self.current_job])
                similarity = calculate_similarity(preferences_dist,current_job_dist)
                print(f"Similarity : {similarity}")

            
            while not self.continue_:
                time.sleep(1)

            user_saw_post(current_user,self.current_is_accepted_,job.linkedin_id)

            if self.exit_:
                print("Exiting ...")
                break
            index += 1
            print(f"Next Job ... {index}/{total_jobs}")

        driverInstance.quit()
        return self.accepted_jobs



def user_saw_post(current_user: user,current_is_accepted:bool,job_id : str):
    if current_is_accepted is None:
        return
    connect_user_to_job_post(current_user.id,job_post_id=job_id,chose_it=current_is_accepted)
    return
    