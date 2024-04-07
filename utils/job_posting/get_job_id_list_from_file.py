
import re


def get_job_id_list_from_file(file_path):
    '''
    This function will return a list of job ids from the job details page
    '''
    job_id_list = []

    pattern = r'data-occludable-job-id=\"(\d+)\"'

    # Open the file and read its contents
    with open(file_path, "r",encoding="utf-8") as file:
        file_contents = file.read()

    # Search for the pattern in the file contents
    matches = re.finditer(pattern, file_contents)
    match_list = list(matches)

    for match in match_list:
            job_id_list.append(match.group(1))

            
    if matches:
        print(f'Found {len(job_id_list)} matches.')
    else:
        matches = []
        print("No ids found in file.")
        
    return job_id_list

def get_job_id_list_from_string(string):
    '''
    This function will return a list of job ids from the job details page
    '''
    # pattern = r'(?<=jobPosting\:)\d{10}\b'
    pattern = r'data-occludable-job-id=\"(\d+)\"'
    pattern = r'(?<=\?currentJobId\=)\d{10}'

    # Search for the pattern in the string
    matches = re.findall(pattern, string)

    if matches:
        print(f'Found {len(matches)} matches.')
    else:
        print("No ids found in string.")
        
    return matches