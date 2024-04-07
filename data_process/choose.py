import time
from db.models.job_posts import job_post
from settings.element_selector_dictionary import Elements
from settings.pages import Pages
from utils.elements.wait_for import highlight_click, wait_for
from utils.general.get_driver import get_driver
from utils.general.load_env import settings
import keyboard



class Filter:
    accepted_jobs:list[job_post] = []
    current_job = None
    continue_ = False
    exit_ = False

    def add_job(self):
        if self.current_job is not None:
            job_id_list = [job.linkedin_id for job in self.accepted_jobs]
            if self.current_job.linkedin_id not in job_id_list:
                self.accepted_jobs.append(self.current_job)
                print(f'Added {self.current_job.title}')
                self.continue_ = True
    
    def reject_job(self):
        self.continue_ = True

    def close(self):
        self.continue_ = True
        self.exit_ = True

    def choose(self,job_list : list[job_post]):
        # List to store URLs selected by the user
    
        # Initialize Selenium webdriver , specifically not headless
        driverInstance = get_driver( { "headless": False } )
        keyboard.add_hotkey('ctrl+c', self.close,suppress=True)
        total_jobs = len(job_list)
        index = 1
        for job in job_list:
            self.continue_ = False
            url = f'{Pages.JOB_VIEW}/{job.linkedin_id}'
            # Load the URL in the browser
            driverInstance.get(url)  
            driverInstance.switch_to.window(driverInstance.current_window_handle)
            time.sleep(settings["page_wait_timeout"])
            wait_for(driverInstance,Elements.JOB_VIEW_MORE_BUTTON)
            highlight_click(driverInstance,Elements.JOB_VIEW_MORE_BUTTON)
            keyboard.press("esc")
            keyboard.press("esc")
            self.current_job = job
            keyboard.add_hotkey('ctrl+right', self.add_job,suppress=True)
            keyboard.add_hotkey('ctrl+left', self.reject_job,suppress=True)
            
            while not self.continue_:
                time.sleep(1)

            if self.exit_:
                print("Exiting ...")
                break
            index += 1
            print(f"Next Job ... {index}/{total_jobs}")

        driverInstance.quit()
        return self.accepted_jobs



