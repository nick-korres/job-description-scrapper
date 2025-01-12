import time
from selenium.webdriver.remote.webdriver import WebDriver
import uuid
from db.queries import find_where, insert_one
from settings.element_selector_dictionary import Elements
from settings.pages import Pages
from utils.elements.wait_for import highlight_click, wait_for
from utils.general.load_env import app_settings

class user:
    id : str
    linkedin_url : str
    def __init__(self, id : str, linkedin_url : str):
        self.id = id
        self.linkedin_url = linkedin_url


def add_user(user_url : str):
    new_user_id = str(uuid.uuid4())
    new_user = user(id=new_user_id,linkedin_url=user_url)
    insert_one(new_user)
    return new_user

def get_user_by_url(user_url : str):
    res =  find_where(user,"linkedin_url",user_url)
    if len(res) == 0:
        return None
    if len(res) > 1:
        raise Exception(f"Multiple users found with url {user_url}")
    return res[0]

def get_or_add_current_user(driver: WebDriver):
    if app_settings["user_url"] is None:
        current_user_url = find_current_user_url(driver)    
    else:
        current_user_url = app_settings["user_url"]
    user =  get_user_by_url(current_user_url)
    if user is None:
        user = add_user(current_user_url)
    return user

def find_current_user_url(driver: WebDriver):
    previous_url = driver.current_url
    driver.get(Pages.MAIN)
    time.sleep(app_settings["page_wait_timeout"])
    wait_for(driver,Elements.PROFILE_BUTTON)
    highlight_click(driver,Elements.PROFILE_BUTTON)
    new_user_url = driver.current_url
    driver.get(previous_url)
    return new_user_url

def add_current_user(driver: WebDriver):
    new_user_url = find_current_user_url(driver)
    new_user = add_user(new_user_url)
    return new_user