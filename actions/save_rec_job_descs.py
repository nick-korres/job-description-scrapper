
from utils.job_posting.get_all_job_ids import get_all_job_ids
from utils.job_posting.scrape_job_ids import scrape_by_job_ids
from settings.pages import Pages
from settings.directories import Dirs

rec_job_url= Pages.RECOMMENDATIONS
out_dir = Dirs.OUT_RECOMMENDATIONS
file_type = ".txt"

def save_rec_job_descs(driver):
    '''
    This function will save the job description of the recommended jobs
    '''

    all_job_ids = get_all_job_ids(driver,rec_job_url)
    
    scrape_by_job_ids(driver,all_job_ids,out_dir)

