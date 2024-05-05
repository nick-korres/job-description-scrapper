import datetime
import re
from selenium.webdriver.remote.webdriver import WebDriver
from db.db_connect import run_query
from db.models.search_strings import find_existing_search, search_strings
from db.models.search_to_job import search_to_job
from db.queries import find_where, get_class_attributes_without_instance, insert_one, serialize_db_response
from settings.element_selector_dictionary import Elements
from selenium.webdriver.remote.webelement import WebElement
from utils.elements.find_element import find_element_wrapper, find_elements_wrapper
from utils.elements.wait_for import  wait_for
from utils.general.string_manipulation import get_desc_from_inner_html
from utils.job_posting.get_current_job_id import get_current_job_id

class job_post:
    linkedin_id : str
    inner_html : str
    description: str
    create_date : datetime
    title : str
    size : str
    sector : str
    name : str
    location : str
    age_number : str
    age_type : str
    applicants :str
    remote : str
    full  : str
    level : str
    def __init__(self, linkedin_id : str,inner_html : str,description: str,create_date : datetime,title : str,size:str,sector:str,name:str,location:str,age_number:str,age_type:str,applicants,    remote : str, full  : str,level : str):

        self.linkedin_id = linkedin_id
        self.inner_html = inner_html
        self.description = description
        self.create_date = create_date
        self.update_date = datetime.datetime.now()
        self.title= title
        self.size = size
        self.sector = sector
        self.name = name
        self.location = location
        self.age_number = age_number
        self.age_type = age_type
        self.applicants = applicants
        self.remote = remote
        self.full = full 
        self.level = level


    
def save_job_to_db(driver: WebDriver):
    current_job_id = get_current_job_id(driver)
    details : WebElement= wait_for(driver,Elements.ALL)
    inner = details.get_attribute("innerHTML")
    description = get_desc_from_inner_html(inner)

    title,size,sector,name,location,age_number,age_type,applicants,remote,full,level = extract_extra_info(driver)

    new_job_post = job_post(linkedin_id=current_job_id,
                            description=description,
                            inner_html="",
                            create_date=datetime.datetime.now(),
                            title=title,
                            size = size,
                            sector = sector,
                            name = name,
                            location = location,
                            age_number = age_number,
                            age_type = age_type,
                            applicants = applicants,
                            remote=remote,full=full,level=level
                            )
    insert_one(new_job_post)   
    return job_post

def find_jobid_where_search(search:str):
    existing_search: search_strings | None =  find_existing_search(search)

    if existing_search is None: return []

    search_to_job_list: list[search_to_job]= find_where(search_to_job,"search_id",existing_search.id)
    job_id_list = [stj.linkedin_id for stj in search_to_job_list]
    return job_id_list

def find_jobs_where_search(search:str | None):
    columns= get_class_attributes_without_instance(job_post)
    prefixed_columns = [f"job_post.{column}" for column in columns]

    if search is None :
        query = f'SELECT {",".join(prefixed_columns)} FROM job_post '
    else: 
        query = f''' SELECT {",".join(prefixed_columns)} FROM job_post 
    LEFT JOIN search_to_job ON job_post.linkedin_id = search_to_job.linkedin_id 
    LEFT JOIN search_strings ON search_strings.id = search_to_job.search_id 
    WHERE search_strings.search ="{search}"; '''

    query = query.replace('\n', ' ')

    res = run_query(query)
    ser_res:list[job_post] = serialize_db_response(res,job_post)
    return ser_res

def extract_extra_info(driver: WebDriver):
    title=size=sector=name=location=age_number=age_type=applicants=remote=full=level=""
    # TODO maybe remake in a way that all info is dumped to a string and extracted by regex , to avoid throwing error
    try:
        title = find_element_wrapper(driver,Elements.JOB_PAGE_TITLE).text
        middle_dot =" · "
        details_element = find_elements_wrapper(driver,Elements.JOB_PAGE_DETAILS)
        details = [d.text for d in details_element]
        details_index = 0

        remote_full = details[0]
        possible_work_time = ["full-time","contract"]
        full = extract(remote_full,possible_work_time)

        details_index+=2
        # second row contains duplicate information usually
        possible_remote_options = ["remote","hybrid","on-site"]
        remote = extract(remote_full,possible_remote_options)

        level = details[details_index]        
        possible_levels = ["entry","senior","mid","associate"]
        # if level is not there then the index does not change as there is other info on it
        level_exists = any(pos_lev in level.lower() for pos_lev in possible_levels)
        if level_exists : 
            details_index+=1
        else:
            level="not stated"

        if middle_dot not in details[details_index]:
            # When sector info doesn't exists
            size = details[details_index]
        else:
            size,sector = details[details_index].split(middle_dot)
        size = size.replace(" employees","")

        name_location = find_element_wrapper(driver,Elements.JOB_PAGE_COMPANY_NAME_LOCATION).text
        temp = name_location.split(middle_dot)
        if len(temp)>=4 :            
            name,location_age,_,applicants = name_location.split(middle_dot)
        else:
            name,location_age,applicants = name_location.split(middle_dot)

        applicants = applicants.replace(" applicants","").replace(" applicant","")
        
        pattern = r'(\d+)\s+(week|day|month|hour|minute)s? ago'
        temp = re.split(pattern, location_age)
        if len(temp) == 1:
            location = temp[0]
        else:
            location,age_number,age_type,*_ = re.split(pattern, location_age)

        location = location.replace("Reposted","")
        location = location.lstrip().rstrip()
    except Exception as e:
        print(f"error extracting extra info {e}") 
    return title,size,sector,name,location,age_number,age_type,applicants,remote,full,level




def delete_orphan_jobs():
    print("DELETING ORPHANS")
    query = f'''DELETE FROM job_post WHERE job_post.linkedin_id IN(
        SELECT job_post.linkedin_id FROM job_post
        LEFT JOIN search_to_job ON job_post.linkedin_id = search_to_job.linkedin_id
        WHERE search_to_job.linkedin_id IS NULL
        )'''
    run_query(query.replace("\n",""))

def extract(string: str,match_list:list[str]):
    match = " - ".join([match for match in string.split() if match.lower() in match_list])
    if (match == "" ) : match ="Not found"
    return match

def get_jobs_user_saw(user_id:str,only_chose:bool = False):
    columns= get_class_attributes_without_instance(job_post)
    prefixed_columns = [f"job_post.{column}" for column in columns]
    query= f'''
    SELECT {",".join(prefixed_columns)} FROM job_post 
    LEFT JOIN user_saw_job_post ON job_post.linkedin_id = user_saw_job_post.job_post_id'''

    if only_chose:
        query = query + " WHERE user_saw_job_post.user_chose_it = 1"

    query = query.replace("\n","")
    res = run_query(query)
    ser_res:list[job_post] = serialize_db_response(res,job_post)
    return ser_res