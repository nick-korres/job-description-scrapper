from settings.element_selector_dictionary import Elements, elements
from utils.general.retry_timeout import retry
from selenium.webdriver.remote.webdriver import WebDriver
from utils.general.load_env import retry_count,retry_delay

@retry( max_attempts = retry_count , delay = retry_delay )   
def find_element_wrapper(driver : WebDriver,element_name: Elements):
    by,value = get_element_selector(element_name)
    element = driver.find_element(by,value)
    return element

@retry( max_attempts = retry_count , delay = retry_delay )   
def find_elements_wrapper(driver : WebDriver ,element_name: Elements):
    by,value = get_element_selector(element_name)
    element = driver.find_elements(by,value)
    return element

def get_element_selector(element_name: Elements):
    by = elements[element_name]["selectBy"]
    value = elements[element_name]["selector"]
    return by,value