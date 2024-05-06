from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings.element_selector_dictionary import Elements
from utils.elements.find_element import get_element_selector
from utils.general.retry_timeout import retry_state, retry
from utils.general.load_env import app_settings
from selenium.webdriver.remote.webdriver import WebDriver

@retry( func_at_fail=lambda: retry_state.callback())
def wait_for(driver: WebDriver,element_name: Elements,timeout: int =app_settings["element_wait_timeout"]):
    by,value = get_element_selector(element_name)
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by,value)))
    # override retry func_at_fail at runtime
    # passing driver.refresh on definition requires driver init at import
    # which leads to unexpected behaviour 
    retry_state.callback = driver.refresh
    return element


def highlight_click(driver,element_name,timeout=app_settings["element_wait_timeout"]):
    clickable_element = wait_for(driver,element_name,timeout)
    driver.execute_script("arguments[0].style.border = '3px solid red'", clickable_element)
    clickable_element.click()



