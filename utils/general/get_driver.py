import os
from selenium.webdriver.chrome.service import Service
from traitlets import Any
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from utils.general.load_env import settings
from settings.browsers import Browsers
import uuid
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
import logging
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def get_driver(settings_override: dict[str, Any] | None = None)-> WebDriver:
    # Values that exist in input should override the original settings
    if settings_override is not None:
        for key,value in settings_override.items():
            if key in settings: settings[key] = value

    LOGGER.setLevel(logging.CRITICAL)
    random_id = uuid.uuid4()
    if(settings["browser"]==Browsers.CHROME):
        options = webdriver.ChromeOptions()
        logging.getLogger('selenium').setLevel(logging.WARNING)
        options.add_argument("--log-level=3")
        options.headless = settings["headless"]
        options.page_load_strategy = settings["load_strategy"]
        options.add_argument(f'--user-agent={random_id}')
        if(settings["user_data_dir_chrome"] and os.path.exists(settings["user_data_dir_chrome"])):
            options.add_argument(f'--user-data-dir={settings["user_data_dir_chrome"]}')
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service,options=options)
    else:
        profile = webdriver.FirefoxProfile()
        options = Options()
        options.headless = settings["headless"]
        logging.getLogger('selenium').setLevel(logging.WARNING)
        options.add_argument("--log-level=3")
        options.page_load_strategy = settings["load_strategy"]
        profile.set_preference("general.useragent.override",random_id.__str__())
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service,firefox_profile=profile,options=options)


    return driver