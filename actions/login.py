from utils.elements.find_element import find_element_wrapper, find_elements_wrapper
from utils.elements.wait_for import wait_for
from utils.general.load_env import email,password
from settings.element_selector_dictionary import Elements
from settings.pages import Pages
from utils.general.retry_timeout import retry
from utils.general.init import driverInstance

def login(driver):
    # Wait for the login button to appear on the page
    print("Waiting for login button")
    is_login_page = find_elements_wrapper(driver,Elements.LOGIN_BUTTON)
    if not is_login_page:
        print("Not in login page")
        return
    clear_authwall(driver)
    # Login

    email_form = wait_for(driver,Elements.EMAIL)
    email_form.send_keys(email)

    password_form = wait_for(driver,Elements.PASSWORD)
    password_form.send_keys(password) 

    log_in_button = wait_for(driver,Elements.LOGIN_BUTTON)
    log_in_button.click()

    print("Waiting for profile button")
    wait_for(driver=driver,element_name=Elements.PROFILE_BUTTON)
    print("Successfully logged in")

@retry(func_at_fail=driverInstance.refresh)
def clear_authwall(driver):
    current_url=driver.current_url
    paywall_string="authwall"

    if paywall_string in current_url:
        driver.get(Pages.LOGIN)

    wait_for(driver,Elements.LOGIN_BUTTON)