import re

def get_current_job_id(driver):
    '''
    This function will return the current job id
    '''
    if( "view" in driver.current_url):
        patern = r'view/(\d+)/'
    elif ( "currentJobId" in driver.current_url):
       patern = r'currentJobId=(\d+)'
    else:
        raise Exception("Could not get current job id")
    
    match = re.search(patern,driver.current_url)
    if match is None:
        raise Exception("Could not get current job id")
    
    current_job_id = match.group(1)

    if current_job_id == "" or current_job_id == None:
        raise Exception("Could not get current job id")
    
    print(f"Current job id: {current_job_id}")
    return current_job_id