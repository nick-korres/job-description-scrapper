

import time
from settings.element_selector_dictionary import Elements
from utils.general.load_env import app_settings
import uuid
from utils.elements.wait_for import wait_for




def save_page_text_to_temp(driver,page_url=None):
    '''
    This function will save the text of the page to a file
    
    Parameters: 
        driver (WebDriver): The driver instance
        page_url (str): The url of the page to save the text of
    '''
    if(page_url!=None):
        print("page_url",page_url)  
        driver.get(page_url)    

    # timeout = element_wait_timeout + 10
    details = wait_for(driver,Elements.ALL)

    # Generate a UUID to use as the temp file name
    my_uuid = uuid.uuid4()
    file_path = f'./temp/{my_uuid}.txt'

    # Write the extracted text to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(details.text)

    return file_path


def save_page_html_to_temp(driver,page_url):
    '''
    This function will save the text of the page to a file
    
    Parameters: 
        driver (WebDriver): The driver instance
        page_url (str): The url of the page to save the text of
    '''

    driver.get(page_url)
    time.sleep(app_settings["page_wait_timeout"])
    details = wait_for(driver,Elements.ALL)

    # Generate a UUID to use as the temp file name
    my_uuid = uuid.uuid4()
    file_path = f'./temp/{my_uuid}.html'

    # Write the extracted text to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(details.get_attribute('innerHTML'))

    return file_path