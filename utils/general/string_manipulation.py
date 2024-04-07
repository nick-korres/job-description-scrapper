def get_desc_from_inner_html(inner_html:str):
    start_string = "About the job"
    end_string = "About the company"
    description = keep_text_between(inner_html,start_string,end_string)

    return description


def keep_text_between(string:str, start_string:str, end_string:str ):
    start_index = string.find(start_string) + len(start_string)
    end_index = string.find(end_string)

    substring = string[start_index:end_index]

    if substring =="" or substring == None:
        print("ERROR: No text found between the start and end strings")
    
    return substring 
