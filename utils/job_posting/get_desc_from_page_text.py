
from utils.files.keep_text_between import keep_text_between


def get_desc_from_page_text(file_path):
    '''
    This function will extract the job description from the page text

    Parameters: 
        file_path (str): The path to the file to extract the text from
    '''

    start_string = "About the job"
    end_string = "About the company"
    description = keep_text_between(file_path,start_string,end_string)

    return description