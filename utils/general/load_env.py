import json
from dotenv import load_dotenv
import os
from settings.browsers import browser_dict

def to_int_or_default(name,default):
    temp_value = os.getenv(name)
    return int(temp_value) if temp_value is not None else default

def string_to_bool(input:str|int,default=False):
    out = default
    if(input is not None and input.lower()=="true" ):
        out = True
    return out

# Override is needed to ignore current system environment variables
load_dotenv(dotenv_path=".env",override=True)

email = os.getenv("LINKEDIN_USER")
password = os.getenv("LINKEDIN_PASSWORD")
user_url= os.getenv("LINKEDIN_URL")
debug = string_to_bool(os.getenv("DEBUG"))
element_wait_timeout = to_int_or_default("ELEMENT_WAIT",10)
page_wait_timeout = to_int_or_default("PAGE_WAIT",10)
retry_delay = to_int_or_default("RETRY_DELAY",10)
retry_count= to_int_or_default("RETRY_COUNT",3)
browser_num= to_int_or_default("BROWSER",1) # Defaults to Chrome
browser= f'{browser_dict[browser_num]}'
window_x = to_int_or_default("WINDOW_START_X",3000)
window_y = to_int_or_default("WINDOW_START_Y",1000)
headless =  string_to_bool(os.getenv("HEADLESS"))
load_strategy = os.getenv("LOAD_STRATEGY") or "normal"
user_data_dir_chrome = os.getenv("USER_DATA_DIR_CHROME")

print("Loaded environment variables")
settings = { 
    "email" : email,  
    "password" : "****",  
    "user_url" : user_url,  
    "element_wait_timeout" : element_wait_timeout,
    "page_wait_timeout" : page_wait_timeout,  
    "retry_delay" : retry_delay,  
    "retry_count" : retry_count,
    "window_x" : window_x,
    "window_y" : window_y,
    "browser" : browser,
    "user_data_dir_chrome" : user_data_dir_chrome,
    "headless": headless,
    "load_strategy":load_strategy,
    "debug" : debug,
    }
print(json.dumps(settings, indent=4))
# TODO dont run on import 